import os

from setuptools import setup, find_packages
version = [
    (line.split('=')[1]).strip().strip('"').strip("'")
    for line in open(os.path.join('bcmwindow','version.py'))
    if line.startswith( '__version__' )
][0]

if __name__ == "__main__":
    setup(
        name='bcmwindow',
        version='1.0.0',
        description='bcmwindow',
        long_description='bcmwindow',
        classifiers=[
            "Programming Language :: Python",
        ],
        author='Mike C. Fletcher',
        author_email='mcfletch@vrplumber.com',
        url='https://github.com/mcfletch/bcmwindow',
        keywords='raspberry pi, window, opengl, gles, egl',
        packages=find_packages(),
        include_package_data=True,
        license='MIT',
        package_data = {
            'bcmwindow': [
            ],
        },
        install_requires=[
        ],
        scripts = [
        ],
        entry_points = dict(
            console_scripts = [
            ],
        ),
    )

