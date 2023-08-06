# FYI:
# https://packaging.python.org/tutorials/packaging-projects/
# https://realpython.com/pypi-publish-python-package/

from setuptools import setup
gh_repo = 'https://github.com/weaming/git-refs'

setup(
    name='git-refs',  # Required
    version='1.1',  # Required
    description='list git references(branches, tags) on local and remote repositories',  # Required
    long_description=open('README.md').read().strip(),
    long_description_content_type="text/markdown",
    url=gh_repo,  # Optional
    author='weaming',  # Optional
    author_email='garden.yuen@gmail.com',  # Optional
    install_requires=['gitpython'],
    py_modules=['git_refs'],
    entry_points={  # Optional
        'console_scripts': [
            'git-refs=git_refs:main',
        ],
    },
    keywords='git,cli,develop',  # Optional
    project_urls={  # Optional
        'Bug Reports': gh_repo,
        'Source': gh_repo,
    },
)
