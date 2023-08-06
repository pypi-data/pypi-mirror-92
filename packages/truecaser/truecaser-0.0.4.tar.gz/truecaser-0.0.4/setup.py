
from setuptools import setup

setup(
	name="truecaser",
	version="0.0.4",
	description="Predict and restore word casing",
	py_modules=[
		"truecaser",
		"case"
	],
	package_dir={"": "truecaser"},
	classifiers=[
		'Programming Language :: Python :: 3',
	]
)


