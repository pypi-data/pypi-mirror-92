from setuptools import setup

with open("README.md", "r", encoding="utf8", errors="ignore") as f:
	long_description = f.read()

setup(
	name="sentenceninja",
	packages=['sentenceninja'],
	version="0.1",
	description="To split paragraphs into individual sentences",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/iamarkaj/sentenceninja",
	author="Arkajyoti Basak",
	author_email="arkajbasak1211@gmail.com",
	license="MIT",
	classifiers=[
		"Topic :: Scientific/Engineering",
		"License :: OSI Approved :: MIT License",
		"Programming Language :: Python :: 3",
		],
	keywords="split sentences",
	)
