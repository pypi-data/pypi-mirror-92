from distutils.core import setup

long_description = """**Rivals of Aether skin package**

This is a fan-made package to generate skins for the game Rivals of Aether.

**Features**

- Generate new skins from color code
- Generate skins with random color
- Get the valid in-game color code of skins
- Generate preview images
- Show preview images in window
- Print preview images to file

**Documentation**

You can find the documentation here: https://htmlpreview.github.io/?https://github.com/ErrorThreeOThree/roaskins/blob/master/docs/build/html/index.html

**Example Application: Discord chat bot**

I have provided an example application using this library. This application is a discord chat bot that can generate random skins and post preview images in discord. You can find the source code here: https://github.com/ErrorThreeOThree/ROASkinBot"""

setup(
    long_description=long_description,
    long_description_content_type='text/markdown',
    name = 'roaskins',
    packages = ['roaskins'],
    version = '1.1',
    license = 'MIT',
    description = 'Rivals of Aether skin and color code library',
    author = 'Julian Hartmer',
    author_email = 'j.hartmer@googlemail.com',
    url = 'https://github.com/ErrorThreeOThree/roaskins',
    keywords = ['roa', 'Rivals', 'of', 'Aether', 'skin'],
    package_data={'': ['data/*/*']},
    include_package_data=True,
    install_requires = [
        'opencv-python',
        'numpy'
    ],
    classifiers = [
        'Development Status :: 5 - Production/Stable  ',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],

)