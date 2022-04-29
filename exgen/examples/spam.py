import math
import random
from statistics import mode

def boolToText(value):
    return 'Kyllä' if value else 'Ei'

def boolToMulti(value):
    return {"choices":['Kyllä', 'Ei'], "correct":"Kyllä" if value else 'Ei', "ordered":True}

def manhattan(a, b):
    value = 0
    for i in range(len(a)):
        value += abs(a[i] - b[i])
    return value

def spam(options):
    r = random.Random(options["seed"])
    keywords = ["osta", "netistä", "tilaisuus", "sinulle", "tarjous"]
    dataset = [
        ("Osta nyt halvalla netistä!", True), 
        ("Ainutlaatuinen tilaisuus juuri sinulle", True),
        ("Tarjous! Osta halvalla roinaa", True),
        ("Netistä sinulle halvalla", True),
        ("Osta netistä! Tarjous sinulle", True),
        ("Ainutlaatuinen tarjous! Osta halvalla!", True),
        ("Halvalla sinulle laatua", True),
        ("Sinulle on tullut uusi viesti", False),
        ("Tarjous hakemastasi työpaikasta", False),
        ("Uusien opiskelijoiden tilaisuus huomenna", False),
        ("Tilaus on saapunut sinulle", False),
        ("Onko sinulle tullut kysely?", False),
        ("Tilasin netistä polkupyörän", False)
    ]
    vectors = []

    # Emails
    numEmails = 7
    positives = r.sample([x for x in dataset if x[1]], math.floor(0.5 * numEmails))
    negatives = r.sample([x for x in dataset if not x[1]], math.ceil(0.5 * numEmails))
    trainSet = positives[1:] + negatives[1:]
    testSet = [positives[0], negatives[0]]
    r.shuffle(trainSet)
    r.shuffle(testSet)
    emails = trainSet + testSet
    
    # Vectors
    r.shuffle(keywords)
    for i in range(len(emails)):
        email = emails[i]
        vector = []
        for key in keywords:
            vector.append(1 if key in email[0].lower() else 0)
        vectors.append(vector)
    
    data = {}
    for key, values in {"key":keywords, "email":emails, "vector":vectors}.items():
        for i in range(len(values)):
            dataKey = key + str(i+1)
            if key == "email":
                data[dataKey] = values[i][0] + " (" + boolToText(values[i][1]) + ")"
            elif key == "vector":
                data[dataKey] = "".join([str(x) for x in values[i]])
            else:
                data[dataKey] = values[i]
    
    # Manhattan distances
    distances = {6:[], 7:[]}
    for i in range(5):
        d6 = manhattan(vectors[i], vectors[5])
        d7 = manhattan(vectors[i], vectors[6])
        distances[6].append((d6, emails[i][0], emails[i][1]))
        distances[7].append((d7, emails[i][0], emails[i][1]))
        data["d" + str(i+1) + "6"] = str(d6)
        data["d" + str(i+1) + "7"] = str(d7)
    
    for key in distances:
        distances[key] = sorted(distances[key])
    
    # Nearest neighbour
    for i in range(6,8):
        nn = distances[i][0]
        pred = nn[2]
        data["nn" + str(i)] = boolToMulti(pred)
    
    k = 3
    for i in range(6,8):
        classes = [x[2] for x in distances[i][0:k]]
        pred = mode(classes)
        data["knn" + str(i)] = boolToMulti(pred)
    
    return data