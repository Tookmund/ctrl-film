import hashlib

def hash(thing):
    sha256 = hashlib.new("sha256")
    if type(thing) is str:
        sha256.update(thing.encode())
    else:
        thing.seek(0)
        sha256.update(thing.read())
    return sha256.hexdigest()
