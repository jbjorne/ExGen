import plot_iris_knn
import svm
import perceptron
import mlp
import tree
import network
import common
import titanic
import spam
import clustering
import md
import convolution
import wordvec
import json
import os
import features
import examnet
import examconvolution

# def generateExamples(examples):
#     for example in examples:
#         if example == "knn":
#             plot_iris_knn.generateKNN()
#         elif example == "kmeans":
#             plot_iris_knn.generateKMeans()
#         elif example == "subset":
#             common.makeIrisFigure("figures/subset_three_classes.png", colors=['#1f77b4', '#2ca02c', '#ff7f0e'])
#             common.makeIrisFigure("figures/subset_two_classes.png", colors=['#1f77b4', 'white', '#ff7f0e'])
#             common.makeIrisFigure("figures/baseline_two_classes.png", classes=["setosa", "virginica"], colors=['#1f77b4', 'white', '#ff7f0e'])
#         elif example == "svm":
#             svm.plotSVM("figures/svm.png")
#             svm.plotSVM("figures/svm_predicted.png", True)
#         elif example == "perceptron":
#             perceptron.plotPerceptron("figures/perceptron/perceptron")
#         elif example == "mlp":
#             mlp.plotMLP("figures/mlp.png")
#         elif example == "tree":
#             tree.plotTree("figures/tree")
#         elif example == "irisnet":
#             network.makeIrisExample("figures/networkIris")
#         else:
#             raise Exception("Unknown example " + str(example))

# def getStem(name, mode, modeTags):
#     return name + "-" + modeTags[mode]

def generateExercise(exercises, instructions, format, modes, modeTags, variants=1):
    assert format in ("moodle", "latex", "exam")
    
    for exercise in exercises:
        print("*** Generating exercise", exercise)
        options = {"imageFormat":"png" if not "latex" else "pdf", "format":format}
        options["outDir"] = format
        content = []
        if instructions:
            content.append(md.parse("ohjeet.md"))
        if exercise == "luento6":
            options["title"] = "Luento 6 (Johdatus koneoppimiseen): Tehtävät"
            content.append(spam.makeSpamExercise(options, format))
            content.append(clustering.makeClusteringExercise(options, format))
        elif exercise == "luento7":
            options["title"] = "Luento 7 (Koneoppimisen menetelmiä): Tehtävät"
            network.makePerceptronInfo(format + "/perceptronInfo", options)
            network.makePerceptronWeights(format + "/perceptronWeights", options)
            network.makePerceptronWeights2(format + "/perceptronWeights2", options)
            network.makePerceptronNot(format + "/perceptronNot", options)
            network.makeNetworkXor(format + "/networkXor", options)
            content.append(md.parse("network.md"))        
            content.append(titanic.makeTitanicExercise(options, format=format))
        elif exercise == "luento8":
            options["title"] = "Luento 8 (Syväoppiminen): Tehtävät"
            content.append(md.parse("deeplearning.md"))
            content.append(convolution.makeConvolution(format + "/convolution", options))
            content.append(wordvec.makeWordVec(format + "/wordvec"))
        elif exercise == "exam":
            options["title"] = "Tentti"
            stem = format + "/features"
            for i in range(variants):
                content.append(features.makeFeatureExercise(i))
            
            #content.append(convolution.makeConvolution(format + "/convolution", options))
            #content.append(wordvec.makeWordVec(format + "/wordvec"))
        elif exercise == "examnet":
            options["title"] = "Neuroverkot"
            content.append(examnet.makeNetwork(options))
        elif exercise == "examconvolution":
            options["title"] = "Konvoluutio"
            content.append(examconvolution.makeConvolution(options))
        elif exercise == "schoolexam":
            options["title"] = "Tentti"
            data = {}
            data.update(examconvolution.makeConvolution(options)["data"])
            data.update(features.makeFeatureExercise(1)["data"])
            content.append(md.parse("schoolexam.md", data))
        else:
            raise Exception("Unknown exercise " + str(exercise))
        
        for mode in modes:
            print("Generating output for", mode)
            options["mode"] = mode
            options["answers"] = mode in ("answers", "solutions")
            options["fileStem"] = os.path.join(format, exercise + "-" + modeTags[mode])
            md.renderDoc(content, options)

def getNames(s):
    return [x.strip() for x in s.split(",") if x.strip() != ""]

def generate(inPath, dataPath, scriptPath, outPath, outFormat):


if __name__=="__main__":
    from optparse import OptionParser
    optparser = OptionParser()
    optparser.add_option("-i", "--input", default=None, help="The input file in Markdown format")
    optparser.add_option("-d", "--data", default=None, help="A data file in JSON format")
    optparser.add_option("-o", "--output", default=None, help="The output file stem")
    optparser.add_option("-f", "--format", default="latex")
    (options, args) = optparser.parse_args()

    #generateExamples(getNames(options.examples))
    generateExercise(getNames(options.exercises), options.instructions, options.format, options.modes.split(","), json.loads(options.modeTags), variants=options.variants)