from google.cloud import firestore
db = firestore.Client()

def get_all_products():
    return [doc.to_dict() for doc in db.collection("products").stream()]