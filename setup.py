"""
    Setup file for shitposteragent2.
    Use setup.cfg to configure your project.

    This file was generated with PyScaffold 4.6.
    PyScaffold helps you to put up the scaffold of your new Python project.
    Learn more under: https://pyscaffold.org/
"""

from setuptools import setup, find_packages

if __name__ == "__main__":
    try:
        setup(
            name='shitposteragent2',
            version='0.1.0',
            description='Automate your social media presence across various platforms.',
            author='nathfavour',
            author_email='116535483+nathfavour@users.noreply.github.com',
            license='MIT',
            keywords='automation social-media',
            packages=find_packages(where='src'),
            package_dir={'': 'src'},
            include_package_data=True,
            install_requires=[
                'pyautogui',
                'playwright',
                'vosk',
                'flite',
                'importlib-metadata; python_version<"3.8"'
            ],
            entry_points={
                'console_scripts': [
                    'shitposter=cli.main:main',
                ],
            },
            classifiers=[
                'Development Status :: 4 - Beta',
                'Programming Language :: Python :: 3',
                'License :: OSI Approved :: MIT License',
            ],
            python_requires='>=3.8',
        )
    except:  # noqa
        print(
            "\n\nAn error occurred while building the project, "
            "please ensure you have the most updated version of setuptools, "
            "setuptools_scm and wheel with:\n"
            "   pip install -U setuptools setuptools_scm wheel\n\n"
        )
        raise
