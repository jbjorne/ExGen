import random
import sys
from collections import OrderedDict

class ValidationError(Exception):
    pass

surnames = [ "Brown", "Wilson", "Evans", "Johnson", "Roberts", "Walker", "Wright", "Taylor", "Robinson", "Thompson"]
maleNames = ["Oliver", "Harry", "George", "Noah", "Jack", "Jacob", "Leo", "Oscar", "Charlie", "Daniel", "Joshua"]
femaleNames = ["Olivia", "Lily", "Sophia", "Emily", "Chloe", "Grace", "Alice", "Sarah", "Emma", "Lucy", "Maya", "Ella"]
cities = ["London", "Manchester", "Birmingham", "Leeds", "Glasgow", "Liverpool", "Newcastle"]

def getCat(value, trueValue, reverse=False):
    value = "0" if value != trueValue else "1"
    if reverse:
        value = "0" if value == "1" else "0"
    return value

def getCutoff(value, cutoff):
    return "0" if value <= cutoff else "1"

def getClass(person):
    return 1 if person["sales"] > 0 else -1

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
        vector = getCat(person["gender"], "female")
        vector += getCutoff(person["age"], 50)
        vector += getCat(person["city"], "London", True)
        vector += getCutoff(person["children"], 0)
        vector += getCat(person["married"], "yes")
        vectors.append(vector)
        data["vec" + str(i + 1)] = vector
    return vectors

def calcDistances(persons, vectors, data, testCutoff):
    classes = set()
    numCorrect = 0
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
        predictedClass = getClass(persons[nearest[1]])
        classes.add(predictedClass)
        if predictedClass == getClass(persons[i]):
            numCorrect += 1
        data["class" + str(i+1)] = predictedClass
    if len(classes) == 1:
        raise ValidationError("Test set examples are of the same class")
    if numCorrect == 0:
        raise ValidationError("Both predictions incorrect")

def makeData(seed):
    data = {}
    persons = []
    rand = random.Random(seed)
    for i in range(6):
        person = OrderedDict()
        person["id"] = i + 1
        gender = rand.choice(["male", "female"])
        person["first name"] = rand.choice(maleNames) if gender == "male" else rand.choice(femaleNames)
        person["last name"] = rand.choice(surnames)
        person["gender"] = gender
        person["age"] = rand.randrange(20, 70)
        person["city"] = rand.choice(["London", rand.choice(cities)])
        person["children"] = rand.randrange(0,4)
        person["married"] = rand.choice(["yes", "no"])
        person["sales"] = 0 if i % 2 == 0 else rand.randrange(100, 900, 20)
        person["called"] = "true" if i < 4 else "false"
        persons.append(person)
    vectors = calcVectors(persons, data)
    calcDistances(persons, vectors, data, 4)
    rows = []
    rows.append([x for x in persons[0].keys()])
    for person in persons:
        rows.append([x for x in person.values()])
    data["persons"] = {"type":"table", "rows":rows, "headers":True}
    return data

def features(options):
    data = None
    seed = options["seed"]
    seedRand = random.Random(seed)
    while data is None:
        try:
            data = makeData(seed)
            data["variant"] = "#" + str(seed)
        except ValidationError as e:
            #print(e)
            seed = seedRand.randrange(0, 1000000000)
    return data