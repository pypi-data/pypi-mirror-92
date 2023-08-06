
from setuptools import setup

with open("README.md", "r") as _file:
    long_description = _file.read()

setup(
	name="truecaser",
	version="0.0.6",
	description="Predict and restore word casing",
	py_modules=[
		"truecaser",
		"case",
		"interface",
	],
	package_dir={"": "truecaser"},
	classifiers=[
		'Programming Language :: Python :: 3',
	],
	long_description=long_description,
	long_description_content_type="text/markdown"
)

