from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Operating System :: OS Independent',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3'      #Specify which pyhton versions that you want to support
]
 
setup(
  name='ainshamsflow',
  version='0.0.5',
  description='A keras inspired deep learning framework.',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
  long_description_content_type='text/markdown',
  url='https://github.com/PierreNabil/AinShamsFlow',
  author='Pierre Nabil',
  author_email='pierre.nabil.attya@gmail.com',
  license='MIT',
  classifiers=classifiers,
  keywords='deep learning',
  packages=find_packages(),
  install_requires=['numpy', 'matplotlib', 'varname']
)

# https://pypi.org/project/ainshamsflow/0.0.5/

# python setup.py sdist bdist_wheel
# python -m twine upload dist/* --skip-existing
# Username: PierreNabil
# Password: q$?ZNdSL7PP&%9y