import pickle

def save_model(model, filename):
    """saves model into a file named 'filename' """

    pickle_out = open(filename, "wb")
    pickle.dump(model, pickle_out)
    pickle_out.close()


def load_model(filename):
    """loads a model from a file and returns model"""

    pickle_in = open(filename, "rb")
    model = pickle.load(pickle_in)
    return model



