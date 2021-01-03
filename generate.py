import os
import md
import importlib

def getExercises(exercises):
    if exercises != None:
        exercises = exercises.split(",")
    return exercises

def generate(inDir, exercises, outStem, outFormat, mode):
    assert os.path.isdir(inDir)
    content = []
    exercises = getExercises(exercises)
    for exercise in exercises:
        print("Reading exercise", exercise)
        data = None
        scriptPath = os.path.join(inDir, exercise + ".py")
        if os.path.exists(scriptPath):
            with open(scriptPath) as f:
                code = compile(f.read(), scriptPath, 'exec')
            scriptGlobals = {}
            exec(code, scriptGlobals)
            data = eval(exercise + "()", scriptGlobals)
        content.append(md.parse(os.path.join(inDir, exercise + ".md"), data))
    
    options = {}
    options["mode"] = mode
    options["format"] = outFormat
    options["answers"] = mode in ("answers", "solutions")
    options["template"] = "templates/template.tex"
    options["fileStem"] = outStem
    md.renderDoc(content, options)

if __name__=="__main__":
    from optparse import OptionParser
    optparser = OptionParser()
    optparser.add_option("-i", "--input", default=None, help="The input directory")
    optparser.add_option("-e", "--exercises", default=None, help="Exercise names to include")
    optparser.add_option("-o", "--output", default=None, help="The output file stem")
    optparser.add_option("-f", "--format", default="latex")
    optparser.add_option("-m", "--mode", default="solutions", help="'questions', 'answers' or 'solutions'")
    (options, args) = optparser.parse_args()

    generate(options.input, options.exercises, options.output, options.format, options.mode)