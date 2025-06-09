from google.cloud import firestore
db = firestore.Client()

def get_all_orders():
    return [doc.to_dict() for doc in db.collection("orders").stream()]