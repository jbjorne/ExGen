from exgen.src.errors import ValidationError
import random
import sys
from collections import OrderedDict

surnames = [ "Brown", "Wilson", "Evans", "Johnson", "Roberts", "Walker", "Wright", "Taylor", "Robinson", "Thompson", "Stevens", "Baker", "Owen"]
maleNames = ["Oliver", "Harry", "George", "Noah", "Jack", "Jacob", "Leo", "Oscar", "Charlie", "Daniel", "Joshua", "Henry", "Theo", "Arthur"]
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
        data["class" + str(i+1)] = predictedClass
    if len(classes) == 1:
        raise ValidationError("Test set examples are of the same class")

def features(options):
    data = {}
    persons = []
    rand = random.Random(options["seed"])
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
        if i < 4:
            person["called"] = "true"
            person["sales"] = 0 if i % 2 == 0 else rand.randrange(100, 900, 20)
        else:
            person["called"] = "false"
            person["sales"] = "-"
        persons.append(person)
    vectors = calcVectors(persons, data)
    calcDistances(persons, vectors, data, 4)
    rows = []
    rows.append([x for x in persons[0].keys()])
    for person in persons:
        rows.append([x for x in person.values()])
    data["persons"] = {"type":"table", "rows":rows, "headers":True}
    return data