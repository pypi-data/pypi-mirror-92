import setuptools
import newpy

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='new_py',
    version=newpy.VERSION,
    author='Ken Youens-Clark',
    author_email='kyclark@gmail.com',
    description='Stub a new Python CLI program',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/kyclark/new.py',
    packages='.',
    entry_points={
        'console_scripts': [
            'new.py=newpy:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
