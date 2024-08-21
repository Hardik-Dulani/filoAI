import pickle
def load(file):
    with open(file, "rb") as f:
        loaded_data = pickle.load(f)
    return loaded_data

def dump(data):
    with open(f"{data['id']}.pkl", "wb") as f:
        pickle.dump(data, f)
# x = load('b87a4a3a-519f-412a-87c2-55389a2b0c5f.pkl')
