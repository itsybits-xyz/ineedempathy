import os
import uvicorn
from alembic.config import Config
from alembic import command

# Run migrations

alembic_cfg = Config("./alembic.ini")
command.upgrade(alembic_cfg, "head")

# Start server

uvicorn.run("backend.main:app", host="127.0.0.1",
        port=int(os.getenv('USE_PORT')), log_level="info")
