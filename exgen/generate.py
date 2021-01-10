import os
from .renderer import md
import importlib

def getExercises(exercises):
    if exercises != None:
        exercises = exercises.split(",")
    return exercises

def execScript(function, scriptPath, seed):
    data = None
    if os.path.exists(scriptPath):
        print("Running script", scriptPath)
        with open(scriptPath) as f:
            code = compile(f.read(), scriptPath, 'exec')
        scriptGlobals = {}
        exec(code, scriptGlobals)
        data = eval(function + "(" + str(seed) + ")", scriptGlobals)
    return data

def generate(inDir, exercises, outStem, outFormat, mode, seed):
    if (inDir == None):
        inDir = "examples"
    assert os.path.exists(inDir)
    content = []
    exercises = getExercises(exercises)
    for i in range(len(exercises)):
        exercise = exercises[i]
        print("-----", "Processing exercise", str(i+1) + "/" + str(len(exercises)), "'" + exercise + "'", "-----")
        mdPath = os.path.join(inDir, exercise + ".py")
        print("Reading exercise from", mdPath)
        data = execScript(exercise, mdPath, seed)
        content.append(md.parse(os.path.join(inDir, exercise + ".md"), data))
    
    options = {}
    options["mode"] = mode
    options["format"] = outFormat
    options["answers"] = mode in ("answers", "solutions")
    options["template"] = "templates/template.tex"
    options["fileStem"] = outStem
    md.renderDoc(content, options)