import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="pypolarity", # Replace with your own username
    version="0.0.3",
    author="sumeth",
    author_email="author@example.com",
    description="analyze news article as positive or negative",
    long_description=README,
    long_description_content_type="text/markdown",
    url="",
    packages=['pypolarity'],
    license='MIT',
    include_package_data=True,
    install_requires= [
        'numpy',
        'cut-sent-thai >= 0.0.4',
        'pythainlp >= 2.2.0',
        'ujson'
        ],
    python_requires='>=3.6',
    zip_safe=False
)