import io
import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, "README.rst"), "rt", encoding="utf8") as f:
    readme = f.read()


setup(
    name="tutor-minio",
    version="0.0.1",
    url="https://docs.tutor.overhang.io/",
    project_urls={
        "Documentation": "https://docs.tutor.overhang.io/",
        "Code": "https://github.com/regisb/tutor/tree/master/plugins/minio",
        "Issue tracker": "https://github.com/regisb/tutor/issues",
        "Community": "https://discuss.overhang.io",
    },
    license="AGPLv3",
    author="Régis Behmo",
    author_email="regis@behmo.com",
    description="A Tutor plugin for object storage in MinIO",
    long_description=readme,
    packages=["tutorminio"],
    include_package_data=True,
    python_requires=">=3.5",
    install_requires=["click>=7.0"],
    entry_points={"tutor.plugin.v0": ["minio = tutorminio.plugin"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
