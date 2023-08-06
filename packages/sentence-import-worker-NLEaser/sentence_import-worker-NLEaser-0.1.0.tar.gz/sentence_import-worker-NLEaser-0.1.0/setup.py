from git import Repo
from setuptools import setup, find_packages


def get_version():
    rep = Repo("../../")
    tags = rep.tags
    version = tags[-1]
    return str(version)


setup(
    name="sentence_import-worker-NLEaser",
    version=get_version(),
    description="Consumer do rabbit para realizar a importação e o preprocessamento "
                "das sentenças",
    author="Mateus Michels de Oliveira, Lucas Domiciano",
    author_email="michels09@hotmail.com, lucas2809@live.com",
    python_requires=">=3.6",
    install_requires=[
        "marshmallow==3.7.1",
        "mongoengine==0.20.0",
        "nltk==3.4.4",
        "pika==1.1.0",
        "pandas==1.1.5"
    ],
    packages=find_packages(
        where="../../../NLEaser_v2",
        exclude=["api*"]
    ) + ["workers.sentence_import"],
    package_dir={"": "../../../NLEaser_v2"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ]
)
