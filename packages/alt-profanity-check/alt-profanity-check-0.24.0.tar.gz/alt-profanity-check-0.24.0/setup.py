import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="alt-profanity-check",
  version="0.24.0",
  author="Victor Zhou (original author), Menelaos Kotoglou, Dimitrios Mistriotis",
  author_email="dimitrios@mistriotis.com",
  description=(
    'Dropdown replacement of "profanity-check", '
    'A fast, robust library to check for offensive language in strings.'),
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://gitlab.com/dimitrios/alt-profanity-check/",
  packages=setuptools.find_packages(),
  install_requires=["scikit-learn==0.24.0", "joblib>=1.0.0"],
  package_data={'profanity_check': ['data/model.joblib', 'data/vectorizer.joblib']},
  classifiers=[
    "Development Status :: 5 - Production/Stable",
    "Natural Language :: English",
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
)
