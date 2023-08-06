import pickle

def load_model(path):
    with open(path, 'rb') as file:
        model = pickle.load(file)
    return model