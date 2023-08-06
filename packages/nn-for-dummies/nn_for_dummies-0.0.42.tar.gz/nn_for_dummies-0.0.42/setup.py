from setuptools import setup

with open("./NN-FRAMEWORK-FOR-DUMMIES/README.md","r") as fh:
    long_description = fh.read()
setup(
    name = "nn_for_dummies",
    version = '0.0.42',
    description = 'a small classfication neural network framework',
    py_modules  =['Activations','DataPreProcessing','Losses','nn','optimization','save_load','visualization'],
    package_dir = {'':'NN-FRAMEWORK-FOR-DUMMIES'},
    classifiers = ["Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Operating System :: OS Independent"
    ],
    long_description = long_description,
    long_description_content_type = "text/markdown",
)