from setuptools import setup, find_packages


with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='python-automation',
    version='0.5.0',
    long_description = long_description,
    long_description_content_type='text/markdown',
    description='window automation package',
    author='changgwak',
    author_email='iamtony.ca@gmail.com',
    url='https://github.com/changgwak/python-automation',
    install_requires=['opencv-python', 'numpy', 'pillow', 'pywin32', 'comtypes', 'PyQt5', 'pyscreeze'],
    packages=find_packages(exclude=[]),
    keywords=['pyauto', 'rpa', 'python rpa', 'python automation', 'window selenium', 'pyautomation', 'autoclick'],
    python_requires='>=3.10',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)
