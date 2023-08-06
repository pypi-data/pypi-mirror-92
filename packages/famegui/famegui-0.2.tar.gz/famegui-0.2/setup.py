from distutils.core import setup
setup(
    name='famegui',
    packages=['famegui', 'famegui.models'],
    version='0.2',
    license='Apache',
    description='Graphical user interface to the FAME modelling framework',
    author='Aurélien Regat-Barrel',
    author_email='pypi@cyberkarma.net',
    url='https://gitlab.com/fame2/FAME-Gui',
    download_url='https://gitlab.com/fame2/FAME-Gui/-/archive/v0.2/FAME-Gui-v0.2.tar.gz',
    install_requires=[
        'pyyaml',
        'python-igraph',
        'PySide2'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Visualization',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    entry_points={
        'console_scripts': [
            'famegui=famegui.app:run',
        ],
    },
)
