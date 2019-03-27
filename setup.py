from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='openbnmapi',
      version='0.3',
      description="The unofficial Python wrapper for Bank Negara Malaysia's Open API endpoints",
      long_description=readme(),
      url='https://github.com/knazran/python-openbnmapi',
      author='Khairul Nazran Kamarulnizam',
      author_email='khairulnazran94@gmail.com',
      license='MIT',
      packages=['openbnmapi'],
      install_requires=[
          'pandas',
          'requests'
      ],
      zip_safe=False)