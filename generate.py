from exgen.generate import generate

if __name__=="__main__":
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