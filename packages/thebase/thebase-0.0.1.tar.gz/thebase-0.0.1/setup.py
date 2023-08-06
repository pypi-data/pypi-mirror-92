from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 3 - Alpha',
  'Intended Audience :: Developers',
  'Operating System :: OS Independent',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='thebase',
  version='0.0.1',
  description='generic stuff i am using',
  # long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Osman Taskin',
  # author_email='josh@edublocks.org',
  license='MIT', 
  classifiers=classifiers,
  keywords='generic', 
  packages=find_packages(),
  install_requires=[''] 
)
