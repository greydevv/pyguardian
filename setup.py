from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
	long_description = fh.read()

setup(
	name="pyguard",
	version="0.0.1",
	author="Greyson Murray",
	author_email="greysonmurray.dev@gmail.com",
	maintainer="Greyson Murray",
	maintainer_email="greysonmurray.dev@gmail.com",
	description="pyguard simplifies parameter type validation",
	long_description=long_description,
	url="https://github.com/greysonDEV/pyguard",
	packages=["pyguard"],
	classifiers=[
		"Programming Language :: Python",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
		"Programming Language :: Python :: 3.9",
		"Operating System :: MacOS :: MacOS X",
		"Operating System :: Microsoft :: Windows",
		"Topic :: Software Development",
		"License :: OSI Approved :: MIT License",
	],
	python_requires=">=3.6",
	extras_require={
		"dev":[
			"pytest=6.1.2"
		]
	}
)