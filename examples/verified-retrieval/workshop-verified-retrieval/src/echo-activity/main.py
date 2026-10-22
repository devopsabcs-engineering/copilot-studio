"""Activity delivery of verified source evidence, never draft model quotations."""

import logging
from urllib.request import urlopen
from uuid import uuid4

from dotenv import load_dotenv

load_dotenv(override=False)

from azure.ai.agentserver.activity import ActivityAgentServerHost

from evidence import EvidenceError, NOTEBOOK_URL, load_corpus
from retrieval import answer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("verified-workshop-retrieval")
with urlopen(NOTEBOOK_URL, timeout=30) as response:
    corpus = load_corpus(response.read(2_000_000))

host = ActivityAgentServerHost()
app = host.agent_app


@app.activity("message")
async def on_message(context, state):
    result = await answer(context.activity.text, corpus)
    logger.info(
        "Verified evidence: retrieval=%s selection=%s records=%s",
        result.retrieval_response_id, result.selection_response_id, result.record_ids,
    )
    await context.send_activity(result.text)


@app.error
async def on_error(context, error):
    reference = str(uuid4())
    logger.error("Evidence delivery failed: reference=%s type=%s", reference, type(error).__name__)
    if isinstance(error, EvidenceError):
        logger.error("Evidence validation rejected the response: %s", error)
    await context.send_activity(
        f"Source verification or delivery failed. No unverified answer was delivered. "
        f"Reference: {reference}"
    )


if __name__ == "__main__":
    host.run()
