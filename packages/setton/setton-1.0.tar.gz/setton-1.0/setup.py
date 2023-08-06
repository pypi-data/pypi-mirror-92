import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="setton",
    version="1.0",
    author="Rafael Setton",
    author_email="rasealca2017@gmail.com",
    description="Algumas Funções úteis para diversas coisas",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RafaelSetton/setton",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
