import os
from .renderer import md
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
        inDir = os.path.join(pathlib.Path(__file__).parent.absolute(), "examples")
    if not os.path.exists(inDir):
        raise Exception("Input directory " + str(inDir) + " not found")
    content = []
    exercises = getExercises(exercises, inDir)
    print("Processing exercises", exercises, "from directory", inDir)
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

def main():
    from optparse import OptionParser
    optparser = OptionParser()
    optparser.add_option("-i", "--input", default=None, help="The input directory")
    optparser.add_option("-e", "--exercises", default=None, help="Exercise names to include")
    optparser.add_option("-o", "--output", default=None, help="The output file stem")
    optparser.add_option("-f", "--format", default="latex")
    optparser.add_option("-s", "--seed", default=0, type=int)
    optparser.add_option("-m", "--mode", default="solutions", help="'questions', 'answers' or 'solutions'")
    (options, args) = optparser.parse_args()

    generate(options.input, options.exercises, options.output, options.format, options.mode, options.seed)