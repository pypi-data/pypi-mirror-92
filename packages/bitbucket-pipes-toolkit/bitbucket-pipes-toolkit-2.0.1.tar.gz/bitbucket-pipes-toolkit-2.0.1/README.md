Bitbucket Pipes Toolkit
=========

![Coverage](https://bitbucket.org/bitbucketpipelines/bitbucket-pipes-toolkit/downloads/coverage.svg)

This package contains various tools and helpers to make it more fun and easy for people to develope pipes. This includes improved colorized logging, shared data interface, array variables helpers and more.

Installation
============

`pip install bitbucket_pipes_toolkit`


Examples
========

Simple pipe example
```python3
from bitbucket_pipes_toolkit import Pipe

class MyPipe(Pipe):
    def run(self):
        super().run()
        print("I'm a simple little pipe")


# below is a simple schema for pipe variables.
schema = {'USERNAME': {'required': True, 'type': 'string'},
          'PASSWORD': {'required': True, 'type': 'string'}}

pipe_metadata = {
	'name': 'My Pipe',
	'image': 'mydockerimage:latest'
}
my_pipe=MyPipe(pipe_metadata=pipe_metadata, schema=schema)
my_pipe=pipe.run()
```

Documentation
=============

For more details have a look at the [official documentation](https://bitbucket-pipes-toolkit.readthedocs.io).