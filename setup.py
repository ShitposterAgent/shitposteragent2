"""
    Setup file for shitposteragent2.
    Use setup.cfg to configure your project.
"""
from setuptools import setup, find_packages

if __name__ == "__main__":
    try:
        setup(
            name='shitposteragent2',
            version='0.1.0',
            description='Intelligent social media automation agent with continuous monitoring',
            author='nathfavour',
            author_email='116535483+nathfavour@users.noreply.github.com',
            license='MIT',
            keywords='automation social-media ai ollama',
            packages=find_packages(where='src'),
            package_dir={'': 'src'},
            include_package_data=True,
            python_requires='>=3.8',
            install_requires=[
                'pyautogui',
                'playwright',
                'vosk',
                'flite',
                'ollama',
                'pytesseract',
                'pillow',
                'numpy',
                'fastapi',
                'uvicorn',
                'click',
                'asyncio',
                'pydantic',
                'python-multipart'
            ],
            entry_points={
                'console_scripts': [
                    'shitposter=cli.main:cli',
                ],
            },
            classifiers=[
                'Development Status :: 4 - Beta',
                'Programming Language :: Python :: 3',
                'License :: OSI Approved :: MIT License',
                'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
                'Topic :: Software Development :: Libraries :: Python Modules',
                'Topic :: Communications :: Chat',
            ],
        )
    except Exception:
        print(
            "\n\nAn error occurred while building the project, "
            "please ensure you have the most updated version of setuptools, "
            "setuptools_scm and wheel with:\n"
            "   pip install -U setuptools setuptools_scm wheel\n\n"
        )
        raise
