# Armazenar todas as Informações necessárias para o pypi ultilizar na publicaçãodo seu pacote
from setuptools import setup, find_packages
from pathlib import Path

setup(
    name='pro_music_player',
    version=1.0,
    description='Este pacote fornecerá ferramentas de áudio',
    long_description=Path('README.md').read_text(),
    author='João Victor Júlio',
    author_email='julio.guerra.dev@gmail.com',
    keywords=['audio', 'ondas sonoras', 'processamento', 'graves'],
    packages=find_packages()
)