from google.cloud import firestore
import functions_framework

db = firestore.Client()

@functions_framework.cloud_event
def update_inventory_on_order(event):
    data = event.data.get("value", {}).get("fields", {})
    pid = data.get("product_id", {}).get("stringValue")
    qty = int(data.get("quantity", {}).get("integerValue", 0))

    inv = db.collection("inventory").document(pid)
    snap = inv.get()
    if snap.exists:
        current_qty = snap.to_dict().get("quantity", 0)
        new_qty = max(current_qty - qty, 0)
        inv.update({"quantity": new_qty})
