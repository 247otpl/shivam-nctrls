# backend/core/bootstrap.py

import json
from pathlib import Path
from backend.core.security import SecurityManager


DEFAULT_BACKUP_COMMANDS = """\
terminal length 0
show running-config
"""

DEFAULT_EXEC_COMMANDS = """\
show version
show ip interface brief
"""

DEFAULT_SETTINGS = {
    "ssh_port": 22,
    "telnet_port": 23,
    "timeout": 10
}

def initialize_environment(base_dir: Path):

    data_dir = base_dir / "data"
    orgs_dir = data_dir / "orgs"

    # Create base directories
    data_dir.mkdir(parents=True, exist_ok=True)
    orgs_dir.mkdir(parents=True, exist_ok=True)

    # Ensure app.key exists
    SecurityManager(base_dir)

def bootstrap_org(base_dir: Path, org_id: str, org_name: str):

    data_dir = base_dir / "data"
    org_dir = data_dir / "orgs" / org_id

    # ---------------------------
    # Create base directories
    # ---------------------------
    (org_dir / "sites").mkdir(parents=True, exist_ok=True)

    # ---------------------------
    # org.json
    # ---------------------------
    org_file = org_dir / "org.json"
    if not org_file.exists():
        org_data = {
            "org_id": org_id,
            "org_name": org_name
        }
        org_file.write_text(json.dumps(org_data, indent=4))

    # ---------------------------
    # Create first site
    # ---------------------------
    bootstrap_site(base_dir, org_id, "site_001", "Primary Site")


def bootstrap_site(base_dir: Path, org_id: str, site_id: str, site_name: str):

    site_dir = (
        base_dir
        / "data"
        / "orgs"
        / org_id
        / "sites"
        / site_id
    )

    site_dir.mkdir(parents=True, exist_ok=True)

    # ---------------------------
    # site.json
    # ---------------------------
    site_file = site_dir / "site.json"
    if not site_file.exists():
        site_data = {
            "site_id": site_id,
            "site_name": site_name
        }
        site_file.write_text(json.dumps(site_data, indent=4))

    # ---------------------------
    # device registry
    # ---------------------------
    registry = site_dir / "device_registry.json"
    if not registry.exists():
        registry.write_text(json.dumps([], indent=4))

    # ---------------------------
    # Modules
    # ---------------------------
    bootstrap_module(site_dir, "config_backup")
    bootstrap_module(site_dir, "command_executor")


def bootstrap_module(site_dir: Path, module_name: str):

    module_dir = site_dir / module_name
    module_dir.mkdir(parents=True, exist_ok=True)

    # commands.txt
    commands_file = module_dir / "commands.txt"
    if not commands_file.exists():
        if module_name == "config_backup":
            commands_file.write_text(DEFAULT_BACKUP_COMMANDS)
        else:
            commands_file.write_text(DEFAULT_EXEC_COMMANDS)

    # settings.json
    settings_file = module_dir / "settings.json"
    if not settings_file.exists():
        settings_file.write_text(json.dumps(DEFAULT_SETTINGS, indent=4))

    # subfolders
    for sub in [
        "credentials",
        "backups",
        "reports",
        "debug_raw",
        "logs",
        "execution_logs"
    ]:
        (module_dir / sub).mkdir(exist_ok=True)
