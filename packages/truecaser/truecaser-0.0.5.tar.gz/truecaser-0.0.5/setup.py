
from setuptools import setup

setup(
	name="truecaser",
	version="0.0.5",
	description="Predict and restore word casing",
	py_modules=[
		"truecaser",
		"case",
		"interface",
	],
	package_dir={"": "truecaser"},
	classifiers=[
		'Programming Language :: Python :: 3',
	]
)


