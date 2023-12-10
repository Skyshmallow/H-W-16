import json 

def get_profiles_from_file():
    with open("data.json", "r")as f:
        return json.load(f)
    
    

def set_profiles_to_file(data):
    with open("data.json", "w") as f:
        json.dump(data , f)

    
def jsonify_request(obj, message="Request was succesifull"):
    return {
        "message": message,
        "result": obj
    }


