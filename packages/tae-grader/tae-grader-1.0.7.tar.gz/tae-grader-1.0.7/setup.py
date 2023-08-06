import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

# get version
env = {}
with open("taeg/version.py") as f:
	exec(f.read(), env)
version = env["__version__"]

setuptools.setup(
	name = "tae-grader",
	version = version,
	author = "TAE Developers",
	author_email = "master@taecoding.com",
	description = "Python and Jupyter Notebook autograder",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	license = "BSD-3-Clause",
	packages = setuptools.find_packages(exclude=["test"]),
	classifiers = [
		"Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
	],
	install_requires=[
		"pyyaml", "nbformat", "ipython", "nbconvert<6.0.0", "tqdm", "setuptools", "pandas", "tornado",
		"docker", "jinja2", "dill", "pdfkit", "PyPDF2"
	],
	scripts=["bin/taeg"],
	package_data={
		"taeg.service": ["templates/*.html"], 
		"taeg.export.exporters": ["templates/*"],
		"taeg.generate": ["templates/*"],
	},
)
