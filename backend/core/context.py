# backend/core/context.py

from pathlib import Path
from .path_resolver import PathResolver
from .org_service import OrgService


class ExecutionContext:
    def __init__(self, org_id: str, site_id: str):
        self.base_dir = Path(__file__).resolve().parents[2]
        self.org_id = org_id
        self.site_id = site_id

        self.paths = PathResolver(self.base_dir)
        self.org_service = OrgService(self.base_dir)

    # -------------------------------------------------
    # VALIDATION
    # -------------------------------------------------
    def validate(self):
        # Validate against master.json
        self.org_service.validate(self.org_id, self.site_id)

        # Ensure directory exists
        site_dir = self.paths.site_dir(self.org_id, self.site_id)
        site_dir.mkdir(parents=True, exist_ok=True)

    # -------------------------------------------------
    # MODULE INIT
    # -------------------------------------------------
    def init_module(self, module: str):
        self.paths.ensure_module_structure(
            self.org_id,
            self.site_id,
            module,
        )
