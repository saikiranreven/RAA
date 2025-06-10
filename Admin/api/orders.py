from google.cloud import firestore
db = firestore.Client()

def get_all_orders(filter_status=None):
    q = db.collection("orders").order_by("timestamp", direction=firestore.Query.DESCENDING)
    if filter_status:
        q = q.where("status", "==", filter_status)
    return [d.to_dict() for d in q.stream()]

def update_order_status(order_id, new_status):
    db.collection("orders").document(order_id).update({"status": new_status})