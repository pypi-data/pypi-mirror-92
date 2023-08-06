import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mcd-state-client",
    version="0.0.0",
    author="Andy McCall",
    author_email="andymc903@gmail.com",
    description="An mcdstate.info API wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tamccall/mcd-state-client",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
