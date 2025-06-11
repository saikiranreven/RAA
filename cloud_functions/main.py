from google.cloud import firestore
import functions_framework

db = firestore.Client()

@functions_framework.cloud_event
def update_inventory_on_order(event):
    """Triggered when a new order is created in Firestore"""
    try:
        # Directly access the document data from the event structure
        document_data = event.data["value"]["fields"]
        
        # Extract product ID and quantity
        pid = document_data["product_id"]["stringValue"]
        qty = int(document_data["quantity"]["integerValue"])
        
        # Update inventory
        inv_ref = db.collection("inventory").document(pid)
        current_qty = inv_ref.get().to_dict().get("quantity", 0)
        new_qty = max(current_qty - qty, 0)
        inv_ref.update({"quantity": new_qty})
        
        print(f"Inventory updated: {pid} = {current_qty} → {new_qty}")
        return f"Inventory updated for {pid}", 200
        
    except KeyError as e:
        print(f"Missing expected field: {str(e)}")
        return f"Missing field: {str(e)}", 400
    except Exception as e:
        print(f"Error processing order: {str(e)}")
        return str(e), 500