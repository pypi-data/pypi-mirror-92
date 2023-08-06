from setuptools import setup


setup(
    name='tpcb',
    version='0.1',
    long_description=open(f'{__file__}/../README.rst', encoding='utf-8').read(),
    long_description_content_type='text/x-rst',
    description=(
        'A command-line utility that converts the text in clipboard into'
        'keystrokes after a given amount of time (default: 2sec).'),
    url='https://github.com/5j9/tpcb',
    author='5j9',
    author_email='5j9@users.noreply.github.com',
    license='GNU General Public License v3 (GPLv3)',
    packages=['_tpcb'],
    python_requires='>=3.6',
    install_requires=['typer', 'pyperclip', 'pyautogui'],
    entry_points={'gui_scripts': ['tpcb = _tpcb.tpcb:main']},
    zip_safe=True,
    classifiers=[
        "Environment :: Console",
        "Natural Language :: English",
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: '
        'GNU General Public License v3 or later (GPLv3+)',
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        'Topic :: Utilities',
    ],
    keywords='convert type clipboard paste keystroke')
