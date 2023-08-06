import setuptools

#with open("latex/README.md", "r") as fh:
#    long_description = fh.read()

setuptools.setup(
    name="TarikDrevonUtils",
    version="1.0.1",
    author="Tarik Ronan Drevon",
    author_email="ronandrevon@gmail.com",
    description="some display utilities",
    long_description='', #long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License ",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'matplotlib','numpy','scipy','colorama','pandas','pillow'],
)
