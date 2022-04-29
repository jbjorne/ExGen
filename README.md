# Exercise Generator

This program is a sample implementation of the method proposed in "Striving for platform independence in the e-learninglandscape: a study on a flexible exercise creationsystem". The program parses one or more exercises from Markdown files, and optionally their associated Python or JSON files, and outputs them in formats usable in online Learning Management Systems or as PDF for offline use.

## Installing

The package can be installed using the command:

`python setup.py install --user`

This installs the package and the exgen command line tool.

## Basic usage

If the package has not been installed please use `python exgen.py` in place of `exgen` in the following examples.

The input exercises are defined with the directory (-i) and the exercises (-e) options. If no input directory is defined, the built-in sample directory is used. To generate a Latex version of a very simple example exercise, run the following command:

`exgen -e velocity -o output_directory`

The -o switch defines the directory for the output files. If the directory doesn't exist, it will be made. The exercises are written to the output directory with the chosen format. For example, if the latex format is used, the above command will generate the output file `output_directory/velocity.tex`. This output file can be compiled into PDF format by using the pdflatex program.

To get an overview of the program options, run exgen with the --help switch.

## Output formats

Different output formats (such as Moodle) can be chosen with the format (-f) switch. The mode switch (-m) is used to define whether correct answers and solutions are shown in the output format.

## Randomizing exercises

Exercise scripts take a seed value parameter, which can be used to initialize a random number generator. The seed value can be defined with the -s switch.

## Advanced usage

Writing a more complex exercise is demostrated in the included "features" example. In this exercise students of a machine learning course construct feature vectors from a dataset and calculate nearest neighbour distances between these vectors. The example demonstrates how to write complex, multi-stage exercises.