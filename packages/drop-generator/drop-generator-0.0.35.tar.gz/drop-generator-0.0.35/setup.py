import pathlib
from setuptools import setup


# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="drop-generator",
    version="0.0.35",
    description="RPG Loot Drop Engine",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Mascha Loomis",
    author_email="mascha.loomis@gmail.com",
    license="MIT",
    url="https://gitlab.com/ramencatz/python-loot",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Games/Entertainment",
        "Topic :: Games/Entertainment :: Role-Playing",
        "Topic :: Utilities"
    ],
    packages=["dropgen"],
    key_words='loot rpg utility',
    include_package_data=True,
    install_requires=[],
    python_requires='>=3',
    
)