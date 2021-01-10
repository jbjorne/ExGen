import random

def velocity(seed):
    r = random.Random(seed).randrange
    data = {"v0":r(2, 10), "a":r(1, 5), "t":r(3, 6)}
    data["v"] = data["v0"] + data["a"] * data["t"]
    return data