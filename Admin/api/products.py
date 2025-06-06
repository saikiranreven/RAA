from google.cloud import firestore

def get_all_products():
    db = firestore.Client()
    docs = db.collection('products').stream()
    return [doc.to_dict() for doc in docs]