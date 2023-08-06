from distutils.core import setup

# patch distutils if it can't cope with the "classifiers" or
# "download_url" keywords
from sys import version
if version < '2.2.3':
    from distutils.dist import DistributionMetadata
    DistributionMetadata.classifiers = None
    DistributionMetadata.download_url = None

def get_sidekit_version():
    with open('sidekit/__init__.py') as f:
        s = [l.rstrip() for l in f.readlines()]
        version = None
        for l in s:
            if '__version__' in l:
                version = l.split('=')[-1]
        if version is None:
            raise RuntimeError('Can not detect version from sidekit/__init__.py')
        return eval(version)

setup(
    name='SIDEKIT',
    version=get_sidekit_version(),
    author='Anthony Larcher',
    author_email='anthony.larcher@univ-lemans.fr',
    packages=['sidekit', 'sidekit.bosaris', 'sidekit.frontend', 'sidekit.libsvm', 'sidekit.nnet'],
    url='http://www-lium.univ-lemans.fr/sidekit/',
    download_url='http://pypi.python.org/pypi/Sidekit/',
    license='LGPL',
    platforms=['Linux, Windows', 'MacOS'],
    description='Speaker, Language Recognition and Diarization package.',
    long_description=open('README.txt').read(),
    install_requires=[
        "numpy==1.19.0",
        "pyparsing >= 2.4.7",
        "python-dateutil >= 2.8.1",
        "scipy>=1.6.0",
        "six>=1.15.0",
        "matplotlib>=3.3.2",
        "pyroomacoustics==0.4.2",
        "soundfile>= 0.10.3",
        "torch >= 1.7.1",
        "torchvision>=0.8.2",
        "tqdm>=4.55.1",
        "pyyaml>=5.4.1",
        "h5py>=2.10.0",
        "pandas>=1.2.1",
        "scikit-learn>=0.24.1"
    ],
    package_data={'sidekit': ['docs/*']},
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
                 'Programming Language :: Python :: 3.8',
                 'Topic :: Multimedia :: Sound/Audio :: Speech',
                 'Topic :: Scientific/Engineering :: Artificial Intelligence']
)




