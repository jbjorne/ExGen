# Exercise Generator

This program is a sample implementation of the method proposed in "A platform-independent solution for creating complex exercises and online exams for popular learning management systems".

## Installing

## Basic usage

If the package has not been installed, go to the subdirectory "exgen" for running the following commands:

If no input directory is defined, the built-in sample directory is used. To generate a Latex version of a very simple exercise, run the following command:

python generate.py -e velocity -o /path/stem

where the -o switch defines the stem (filename without the extension) for the output files. Once you run the program, it generates a file /path/stem.tex. You can compile this file into PDF format by using e.g. the pdflatex command line program.

To get an overview of the program options, run generate.py with the --help switch.