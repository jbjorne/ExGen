import copy
import random
import sys
import os

# Heuristics ##################################################################

def getPositions(width, height):
    count = 1
    positions = {} #[[None for x in range(width)] for y in range(height)]
    for i in range(height):
        for j in range(width):
            positions[count] = (i, j)
            count += 1
    positions[0] = (width-1, height-1)
    return positions

def getHeuristicDistance(state, positions):
    total = 0
    for i in range(len(state)):
        for j in range(len(state[i])):
            tile = state[i][j]
            distance = abs(i - positions[tile][0]) + abs(j - positions[tile][1])
            #print tile, (i, j), positions[tile], distance
            if tile != 0:
                total += distance
    return total

def getHeuristicOutOfPlace(state, positions):
    total = 0
    for i in range(len(state)):
        for j in range(len(state[i])):
            tile = state[i][j]
            if tile != 0 and (positions[tile][0] != i or positions[tile][1] != j):
                total += 1
    return total

HEURISTICS = {
    "OOP":{
        "func":getHeuristicOutOfPlace, 
        "desc":"number of tiles out of place (e.g. the starting position heuristic value would be 5, because tiles 5, 2, 4, 7 and 8 are out of place)"
        },
    "distance":{
        "func":getHeuristicDistance, 
        "desc":"The sum of tile distances from their correct place (e.g. the starting position heuristic value would be 5, because tiles 5, 2, 4, 7 and 8 are out of place)"
    },
}

# Search Tree #################################################################

def getMoves(state):
    moves = []
    h = len(state)
    w = len(state[0])
    for i in range(w):
        for j in range(h):
            for step in ((1,0), (-1,0), (0,1), (0,-1)):
                i2 = i + step[0]
                j2 = j + step[1]
                if i2 < 0 or i2 >= w or j2 < 0 or j2 >= h:
                    continue
                if state[i2][j2] == 0:
                    move = copy.deepcopy(state)
                    move[i2][j2] = move[i][j]
                    move[i][j] = 0
                    moves.append(move)
    return moves

def build(initial, numLevels, getHeuristic):
    positions = getPositions(len(initial), len(initial[0]))
    print(initial, positions)
    root = {"index":0, "state":initial, "parent":None, "children":[], "heuristic":getHeuristic(initial, positions), "level":0, "allNodes":[]}
    root["allNodes"].append(root)
    graph = {}
    graph["source"] = "digraph G {\n"
    graph["source"] += "forcelabels=true;\n"
    graph["source"] += "concentrate=True;\n"
    graph["source"] += "rankdir=TB;\n"
    graph["source"] += "node [shape=record, margin=0];\n"
    graph["source"] += nodeToString(root)
    addNodes(root, numLevels, set(), graph, getHeuristic)
    graph["source"] += "}"
    print(graph)
    return root, graph

def addNodes(current, maxLevel, visited, graph, getHeuristic):
    if current["level"] < maxLevel:
        for state in getMoves(current["state"]):
            if str(state) not in visited:
                positions = getPositions(len(state), len(state[0]))
                heuristic = getHeuristic(state, positions)
                visited.add(str(state))
                node = {"index":len(visited), "state":state, "parent":current, "children":[], "heuristic":heuristic, "level":current["level"] + 1, "allNodes":current["allNodes"]}
                current["children"].append(node)
                current["allNodes"].append(node)
        for node in current["children"]:
            graph["source"] += nodeToString(node)
            graph["source"] += "N" + str(current["index"]) + " -> " + "N" + str(node["index"]) + ";\n"
            addNodes(node, maxLevel, visited, graph, getHeuristic)

def nodeToString(node, xlabel=True):
    label = "{" + "|".join(["{" + "|".join([str(x) if x != 0 else "_" for x in row]) + "}" for row in node["state"]]) + "}"
    name = "N" + str(node["index"])
    name += " [label=\"" + label + "\""
    if xlabel:
        name += ",xlabel=\"" + name + "\"
    name += "];\n"
    return name

def shuffle(state, numSteps, rand):
    seen = set()
    unused = []
    for i in range(numSteps):
        moves = [x for x in getMoves(state) if str(x) not in seen]
        for move in moves:
            seen.add(str(move))
        if len(moves) > 0:
            state = rand.sample(moves, 1)[0]
            unused.extend(moves)
        else:
            state = rand.sample(unused, 1)[0]
    return state

def getPath(node):
    path = [node]
    while len(node["children"]) > 0:
        node = sorted(node["children"], key=lambda x: x["heuristic"])[0]
        path.append(node)
    return path

def getRandomNodes(root, data, numNodes, rand):
    nodes = sorted(rand.sample(root["allNodes"], numNodes), key=lambda x: x["index"])
    for i in range(numNodes):
        node = nodes[i]
        data["n" + str(i + 1)] = "N" + str(node["index"])
        data["h" + str(i + 1)] = node["heuristic"]

def drawNode(outDir, node):
    if outDir == None:
        return
    graph = "digraph G {\n"
    graph += "concentrate=True;\n"
    graph += "rankdir=TB;\n"
    graph += "node [shape=record, margin=0];\n"
    graph += "{\n"
    graph += nodeToString(node, False)


# Question Generation #########################################################

def sliding(options):
    heuristic = "OOP"
    numSteps = 2
    seed = options["seed"]
    rand = random.Random(seed)
    assert heuristic in HEURISTICS
    data = {"heuristic":HEURISTICS[heuristic]["desc"]}
    initial = shuffle([[1, 2, 3], [4, 5, 6], [7, 8, 0]], numSteps, rand)
    root, graph = build(initial, numSteps, HEURISTICS[heuristic]["func"])
    data["path"] = ",".join(["N" + str(x["index"]) for x in getPath(root)])
    getRandomNodes(root, data, 3, rand)
    if options["outDir"] != None:
        odir = options["outDir"]
        with open(os.path.join(odir, "SlidingPuzzleTree.dot"), "wt") as f:
            f.write(graph["source"])
        cmd = "dot -Tpng " + os.path.join(odir, "SlidingPuzzleTree.dot") + " -o " + os.path.join(odir, "SlidingPuzzleTree.png")
        print("Running", cmd)
        os.system(cmd)
    return data