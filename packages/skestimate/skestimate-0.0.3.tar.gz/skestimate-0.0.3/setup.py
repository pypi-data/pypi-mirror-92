"""
This package is used to fit and get various metrics for a multi class classifier. It is based on scikit-learn library and uses the methods from that library.

fit_est module inside the package has a class named Xest(self, estimator, data, target_label, ts).
* estimator: A piplined classifier that encodes all the categorical features.
* data: Raw dataset including the target label
* target_label: A string type representing the name of the target label
* ts: A number between 0 and 1 that specifies the test portion of the data.
"""
import setuptools
REQUIRED = [
    "numpy",
    "pandas",
    "matplotlib",
    "scikit-learn"
]
with open("./skestimate/README.md", "r") as file:
    LONG_DESCRIPTION = file.read()
setuptools.setup(
    name="skestimate",
    version="0.0.3",
    author="skhabiri",
    description="fit estimate utility",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/skhabiri/EstimatorPkg",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=REQUIRED,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
