from setuptools import setup, find_packages
from pip.req import parse_requirements

install_reqs = parse_requirements("requirements.txt")
reqs = [str(i.req) for i in install_reqs]

setup(
    name="lego_rest_api",
    version="0.0.1",
    description="python stuff for a practical course",
    author="Markus Grotz",
    author_email="markus.grotz@kit.edu",
    url="http://gitlab.com/markusgrotz/lego_rest_api",
    install_requires=reqs,
    packages=find_packages(exclude=["tests"])
)
