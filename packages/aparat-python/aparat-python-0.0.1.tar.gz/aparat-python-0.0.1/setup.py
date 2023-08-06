import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aparat-python",
    version="0.0.1",
    author="Mahdi Khashan",
    author_email="mahdikhashan1@gmail.com",
    description="Aprat VOD platform rest api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mahdikhashan/aparat-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)