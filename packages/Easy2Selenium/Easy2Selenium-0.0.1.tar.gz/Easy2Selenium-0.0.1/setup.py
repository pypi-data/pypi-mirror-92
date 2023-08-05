from setuptools import setup, find_packages

setup(name='Easy2Selenium',
      version='0.0.1',
      url='https://github.com/HHongSeungWoo/EasySelenium',
      author='HHongSeungWoo',
      author_email='qksn1541@gmail.com',
      description='Library for easy use of Selenium.',
      packages=find_packages(exclude=['tests']),
      long_description=open('README.md', 'r', encoding='utf8').read(),
      long_description_content_type='text/markdown',
      install_requires=['selenium', 'mitmproxy'],
      zip_safe=False,
      classifiers=[
          'License :: OSI Approved :: MIT License'
      ],
      python_requires='>=3.0'
)
