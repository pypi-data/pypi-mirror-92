from setuptools import setup, find_packages
import sys, os

NAME = "tegridy-tools"

version_ns = {}
with open('./tegridy_tools/__version__.py') as f:
    exec(f.read(), {}, version_ns)

with open('./tegridy_tools/README.md') as f:
    long_description = f.read()

setup(
    name='tegridy-tools',
    version=version_ns['__version__'],    
    description='All tegridy-tools as python modules because there is never enough tegridy :)',
    url='https://github.com/asigalov61/tegridy-tools',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="music nlp raspberry-pi machine-learning deep-learning midi numpy               keras pytorch music-generation python-modules plagiarism-detection               midi-toolkit midi-processing artifical-intelligence tensorflow2               tegridy pyknon midi-processor midi-search",
    author='Aleksandr Sigalov',
    author_email='asigalov61@hotmail.com',
    license='Apache 2.0',
    packages=find_packages(exclude=["test",]),
    namespace_packages=[],
    include_package_data=False,
    zip_safe=False,
    install_requires=['tqdm',
                      'unidecode',
                      'torch',
                      'torchvision',
                      'keras',
                      'pretty-midi',
                      'tensorflow==1.15.0',
                      'tensorflow-datasets==3.2.1',
                      'visual_midi',
                      'pyfluidsynth',
                      'pypianoroll',
                      'matplotlib',
                      'librosa',
                      'fluidsynth',
                      'midi2audio',                     
                      ],

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',  
        'Operating System :: OS Independent',        
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9"
    ],
)