import random
from exgen.examples.features import ValidationError
import sys, os
from .src import md
import importlib
import pathlib

def getExercises(exercises, inDir):
    if exercises != None:
        exercises = exercises.split(",")
    else:
        exercises = []
        for filename in os.listdir(inDir):
            if filename.endswith(".md"):
                exercises.append(filename.rsplit(".", 1)[0])
        exercises.sort()
    return exercises

def execScript(function, scriptPath, options):
    data = None
    if os.path.exists(scriptPath):
        print("Running script", scriptPath)
        with open(scriptPath) as f:
            code = compile(f.read(), scriptPath, 'exec')
        scriptDir = os.path.dirname(scriptPath)
        if scriptDir not in sys.path:
            sys.path.append(scriptDir)
        scriptGlobals = {}
        exec(code, scriptGlobals)
        #data = eval(function + "(" + str(seed) + ")", scriptGlobals)
        data = None
        scriptOptions = options.copy()
        seedRand = random.Random()
        exceptions = []
        while data is None and len(exceptions) < 10:
            try:
                data = scriptGlobals[function](scriptOptions)
                data["variant"] = "#" + str(scriptOptions["seed"])
            except ValidationError as e:
                exceptions.append(e)
                scriptOptions["seed"] = seedRand.randrange(0, 1000000000)
        print(data, exceptions)
    return data

def generate(inDir, exercises, outDir, outFormat, mode, seed):
    fileDir = os.path.join(pathlib.Path(__file__).parent.absolute())
    if not os.path.exists(outDir):
        print("Making output directory", outDir)
        os.makedirs(outDir)

    options = {}
    options["mode"] = mode
    options["format"] = outFormat
    options["answers"] = mode in ("answers", "solutions")
    options["template"] = os.path.join(fileDir, "templates", "template.tex")
    options["outDir"] = outDir
    options["seed"] = seed

    if inDir is None:
        inDir = os.path.join(fileDir, "examples")
    if not os.path.exists(inDir):
        raise Exception("Input directory " + str(inDir) + " not found")
    exercises = getExercises(exercises, inDir)
    print("Processing exercises", exercises, "from directory", inDir)
    for i in range(len(exercises)):
        content = []
        exercise = exercises[i]
        print("-----", "Processing exercise", str(i+1) + "/" + str(len(exercises)), "'" + exercise + "'", "-----")
        options["exercise"] = exercise
        scriptPath = os.path.join(inDir, exercise + ".py")
        print("Reading exercise from", scriptPath)
        data = execScript(exercise, scriptPath, options)
        content.append(md.parse(os.path.join(inDir, exercise + ".md"), data))
        md.renderDoc(content, options)

def main():
    from optparse import OptionParser
    optparser = OptionParser()
    optparser.add_option("-i", "--input", default=None, help="The input directory. If not given the built-in examples directory is used.")
    optparser.add_option("-e", "--exercises", default=None, help="Exercise names to include. If not given all exercises from the directory are included.")
    optparser.add_option("-o", "--output", default=None, help="The output directory")
    optparser.add_option("-f", "--format", default="latex", help="One of 'latex', 'moodle' or 'exam'")
    optparser.add_option("-s", "--seed", default=1, type=int, help="Random number generator seed for randomizing the exercises")
    optparser.add_option("-m", "--mode", default="solutions", help="One of 'questions', 'answers' or 'solutions'")
    (options, args) = optparser.parse_args()

    generate(options.input, options.exercises, options.output, options.format, options.mode, options.seed)