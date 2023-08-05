import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py_headless_daw", # Replace with your own username
    version="0.0.1",
    author="Sergey Grechin",
    author_email="grechin.sergey@gmail.com",
    description="A GUI-less DAW (Digital Audio Workstation) for producing electronic music using python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hq9000/py_headless_daw",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)