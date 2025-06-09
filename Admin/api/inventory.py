from google.cloud import firestore
db = firestore.Client()

def get_all_inventory():
    return [doc.to_dict() for doc in db.collection("inventory").stream()]