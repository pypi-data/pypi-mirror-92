import gzip
import pickle


def save(obj, filename, protocol=-1):
    """Save an object to a compressed disk file.
       Works well with huge objects.
    """
    file = gzip.GzipFile(filename, 'wb')
    pickle.dump(obj, file, protocol)
    file.close()


def load(filename):
    """Loads a compressed object from disk
    """
    file = gzip.GzipFile(filename, 'rb')
    obj = pickle.load(file)
    file.close()

    return obj
