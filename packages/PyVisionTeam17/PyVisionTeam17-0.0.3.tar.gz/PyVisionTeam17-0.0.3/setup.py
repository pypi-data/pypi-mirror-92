from setuptools import setup
with open("ReadMe.md","r") as fh:
    long_description = fh.read()
setup(
    name = 'PyVisionTeam17',
    version = '0.0.3',
    description = 'Deep Learning Framework',
    py_modules = ["activations","CNN","Datamodule","Evaluation","function","functional","layer","linear","losses","model","net","optimizer","Utils","Visualization"],
    package_dir = {'':'src'},
    install_requires = [
        "matplotlib <= 3.1.3",
        "pillow <= 8.0.1",
        "numpy <= 1.17.5",
        "pandas <= 0.25.1",
    ],
    long_description = long_description,
    long_description_content_type = "text/markdown",
    license="MIT",
    url="https://github.com/HendMuhmmad/Deep-Learning-Framework",
)