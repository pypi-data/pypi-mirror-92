from setuptools import setup


def readme():
    with open("README.md") as f:
        return f.read()


# def license():
#     with open('LICENSE') as f:
#         return f.read()


setup(
    name="funpdbe-validator",
    version="1.0.1",
    description="Validate PDBe-KB JSONs by FunPDBe Schema",
    long_description_content_type='text/markdown',
    long_description=readme(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    keywords="json validator",
    url="https://github.com/PDBe-KB/funpdbe-validator",
    author="Mihaly Varadi",
    author_email="mvaradi@ebi.ac.uk",
    license_file="LICENSE",
    packages=["validator"],
    install_requires=["jsonschema", "requests"],
    test_suite="tests",
    tests_require=["pytest", "pytest-cov"],
    include_package_data=True,
    zip_safe=True,
    python_requires='>=3.6',
)
