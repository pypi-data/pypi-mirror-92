from setuptools import setup

setup(
    name='pyray2',
    version='0.0.4',
    description='Mini Neural Network Library',
    py_modules=["abstract_classes","activations", "cnn", "dataset", "evaluation", "Linear", "loss", "model", "optim", "utils", "visualize"],
    package_dir={'':'src'},
    install_requires = [
        "numpy",
        "matplotlib",
        "pandas"
    ],
    url="https://github.com/AmrElsersy/DL-Framework",
    author = "mamoanwar97",
    author_email= "1601323@eng.asu.edu.eg"
)
