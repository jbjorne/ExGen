import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="exgen",
    version="1.0.0",
    author="",
    author_email="",
    description="An exercise generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    entry_points={'console_scripts':['exgen = exgen.generate:main']}, 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    #include_package_data=True,
    #package_data={'exgen': ['exgen/examples/*', 'exgen/template/*']},
    data_files=[('exgen/examples', 
        ['exgen/examples/velocity.md',
        'exgen/examples/velocity.py',
        'exgen/examples/features.md',
        'exgen/examples/features.py']), 
        ('exgen/templates', ['exgen/templates/template.tex'])],
    python_requires='>=3.6',
)