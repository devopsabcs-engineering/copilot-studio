"""Stateless HTTP delivery of the same verified evidence as the Activity route."""
import json
import logging
from uuid import uuid4

from azure.ai.agentserver.activity import ActivityAgentServerHost
from azure.core.exceptions import AzureError
from openai import APIError
from starlette.requests import Request
from starlette.responses import JSONResponse

from evidence import EvidenceError, Record
import retrieval

logger = logging.getLogger(__name__)
MAX_REQUEST_BYTES = 150000


def error_response(status: int, code: str, message: str, error: Exception | None = None) -> JSONResponse:
    reference = str(uuid4())
    logger.log(
        logging.ERROR if status >= 500 else logging.WARNING,
        "Invocation rejected: reference=%s status=%s code=%s type=%s",
        reference, status, code, type(error).__name__ if error else "InvalidRequest",
    )
    return JSONResponse(
        {"error": {"code": code, "message": message, "reference": reference}},
        status_code=status,
    )


def openapi_spec() -> dict:
    result_schema = {
        "type": "object",
        "additionalProperties": False,
        "required": ["text", "record_ids", "retrieval_response_id", "selection_response_id"],
        "properties": {
            "text": {"type": "string"},
            "record_ids": {"type": "array", "items": {"type": "string"}, "uniqueItems": True},
            "retrieval_response_id": {"type": "string"},
            "selection_response_id": {"type": ["string", "null"]},
        },
    }
    error_schema = {
        "type": "object", "required": ["error"], "additionalProperties": False,
        "properties": {"error": {
            "type": "object", "required": ["code", "message", "reference"],
            "additionalProperties": False,
            "properties": {
                "code": {"type": "string"}, "message": {"type": "string"},
                "reference": {"type": "string", "format": "uuid"},
            },
        }},
    }
    return {
        "openapi": "3.1.0",
        "info": {
            "title": "Verified workshop retrieval", "version": "1.0.0",
            "description": (
                "Stateless container transport. For hosted calls use the Foundry agent's "
                "canonical Invocations endpoint, protected by Entra and Azure RBAC."
            ),
        },
        "security": [{"foundryBearer": []}],
        "components": {"securitySchemes": {"foundryBearer": {
            "type": "http", "scheme": "bearer", "bearerFormat": "JWT",
            "description": "Enforced by the hosted Foundry gateway; local development is loopback-only.",
        }}},
        "paths": {"/invocations": {"post": {
            "operationId": "retrieveVerifiedEvidence",
            "requestBody": {
                "required": True,
                "content": {"application/json": {"schema": {
                    "type": "object", "required": ["question"], "additionalProperties": False,
                    "properties": {"question": {
                        "type": "string", "minLength": 1,
                        "maxLength": retrieval.MAX_QUESTION_LENGTH, "pattern": r"\S",
                    }},
                }}},
            },
            "responses": {
                "200": {
                    "description": "Verbatim evidence or explicit no-evidence abstention",
                    "content": {"application/json": {"schema": result_schema}},
                },
                **{
                    str(status): {
                        "description": description,
                        "content": {"application/json": {"schema": error_schema}},
                    }
                    for status, description in (
                        (400, "Invalid request"), (413, "Request too large"),
                        (415, "Unsupported media type"), (502, "Verification or retrieval failed"),
                        (504, "Retrieval timed out"),
                    )
                },
            },
        }}},
    }


def register_invocations(host: ActivityAgentServerHost, corpus: dict[str, Record]) -> None:
    async def invoke(request: Request) -> JSONResponse:
        if request.headers.get("content-type", "").split(";", 1)[0].strip().lower() != "application/json":
            return error_response(415, "unsupported_media_type", "Content-Type must be application/json.")
        body = bytearray()
        async for chunk in request.stream():
            if len(body) + len(chunk) > MAX_REQUEST_BYTES:
                return error_response(413, "request_too_large", f"Request must not exceed {MAX_REQUEST_BYTES} bytes.")
            body.extend(chunk)
        try:
            payload = json.loads(body.decode("utf-8"))
        except (ValueError, RecursionError) as error:
            return error_response(400, "invalid_request", "Request must be valid UTF-8 JSON.", error)
        if not isinstance(payload, dict) or set(payload) != {"question"}:
            return error_response(400, "invalid_request", "Request must contain only a question string.")
        try:
            question = retrieval.validate_question(payload["question"])
        except ValueError as error:
            return error_response(400, "invalid_request", str(error), error)
        try:
            result = await retrieval.answer(question, corpus)
        except (EvidenceError, json.JSONDecodeError) as error:
            return error_response(
                502, "source_verification_failed",
                "Source verification failed. No unverified answer was delivered.", error,
            )
        except TimeoutError as error:
            return error_response(504, "retrieval_timed_out", "Verified retrieval timed out.", error)
        except (AzureError, APIError) as error:
            return error_response(502, "retrieval_failed", "Verified retrieval failed.", error)
        logger.info(
            "Verified invocation: retrieval=%s selection=%s records=%s",
            result.retrieval_response_id, result.selection_response_id, result.record_ids,
        )
        return JSONResponse({
            "text": result.text, "record_ids": list(result.record_ids),
            "retrieval_response_id": result.retrieval_response_id,
            "selection_response_id": result.selection_response_id,
        })

    async def schema(_request: Request) -> JSONResponse:
        return JSONResponse(openapi_spec())

    host.add_route("/invocations", invoke, methods=["POST"])
    host.add_route("/invocations/docs/openapi.json", schema, methods=["GET"])
