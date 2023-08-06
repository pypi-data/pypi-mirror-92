from setuptools import setup
from setuptools import find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

packages = find_packages()

setup(
    name="mvnproxy",
    version="1.1.0",
    description="mvnproxy",
    long_description=readme,
    author="Bogdan Mustiata",
    author_email="bogdan.mustiata@gmail.com",
    license="BSD",
    entry_points={"console_scripts": ["mvnproxy = mvnproxy.mainapp:main"]},
    install_requires=[
        "requests==2.25.1",
        "termcolor_util",
        "fastapi==0.63.0",
        "uvicorn[standard]==0.11.8",
        "aiofiles==0.6.0",
    ],
    packages=packages,
    package_data={
        "": ["*.txt", "*.rst"],
        "mvnproxy": ["py.typed"],
    },
)
