from google.cloud import firestore

def get_all_inventory():
    db = firestore.Client()
    docs = db.collection('inventory').stream()
    return [doc.to_dict() for doc in docs]