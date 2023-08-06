from setuptools import setup, find_packages
from distutils.cmd import Command
import os

install_requirements = [i.replace('\n','') for i in open('./requirements.txt').readlines()]

classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

class TorchInstall(Command):
    description = 'Install torch from the website'
    user_options = []

    def initialize_options(self):
        pass

    # This method must be implemented
    def finalize_options(self):
        pass

    def run(self):
        os.system('pip install torch==1.5.0+cpu --find-links https://download.pytorch.org/whl/torch_stable.html')

setup(
    name = 'bert-embeddings',
    version = '0.0.3',
    description = 'Create positional embeddings based on TinyBERT or similar bert models',
    long_description = 'Bert Embeddings\n Use this library to really easily embed text using Bert Models.\n\n Github: https://github.com/sorcely/BertEmbeddings ' + '\n\n' + open('CHANGELOG.txt').read(),
    url = 'https://github.com/Sorcely/EmbeddingsLib',
    author = 'Marius J. Schlichtkrull',
    author_email = 'marius.schlichtkrull@gmail.com',
    license = 'MIT',
    classifiers = classifiers,
    keywords = 'embeddings',
    packages = find_packages(),
    install_requires = install_requirements,
    cmdclass = {'install_torch': TorchInstall}
)
