from distutils.core import setup
import setuptools

setup(
    name='tutorialpypi',  # How you named your package folder (MyLib)
    packages=setuptools.find_packages(),  # Chose the same as "name"
    version='0.4',  # Start with a small number and increase it with every change you make
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='Tutorial for a new package',  # Give a short description about your library
    author='Gonzalo Mazzini',  # Type in your name
    author_email='gmazzini@itba.edu.ar',  # Type in your E-Mail
    url='https://github.com/GonMazzini/tutorialpypi/releases/tag/v0.4',  # Provide either the link to your github or to your website
    download_url='https://github.com/GonMazzini/tutorialpypi/releases/tag/v0.2',  # I explain this later on
    keywords=['SOME', 'KEYWORDS'],  # Keywords that define your package best
    install_requires=['beautifulsoup4',
                      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
