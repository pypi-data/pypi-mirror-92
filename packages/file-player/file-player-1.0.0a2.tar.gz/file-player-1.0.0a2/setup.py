from setuptools import setup

LONG_DESCRIPTION_STR = "A music and audio player which uses the file system rather than tags to order files. Support for m3u playlists"

setup(
    name='file-player',
    version='1.0.0-alpha2',
    packages=['filep'],
    url='https://gitlab.com/SunyataZero/file-player',
    license='GPLv3',
    author='Tord Dellsén',
    author_email='tord.dellsen@gmail.com',
    description='A music and audio player which uses the file system rather than tags to order files',
    install_requires=["PyQt5>=5.15.2"],
    entry_points={"console_scripts": ["file-player=filep.__main__:main"]},
    long_description_content_type='text/markdown',
    long_description=LONG_DESCRIPTION_STR,
    python_requires='>=3.8.0',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3'
    ]
)
