import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mini-tic-tac-toe",
    version="0.0.1",
    description="Library to play Tic Tac Toe",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MesterLum/tic-tac-toe",
    author="Eduardo Cuauhtémoc Paez Palafox",
    author_email="mesterlum@hotmail.com",
    packages=setuptools.find_packages(),
    install_requires=[],
    license='MIT',
)
