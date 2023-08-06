import setuptools


with open('requirements.txt', 'r', encoding='utf-8') as fh:
    required = fh.read()

with open('README.rst', 'r', encoding='utf-8') as fh:
    long_description = fh.read()


setuptools.setup(
    name='ANF-Feed',
    version='0.0.1.dev2',
    author='m1ghtfr3e',
    description='Read ANF Feeds',
    keywords='anf, feed, rss',
    long_description=long_description,
    url='https://github.com/m1ghtfr3e/ANF-Feed-Reader',
    packages=setuptools.find_packages(),
    install_requires=required,
    include_package_data = True,
    data_files=[
        ('', ['anfrss/assets/anf.png'])
    ],
    entry_points={
        'console_scripts':[
            'anfrss = anfrss.gui.guiapp:run'
        ]
    },
    license='GPLv3',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Development Status :: 1 - Planning',
        'Environment :: X11 Applications :: Qt',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary',
        ],
    python_requires='>=3',
    project_urls={
        'Source': 'https://github.com/m1ghtfr3e/ANF-Feed-Reader',
        'Bug Reports': 'https://github.com/m1ghtfr3e/ANF-Feed-Reader/issues'
    }
)
