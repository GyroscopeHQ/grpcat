from distutils.core import setup

setup(name='grpcat',
      version='0.1',
      description='gRPC arbitrary message sender.',
      author='Adam Fletcher',
      author_email='adam@gyroscope.cc',
      url='https://github.com/GyroscopeHQ/grpcat',
      py_modules=['grpcat', 'grpcio-tools', 'protobuf'],
      )
