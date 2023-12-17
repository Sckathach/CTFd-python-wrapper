from setuptools import setup, find_packages

setup(
    name="wrapper",
    version="0.2.1",
    author="Sckathach",
    author_email="sckathach@hackademint.org",
    description="A simple python wrapper for the CTFd API",
    packages=find_packages(),
    install_requires=[
        "black==23.11.0",
        "certifi==2023.11.17",
        "charset-normalizer==3.3.2",
        "click==8.1.7",
        "idna==3.4",
        "mypy-extensions==1.0.0",
        "packaging==23.2",
        "pathspec==0.11.2",
        "platformdirs==4.0.0",
        "python-dotenv==1.0.0",
        "requests==2.31.0",
        "urllib3==2.1.0",
    ],
    classifiers=[],
    python_requires=">=3.6",
)
