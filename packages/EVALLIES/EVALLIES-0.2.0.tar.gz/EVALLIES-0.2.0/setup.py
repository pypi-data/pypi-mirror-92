from distutils.core import setup

# patch distutils if it can't cope with the "classifiers" or
# "download_url" keywords
from sys import version
if version < '2.2.3':
    from distutils.dist import DistributionMetadata
    DistributionMetadata.classifiers = None
    DistributionMetadata.download_url = None

def get_evallies_version():
    with open('evallies/__init__.py') as f:
        s = [l.rstrip() for l in f.readlines()]
        version = None
        for l in s:
            if '__version__' in l:
                version = l.split('=')[-1]
        if version is None:
            raise RuntimeError('Can not detect version from evallies/__init__.py')
        return eval(version)

setup(
    name='EVALLIES',
    version=get_evallies_version(),
    author='Anthony Larcher',
    author_email='anthony.larcher@univ-lemans.fr',
    packages=['evallies', 'evallies.lium_baseline'],
    url='https://lium.univ-lemans.fr/en/allies-evaluation/',
    download_url='http://pypi.python.org/pypi/Evallies/',
    license='LGPL',
    platforms=['Linux, Windows', 'MacOS'],
    description='Lifelong learning Speaker diarization baseline system.',
    long_description=open('README.txt').read(),
    install_requires=[
        "mock",
        "nose",
        "numpy",
        "pyparsing",
        "python-dateutil",
        "scipy",
        "six",
        "matplotlib",
        "torch",
        "torchvision",
        "PyYAML",
        "h5py",
        "pandas",
        "fastcluster",
        "sidekit>=1.3.7",
        "soundfile",
        "s4d==0.1.5"
    ],
    package_data={'evallies': ['docs/*']},
    classifiers=['Development Status :: 4 - Beta',
                 'Environment :: Console',
                 'Environment :: MacOS X',
                 'Environment :: Win32 (MS Windows)',
                 'Environment :: X11 Applications',
                 'Intended Audience :: Education',
                 'Intended Audience :: Legal Industry',
                 'Intended Audience :: Science/Research',
                 'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
                 'Natural Language :: English',
                 'Operating System :: MacOS',
                 'Operating System :: Microsoft',
                 'Operating System :: Other OS',
                 'Operating System :: POSIX',
                 'Programming Language :: Python :: 3.6',
                 'Topic :: Multimedia :: Sound/Audio :: Speech',
                 'Topic :: Scientific/Engineering :: Artificial Intelligence']
)




