from google.cloud import firestore

def get_all_orders():
    db = firestore.Client()
    docs = db.collection('orders').stream()
    return [doc.to_dict() for doc in docs]