from google.cloud import firestore
import functions_framework

db = firestore.Client()

@functions_framework.cloud_event
def update_inventory_on_order(event):
    """
    Firestore trigger: fires when a new order doc is created,
    subtracts ordered quantity from inventory, and prevents negatives.
    """
    fields = event.data.get("value", {}).get("fields", {})
    pid = fields.get("product_id", {}).get("stringValue")
    qty = int(fields.get("quantity", {}).get("integerValue", 0))

    if not (pid and qty):
        return  # Skip if missing data

    inv_ref = db.collection("inventory").document(pid)
    snap = inv_ref.get()
    if snap.exists:
        new_qty = max(snap.to_dict().get("quantity", 0) - qty, 0)
        inv_ref.update({"quantity": new_qty})