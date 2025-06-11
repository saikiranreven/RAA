from google.cloud import firestore
import functions_framework
import json

db = firestore.Client()

def extract_firestore_data(event_data):
    """Handles all possible Firestore trigger data formats"""
    if isinstance(event_data, bytes):
        try:
            # Try direct JSON parsing first
            return json.loads(event_data.decode('utf-8'))
        except (UnicodeDecodeError, json.JSONDecodeError):
            # If that fails, try parsing the protoPayload format
            try:
                from google.protobuf.json_format import MessageToDict
                from google.events.cloud.firestore.v1 import DocumentEventData
                proto_data = DocumentEventData()
                proto_data._pb.MergeFromString(event_data)
                return MessageToDict(proto_data._pb)
            except:
                raise ValueError("Unsupported binary format")
    elif isinstance(event_data, dict):
        return event_data
    else:
        raise ValueError("Unknown event data format")

@functions_framework.cloud_event
def update_inventory_on_order(event):
    """Triggered when a new order is created in Firestore"""
    try:
        # Extract and parse the event data
        event_data = extract_firestore_data(event.data)
        
        # Safely navigate the document structure
        fields = event_data.get('value', {}).get('fields', {})
        if not fields:
            raise ValueError("Document has no fields")

        # Extract product ID
        product_info = fields.get('product_id', {})
        pid = product_info.get('stringValue') or product_info.get('referenceValue')
        if not pid:
            raise ValueError("Missing or invalid product_id")

        # Extract quantity (handles both integer and double values)
        quantity_info = fields.get('quantity', {})
        qty = float(quantity_info.get('integerValue') or 
                   quantity_info.get('doubleValue') or 0)
        qty = int(qty) if qty.is_integer() else qty

        if qty <= 0:
            raise ValueError(f"Invalid quantity: {qty}")

        # Update inventory
        inv_ref = db.collection("inventory").document(pid)
        doc = inv_ref.get()
        
        if not doc.exists:
            raise ValueError(f"Inventory not found for product {pid}")

        current_qty = doc.to_dict().get('quantity', 0)
        new_qty = max(current_qty - qty, 0)
        inv_ref.update({'quantity': new_qty})
        
        print(f"Success: {pid} updated from {current_qty} to {new_qty}")
        return {'status': 'success', 'product_id': pid, 'new_quantity': new_qty}, 200

    except Exception as e:
        error_msg = f"Error processing order: {str(e)}"
        print(error_msg)
        return {'status': 'error', 'message': error_msg}, 500