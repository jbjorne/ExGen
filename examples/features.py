import md
import table
import random
import sys
from collections import OrderedDict

class ValidationError(Exception):
    pass

surnames = [
    "Korhonen", "Virtanen", "Mäkinen", "Nieminen", "Mäkelä", "Hämäläinen",
    "Laine", "Heikkinen", "Koskinen", "Järvinen"]

maleNames = ["Juha", "Timo", "Matti", "Kari", "Mikko", "Jari", "Antti", "Jukka", "Mika", "Markku"]

femaleNames = ["Tuula", "Anne", "Päivi", "Anna", "Ritva", "Leena", "Pirjo", "Sari", "Minna", "Marja"]

cities = ["Helsinki", "Espoo", "Tampere", "Vantaa", "Oulu", "Turku", "Jyväskylä",
    "Lahti", "Kuopio", "Pori", "Kouvola"]

def getCat(value, trueValue):
    return "0" if value != trueValue else "1"

#def getCatReverse(value, trueValue):
#    return "1" if value != trueValue else "0"

def getCutoff(value, cutoff):
    return "0" if value <= cutoff else "1"

def getClass(person):
    value = person["ostotapahtumia"]
    if value < 5:
        return 0
    elif value < 10:
        return 1
    else:
        return 2

def manhattan(a, b):
    value = 0
    assert len(a) == len(b)
    a = [int(x) for x in a]
    b = [int(x) for x in b]
    for i in range(len(a)):
        value += abs(a[i] - b[i])
    return value

def calcVectors(persons, data):
    vectors = []
    for i in range(len(persons)):
        person = persons[i]
        vector = getCat(person["sukupuoli"], "nainen")
        vector += getCutoff(person["ikä"], 30)
        vector += getCat(person["asuinpaikka"], "Helsinki")
        vector += getCutoff(person["lapsia"], 0)
        vector += getCat(person["siviilisääty"], "naimisissa")
        vectors.append(vector)
        data["vec" + str(i + 1)] = vector
    return vectors

def calcDistances(persons, vectors, data, testCutoff):
    for i in range(testCutoff, len(vectors)):
        distances = []
        for j in range(0, testCutoff):
            distance = manhattan(vectors[i], vectors[j])
            distances.append((distance, j))
            data["dist" + str(i+1) + "-" + str(j+1)] = distance
        distances.sort()
        nearest = distances[0]
        if distances[1][0] == nearest[0]:
            raise ValidationError("Multiple nearest neighbours")
        data["class" + str(i+1)] = getClass(persons[nearest[1]])

def makeData(seed):
    data = {}
    persons = []
    rand = random.Random(seed)
    for i in range(6):
        person = OrderedDict()
        person["id"] = i + 1
        person["etunimi"] = None
        person["sukunimi"] = rand.choice(surnames)
        person["sukupuoli"] = rand.choice(["mies", "nainen"])
        person["etunimi"] = rand.choice(maleNames) if person["sukupuoli"] == "mies" else rand.choice(femaleNames)
        person["ikä"] = rand.randrange(25, 70)
        person["asuinpaikka"] = rand.choice(cities)
        person["lapsia"] = rand.randrange(0,4)
        person["siviilisääty"] = rand.choice(["naimisissa", "naimaton"])
        person["ostotapahtumia"] = rand.randrange(0,20)
        # The test set classes should be included in the data, because the test set
        # does not represent actually unknown examples, but rather the data used to
        # evaluate system performance.
        #if i >= 4:
        #    person["ostotapahtumia"] = "-"
        persons.append(person)
    vectors = calcVectors(persons, data)
    calcDistances(persons, vectors, data, 4)
    rows = []
    rows.append([x for x in persons[0].keys()])
    for person in persons:
        rows.append([x for x in person.values()])
    data["asiakkaat"] = table.Table(rows, headers=True)
    return data

def makeFeatureExercise(seed):
    data = None
    while data is None:
        try:
            data = makeData(seed)
            data["variant"] = "#" + str(seed)
        except ValidationError as e:
            print(e)
            seed = random.Random(seed).randrange(0, 9999999999999999)
    return md.parse("features.md", data)