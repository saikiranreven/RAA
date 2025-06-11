from google.cloud import firestore
import functions_framework

db = firestore.Client()

@functions_framework.cloud_event
def update_inventory_on_order(event):
    data = event.data.get("value", {}).get("fields", {})

    if not data:
        print("❌ Missing value fields in event")
        return

    product_id = data.get("product_id", {}).get("stringValue")
    qty_str = (
        data.get("quantity", {}).get("integerValue") or
        data.get("quantity", {}).get("doubleValue")
    )

    try:
        quantity = int(float(qty_str)) if qty_str else 0
    except ValueError:
        print("❌ Invalid quantity format")
        return

    if not product_id or quantity <= 0:
        print(f"⛔ Invalid product_id ({product_id}) or quantity ({quantity})")
        return

    inv_ref = db.collection("inventory").document(product_id)
    snap = inv_ref.get()

    if not snap.exists:
        print(f"⚠️ Inventory not found for product_id={product_id}")
        return

    current_qty = int(snap.to_dict().get("quantity", 0))
    new_qty = max(current_qty - quantity, 0)

    inv_ref.update({"quantity": new_qty})
    print(f"✔️ Inventory updated: {product_id} = {current_qty} → {new_qty}")