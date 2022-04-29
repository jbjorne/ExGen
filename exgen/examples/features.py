from exgen.src.errors import ValidationError
import random
from scipy.spatial.distance import cityblock

# Define the values from which the randomized examples are built
surnames = [ "Brown", "Wilson", "Evans", "Johnson", "Roberts", "Walker", "Wright", "Taylor"]
maleNames = ["Oliver", "Harry", "George", "Noah", "Jack", "Jacob", "Leo", "Oscar", "Charlie", "Daniel"]
femaleNames = ["Olivia", "Lily", "Sophia", "Emily", "Chloe", "Grace", "Alice", "Sarah", "Emma", "Lucy"]
cities = ["London"] * 6 + ["Manchester", "Birmingham", "Leeds", "Glasgow", "Liverpool", "Newcastle"]

def features(options):
    """ Generate the data for the feature vector exercise. """
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
    data = {"persons":{"type":"table", "rows":persons}}
    # Convert the examples into vectors and calculate the distances and nearest neighbours
    vectors = vectorize(persons)
    data.update({"vec" + str(i+1):"".join([str(x) for x in v]) for i,v in enumerate(vectors)})
    manhattan(persons, vectors, data, 4)
    return data

def vectorize(persons):
    """ Convert the person examples into feature vectors """
    return [[0 if p["gender"] == "male" else 1,  0 if p["age"] < 50 else 1,
             0 if p["city"] == "London" else 1,  0 if p["children"] == 0 else 1,
             0 if p["married"] == "no" else 1] for p in persons]

def manhattan(persons, vectors, data, testCutoff):
    """ Calculate the distances and nearest neighbours between the train and test set vectors """
    trainSet = [x for x in range(0, testCutoff)]
    testSet = [x for x in range(testCutoff, len(vectors))]
    for i in testSet:
        distances = sorted([(cityblock(vectors[i], vectors[j]), j) for j in trainSet])
        for distance in distances:
            data["dist" + str(i+1) + "-" + str(distance[1]+1)] = distance[0]
        if distances[0][0] == distances[1][0]:
            raise ValidationError("Multiple nearest neighbours")
        persons[i]["predicted"] = -1 if persons[distances[0][1]]["sales"] == 0 else 1
        data["class" + str(i+1)] = persons[i]["predicted"]
    if len(set([persons[i]["predicted"] for i in testSet])) == 1:
        raise ValidationError("Test set examples are of the same class")