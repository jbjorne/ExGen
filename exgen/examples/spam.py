import md
import statistics 
from statistics import mode

SENTENCES = [
("")
]

def makeSpamExercise(options, format):
    keywords = ["osta", "verkosta", "tilaisuus", "sinulle", "tarjous"]
    emails = [
        ("Osta nyt halvalla verkosta!", True), 
        ("Uusien opiskelijoiden tilaisuus huomenna", False),
        ("Ainutlaatuinen tilaisuus juuri sinulle", True),
        ("Tarjous! Osta halvalla roinaa", True),
        ("Sinulle on tullut uusi viesti", False),
        ("Osta verkosta! Tarjous sinulle", True),
        ("Tarjous hakemastasi työpaikasta", False)]
    vectors = []

    #for i in range(len(keywords)):
    #    template = template.replace("[key" + str(i+1) + "]", keywords[i])

    # "Emails"
    for i in range(len(emails)):
        email = emails[i]
        #template = template.replace("[email" + str(i+1) + "]", email[0] + " (" + boolToText(email[1]) + ")")
        #print(str(i + 1) + ": " + str(emails[i]))
    
    #print("Vectors")
    for i in range(len(emails)):
        email = emails[i]
        vector = []
        for key in keywords:
            vector.append(1 if key in email[0].lower() else 0)
        vectors.append(vector)
        #vectorString = "".join([str(x) for x in vector])
        #template = template.replace("[vector" + str(i+1) + "]", vectorString)
        #print(str(i+1) + ": " + "".join([str(x) for x in vector]))
    
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
    
    #print("Manhattan distances")
    distances = {6:[], 7:[]}
    for i in range(5):
        d6 = manhattan(vectors[i], vectors[5])
        d7 = manhattan(vectors[i], vectors[6])
        distances[6].append((d6, emails[i][0], emails[i][1]))
        distances[7].append((d7, emails[i][0], emails[i][1]))
        #template = template.replace("[d" + str(i+1) + "6]", str(d6))
        #template = template.replace("[d" + str(i+1) + "7]", str(d7))
        #print(str(i+1) + ": " + str(d6) + ", " + str(d7))
        data["d" + str(i+1) + "6"] = str(d6)
        data["d" + str(i+1) + "7"] = str(d7)
    
    for key in distances:
        distances[key] = sorted(distances[key])
    #print(distances)
    
    #print("Nearest neighbour")
    for i in range(6,8):
        nn = distances[i][0]
        pred = nn[2]
        #template = template.replace("[nn" + str(i) + "]", boolToMulti(pred, 2))
        #print(str(i) + ": " + str(nn) + ", " + str(pred))
        data["nn" + str(i)] = boolToText(pred)
    
    k = 3
    #print("KNN " + str(k))
    for i in range(6,8):
        classes = [x[2] for x in distances[i][0:k]]
        pred = mode(classes)
        #template = template.replace("[knn" + str(i) + "]", boolToMulti(pred, 2))
        #print(str(i) + ": " + str(classes) + ", " + str(pred))
        data["knn" + str(i)] = boolToText(pred)
    
    data["show_answers"] = True
    return md.parse("spam.md", data)

def manhattan(a, b):
    value = 0
    for i in range(len(a)):
        value += abs(a[i] - b[i])
    return value