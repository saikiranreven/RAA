from google.cloud import firestore
import functions_framework
import os
import time

# Initialize Firestore client
db = firestore.Client()

# Add delay to ensure container startup
time.sleep(10)  # 10-second delay for container initialization

@functions_framework.http
def update_inventory(request):
    """HTTP endpoint for inventory updates"""
    try:
        # Get PORT from environment (required for Cloud Run)
        port = int(os.environ.get("PORT", 8080))
        print(f"Server running on port {port}")

        # Process request
        request_json = request.get_json()
        pid = request_json.get('product_id')
        qty = int(request_json.get('quantity', 0))
        
        # Validate input
        if not pid or qty <= 0:
            return {'error': 'Invalid product_id or quantity'}, 400
        
        # Update inventory
        inv_ref = db.collection("inventory").document(pid)
        current_qty = inv_ref.get().to_dict().get('quantity', 0)
        new_qty = max(current_qty - qty, 0)
        inv_ref.update({'quantity': new_qty})
        
        return {
            'status': 'success',
            'product_id': pid,
            'old_quantity': current_qty,
            'new_quantity': new_qty
        }, 200
        
    except Exception as e:
        return {'error': str(e)}, 500

# For local testing
if __name__ == "__main__":
    from flask import Flask, request
    app = Flask(__name__)
    app.route("/", methods=["POST"])(update_inventory)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))