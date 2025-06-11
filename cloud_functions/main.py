from google.cloud import firestore
import functions_framework

db = firestore.Client()

@functions_framework.cloud_event
def update_inventory_on_order(event):
    """Triggered when a new order is created in Firestore"""
    try:
        fields = event.data.get("value", {}).get("fields", {})
        if not fields:
            raise ValueError("No fields in event data")
            
        pid = fields.get("product_id", {}).get("stringValue")
        qty = int(fields.get("quantity", {}).get("integerValue", 0))
        
        if not pid or qty <= 0:
            raise ValueError(f"Invalid product_id ({pid}) or quantity ({qty})")
            
        inv_ref = db.collection("inventory").document(pid)
        snap = inv_ref.get()
        
        if not snap.exists:
            raise ValueError(f"Inventory not found for product {pid}")
            
        current_qty = snap.to_dict().get("quantity", 0)
        new_qty = max(current_qty - qty, 0)
        inv_ref.update({"quantity": new_qty})
        
        print(f"Inventory updated: {pid} = {current_qty} → {new_qty}")
        return f"Inventory updated for {pid}", 200
        
    except Exception as e:
        print(f"Error processing order: {str(e)}")
        return str(e), 500