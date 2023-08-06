from setuptools import find_packages, setup

setup(
    name="django_dnoticias_services",
    version='1.0.5',
    url="https://www.dnoticias.pt/",
    author="Pedro Mendes",
    author_email="pedro.trabalho.uma@gmail.com",
    license="MIT",
    install_requires=[
        'requests',
        'django'
    ],
    packages=find_packages(),
)
