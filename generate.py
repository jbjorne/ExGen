import md

def generate(inPath, dataPath, scriptPath, outStem, outFormat, mode):
    content = md.parse(inPath)
    options["mode"] = mode
    options["answers"] = mode in ("answers", "solutions")
    options["fileStem"] = os.path.join(outStem)
    md.renderDoc(content, options)

if __name__=="__main__":
    from optparse import OptionParser
    optparser = OptionParser()
    optparser.add_option("-i", "--input", default=None, help="The input file in Markdown format")
    optparser.add_option("-d", "--data", default=None, help="A data file in JSON format")
    optparser.add_option("-o", "--output", default=None, help="The output file stem")
    optparser.add_option("-f", "--format", default="latex")
    optparser.add_option("-m", "--mode", default="solutions", help="'questions', 'answers' or 'solutions'")
    (options, args) = optparser.parse_args()

    generate()