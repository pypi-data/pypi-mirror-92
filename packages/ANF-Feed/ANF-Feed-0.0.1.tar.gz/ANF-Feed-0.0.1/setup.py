import os
import sys
import setuptools

here = os.path.abspath(os.path.dirname(__file__))

sys.path.insert(0, here)


with open('README.rst', 'r', encoding='utf-8') as fh:
    long_description = fh.read()


Requires = [
    'feedparser',
    'requests',
    'PyQt5',
    'qdarkstyle',
]


setuptools.setup(
    name='ANF-Feed',
    version='0.0.1',
    author='m1ghtfr3e',
    description='Read ANF Feeds',
    keywords='anf, feed, rss',
    long_description=long_description,
    url='https://github.com/m1ghtfr3e/ANF-Feed-Reader',
    packages=setuptools.find_packages(),
    install_requires=Requires,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'anfrss = anfrss.gui.guiapp:run'
        ]
    },
    license='GPLv3',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        'Environment :: X11 Applications :: Qt',
        'Intended Audience :: Other Audience',
        'Natural Language :: English',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary',
    ],
    python_requires='>=3',
    project_urls={
        'Source': 'https://github.com/m1ghtfr3e/ANF-Feed-Reader',
        'Bug Reports': 'https://github.com/m1ghtfr3e/ANF-Feed-Reader/issues'
    }
)
