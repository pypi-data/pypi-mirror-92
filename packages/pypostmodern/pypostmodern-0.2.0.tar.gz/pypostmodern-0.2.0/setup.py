import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pypostmodern",
    version="0.2.0",
    author="Zvi Bazak",
    author_email="",
    description="Prepare your Python code to the postmodernism era!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zvibazak/pypostmodern",
    packages=setuptools.find_packages(),
    classifiers=[
    ],
    python_requires='>=3.6',
)