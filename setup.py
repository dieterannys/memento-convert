from setuptools import setup, find_packages


setup(
    name="memento_convert",
    version="0.1.0",
    packages=find_packages(where="./src"),
    package_dir={"": "src"},
    install_requires=["pandas"],
    entry_points={"console_scripts": ["memento-convert = memento_convert.main:main"]},
)
