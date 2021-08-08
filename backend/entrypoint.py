import sentry_sdk
import uvicorn
from alembic.config import Config
from alembic import command

# Run migrations

alembic_cfg = Config("./alembic.ini")
command.upgrade(alembic_cfg, "head")

# Start server

sentry_sdk.init(
    "https://2147b3c92a9b482eaefc19feaeda5ecd@o948279.ingest.sentry.io/5897486",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
)

# uvicorn.run("backend.main:app", fd=0, log_level="debug")
uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, log_level="debug")
