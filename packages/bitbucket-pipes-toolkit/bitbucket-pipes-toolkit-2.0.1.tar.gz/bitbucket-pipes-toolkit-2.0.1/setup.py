from setuptools import setup

setup(
    name='bitbucket-pipes-toolkit',
    version='2.0.1',
    packages=['bitbucket_pipes_toolkit', ],
    url='https://bitbucket.org/bitbucketpipelines/bitbucket-pipes-toolkit',
    author='Atlassian',
    author_email='bitbucketci-team@atlassian.com',
    description='This package contains various helpers for developing bitbucket pipelines pipes',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    install_requires=['colorama==0.4.1',
                      'colorlog==4.0.2',
                      'pyyaml==5.3.*',
                      'Cerberus==1.2',
                      'docker==4.2.*',
                      'GitPython==3.0.8', ]
)
