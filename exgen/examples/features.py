from exgen.src.errors import ValidationError
import random, itertools
from scipy.spatial.distance import cityblock

surnames = [ "Brown", "Wilson", "Evans", "Johnson", "Roberts", "Walker", "Wright", "Taylor", "Robinson", "Thompson", "Stevens", "Baker", "Owen"]
maleNames = ["Oliver", "Harry", "George", "Noah", "Jack", "Jacob", "Leo", "Oscar", "Charlie", "Daniel", "Joshua", "Henry", "Theo", "Arthur"]
femaleNames = ["Olivia", "Lily", "Sophia", "Emily", "Chloe", "Grace", "Alice", "Sarah", "Emma", "Lucy", "Maya", "Ella"]
cities = ["London"] * 6 + ["Manchester", "Birmingham", "Leeds", "Glasgow", "Liverpool", "Newcastle"]

def vectorize(persons):
    vectors = []
    for p in persons:
        vectors.append([
            0 if p["gender"] == "female" else 1, 
            0 if p["age"] < 50 else 1,
            0 if p["city"] == "London" else 1, 
            0 if p["children"] == 0 else 1,
            0 if p["married"] != "yes" else 1])
    return vectors

def manhattan(persons, vectors, data, testCutoff):
    trainSet = [x for x in range(0, testCutoff)]
    testSet = [x for x in range(testCutoff, len(vectors))]
    distances = [(cityblock(vectors[pair[0]], vectors[pair[1]]), pair[0], pair[1]) for pair in itertools.product(testSet,trainSet)]
    for d, i, j in distances:
        data["dist" + str(i+1) + "-" + str(j+1)] = d
    for i in testSet:
        distances = sorted([(cityblock(vectors[i], vectors[j]), j) for j in trainSet])
        if distances[0][0] == distances[1][0]:
            raise ValidationError("Multiple nearest neighbours")
        persons[i]["predicted"] = -1 if persons[distances[0][1]]["sales"] == 0 else 1
        data["class" + str(i+1)] = persons[i]["predicted"]
    if len(set([persons[i]["predicted"] for i in testSet])) == 1:
        raise ValidationError("Test set examples are of the same class")

def features(options):
    persons = []
    r = random.Random(options["seed"])
    for i in range(6):
        gender = r.choice(["male", "female"])
        names = maleNames if gender == "male" else femaleNames
        persons.append({"id":i + 1, "first name":r.choice(names), "last name":r.choice(surnames),
            "gender":gender, "age":r.randrange(20, 70), "city":r.choice(cities),
            "children":r.randrange(0,4), "married":r.choice(["yes", "no"]),
            "called":"true" if i < 4 else "false", 
            "sales":(0 if i % 2 == 0 else r.randrange(100, 900, 20)) if i < 4 else "-"})
    rows = []
    rows.append([x for x in persons[0].keys()])
    for person in persons:
        rows.append([x for x in person.values()])
    data = {"persons":{"type":"table", "rows":rows, "headers":True}}
    vectors = vectorize(persons)
    manhattan(persons, vectors, data, 4)
    data.update({"vec" + str(i+1):str(v) for i,v in enumerate(vectors)})
    return data