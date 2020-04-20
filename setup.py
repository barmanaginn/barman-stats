import os

from setuptools import find_packages, setup

try:
    with open(
        os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8"
    ) as f:
        long_description = f.read()
except:
    long_description = None

setup(
    name="barman-stats",
    version=0.1,
    description="Add some statistics to BarMan",
    long_description=long_description,
    author="Yoann Pietri",
    author_email="me@nanoy.fr",
    url="https://github.com/barmanaginn/barman-stats",
    license="GPLv3",
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    entry_points="""
[barman.plugin]
barman_stats=barman_stats:BarmanPluginMeta
""",
)
