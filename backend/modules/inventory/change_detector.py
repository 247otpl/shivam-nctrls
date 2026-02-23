# backend/modules/inventory/change_detector.py

from datetime import datetime


def detect_inventory_changes(existing_inventory, new_data):

    changes = []

    for key, new_value in new_data.items():

        if key not in existing_inventory:
            continue

        field = existing_inventory[key]

        old_value = field.get("value")
        source = field.get("source")

        # Skip manual overrides
        if source == "manual":
            continue

        # Skip first-time population
        if not old_value:
            continue

        if old_value != new_value:

            changes.append({
                "field": key,
                "old_value": old_value,
                "new_value": new_value,
                "timestamp": datetime.now().isoformat()
            })

    return changes
