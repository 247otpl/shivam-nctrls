# backend\modules\inventory\adapters\init.py

from .cisco import CiscoAdapter
from .allied import AlliedAdapter
from .tplink import TPLinkAdapter
from .dlink import DLinkAdapter
from .generic import GenericAdapter


def get_adapter(vendor: str):

    vendor = vendor.lower()

    if "cisco" in vendor:
        return CiscoAdapter()

    if "allied" in vendor:
        return AlliedAdapter()

    if "tp-link" in vendor:
        return TPLinkAdapter()

    if "d-link" in vendor:
        return DLinkAdapter()

    return GenericAdapter()
