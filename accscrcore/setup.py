from setuptools import setup, find_packages

from pip.req import parse_requirements

install_reqs = parse_requirements('requirements/production.txt', session=False)

# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
reqs = [str(ir.req) for ir in install_reqs]

setup(name='acc-scraper',
      version='0.0.1',
      description='Accommodation scraper',
      author='LLama s.r.o',
      author_email='luxas98@gmail.com',
      test_suite='nose.collector',
      tests_require=['nose', 'mock'],
      install_requires=reqs,
      packages=find_packages(),
      scripts=[],
      )
