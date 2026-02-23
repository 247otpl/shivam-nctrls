# backend/core/path_resolver.py

from pathlib import Path
from typing import Optional


class PathResolver:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.data_dir = self.base_dir / "data"
        self.orgs_dir = self.data_dir / "orgs"

    # -------------------------------------------------
    # ROOT STRUCTURE
    # -------------------------------------------------
    def master_file(self) -> Path:
        return self.data_dir / "master.json"

    def org_dir(self, org_id: str) -> Path:
        return self.orgs_dir / org_id

    def site_dir(self, org_id: str, site_id: str) -> Path:
        return self.org_dir(org_id) / "sites" / site_id

    def module_dir(self, org_id: str, site_id: str, module: str) -> Path:
        return self.site_dir(org_id, site_id) / module

    # -------------------------------------------------
    # MODULE PATH HELPERS
    # -------------------------------------------------
    def backups_dir(self, org_id: str, site_id: str) -> Path:
        return self.module_dir(org_id, site_id, "config_backup") / "backups"

    def debug_raw_dir(self, org_id: str, site_id: str) -> Path:
        return self.module_dir(org_id, site_id, "config_backup") / "debug_raw"

    def exec_logs_dir(self, org_id: str, site_id: str) -> Path:
        return self.module_dir(org_id, site_id, "command_executor") / "exec_logs"

    def auth_logs_dir(self, org_id: str, site_id: str, module: str) -> Path:
        return self.module_dir(org_id, site_id, module) / "auth_logs"

    def ip_list_file(self, org_id: str, site_id: str, module: str) -> Path:
        return self.module_dir(org_id, site_id, module) / "ip_list.txt"

    def commands_file(self, org_id: str, site_id: str) -> Path:
        return (
            self.module_dir(org_id, site_id, "command_executor")
            / "commands"
            / "commands.txt"
        )

    def credentials_dir(self, org_id: str, site_id: str, module: str) -> Path:
        return self.module_dir(org_id, site_id, module) / "credentials"

    def ensure_module_structure(
        self, org_id: str, site_id: str, module: str
    ):
        base = self.module_dir(org_id, site_id, module)
        base.mkdir(parents=True, exist_ok=True)

        (base / "auth_logs").mkdir(exist_ok=True)

        if module == "config_backup":
            (base / "backups").mkdir(exist_ok=True)
            (base / "debug_raw").mkdir(exist_ok=True)

        if module == "command_executor":
            (base / "exec_logs").mkdir(exist_ok=True)
            (base / "commands").mkdir(exist_ok=True)
