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

Some scripts use a seed value parameter, which can be used to initialize a random number generator. The seed value can be defined with the -s switch.

## Defining variables

Questions are written using Markdown text where variables computed by the associated Python script can be inserted using the link syntax `[value](type)`. If the `value` is a variable name found in the dictionary returned by the Python script, it is replaced by the value in the dictionary. Variables do not need to be typed, but several types are supported.

### Answers

The type `answer` marks the variable as an answer which supports different answer types. The answer can be a simple string or number, or it can be a multiple choice question. Multiple choice answers can be defined as a semicolon-separated list (CSV) or as a JSON list or dictionary.

### Solutions

The types `solution:begin` and `solution:end` can be used to enclose a solution section which can be revealed to the students only after the exam.

### Tables

Tables can be defined as named variables produced by the script. A table is defined as a dictionary object with the key `type` set as `table`. The `rows` of the table can be defined either as a list of lists or dictionaries. Answers can be embedded in tables as dictionary objects with the `type` set as `answer` and the `value` as the answer value.

## Advanced usage

Writing a more complex exercise is demostrated in the included "features" example. In this exercise students of a machine learning course construct feature vectors from a dataset and calculate nearest neighbour distances between these vectors. The example demonstrates how to write complex, multi-stage exercises.