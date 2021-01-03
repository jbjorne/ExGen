import os
import md

def generate(inDir, exercises, outStem, outFormat, mode):
    assert os.path.isdir(inDir)
    content = []
    for exercise in exercises:
        content.append(md.parse(os.path.join(inDir, exercise)))
        pyPath = os.path.join(inDir, exercise + ".py")
        if os.path.exists(pyPath):
            pass
    
    options["mode"] = mode
    options["answers"] = mode in ("answers", "solutions")
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