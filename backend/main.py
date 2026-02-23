# backend/main.py

from fastapi import FastAPI
from pathlib import Path

from backend.core.bootstrap import initialize_environment
from backend.modules.inventory.contract_scheduler import ContractScheduler

# Import routers
from backend.api.routes import org
from backend.api.routes import provisioning
from backend.api.routes import credentials
from backend.api.routes import discovery
from backend.api.routes import history
from backend.api.routes import config_backup
from backend.api.routes import command_executor
from backend.api.routes import command_executor_history
from backend.api.routes import inventory


app = FastAPI(title="NetControlSuite v2")

# -------------------------------------------------
# INITIALIZE ENVIRONMENT
# -------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
initialize_environment(BASE_DIR)

# -------------------------------------------------
# SERVICE CONTRACT AUTO CHECK SCHEDULER (Currently Disabled)
# -------------------------------------------------
# contract_scheduler = ContractScheduler(BASE_DIR)
# contract_scheduler.start()

# -------------------------------------------------
# REGISTER ROUTERS
# -------------------------------------------------
app.include_router(
    org.router,
    prefix="/api/org",
    tags=["Organization"]
)

app.include_router(
    credentials.router,
    prefix="/api/credentials",
    tags=["Credentials"]
)

app.include_router(
    discovery.router,
    prefix="/api/discovery",
    tags=["Discovery"]
)

app.include_router(
    provisioning.router,
    prefix="/api/devices",
    tags=["Devices"]
)

app.include_router(
    config_backup.router,
    prefix="/api/config-backup",
    tags=["Config Backup"]
)

app.include_router(
    history.router,
    prefix="/api/history",
    tags=["Backup Execution History"]
)

app.include_router(
    command_executor.router,
    prefix="/api/command-executor",
    tags=["Command Executor"]
)

app.include_router(
    command_executor_history.router,
    prefix="/api/history/command-executor",
    tags=["Command Executor History"]
)

app.include_router(
    inventory.router,
    prefix="/api/inventory",
    tags=["Inventory"]
)
