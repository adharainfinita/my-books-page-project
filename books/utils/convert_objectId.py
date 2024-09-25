from bson import ObjectId

def str_to_objectid(id: str):
    try:
        return ObjectId(id)
    except Exception as e:
        print(f"Error converting to ObjectId: {e}")
        return None