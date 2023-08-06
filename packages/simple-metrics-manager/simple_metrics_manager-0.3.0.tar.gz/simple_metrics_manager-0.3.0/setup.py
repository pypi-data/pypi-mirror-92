from setuptools import setup

# Read the version number
with open("simple_metrics_manager/_version.py") as f:
    exec(f.read())

setup(
    name="simple_metrics_manager",
    version=__version__,  # use the same version that's in _version.py
    author="David N. Mashburn",
    author_email="david.n.mashburn@gmail.com",
    packages=["simple_metrics_manager"],
    scripts=[],
    url="http://pypi.python.org/pypi/simple_metrics_manager/",
    license="LICENSE.txt",
    description="Just a simple system to manage a set of metrics (string name / function / returned data) that supports caching (memory and disk)",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=["human_time_formatter >= 1.0.0.6"],
)
