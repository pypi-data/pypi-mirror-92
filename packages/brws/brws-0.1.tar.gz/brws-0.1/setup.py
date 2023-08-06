import subprocess
import sys
from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install

with open('README.md', 'r') as f:
    long_description = f.read()

with open('requirements.txt', 'r') as f:
    requirements = f.readlines()


class PostDevelopCommand(develop):
    def run(self):
        develop.run(self)
        download_embeddings('en_core_web_sm')


class PostInstallCommand(install):
    def run(self):
        install.run(self)
        download_embeddings('en_core_web_sm')


def download_embeddings(embeddings):
    subprocess.check_call(
        [sys.executable, "-m", "spacy", "download", embeddings]
    )


setup(
    name='brws',
    version='0.1',
    author='Ingo Fruend',
    author_email='github@ingofruend.net',
    descriptions='Content based browsing documents',
    long_description=long_description,
    url='',
    install_requires=requirements,
    scripts=['brws'],
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    }
)
