from setuptools import setup, find_packages

setup(name='hermeskit', 
      author='HuynhThanhQuan',
      author_email='quanht6@onemount.com',
      maintainer='HuynhThanhQuan',
      maintainer_email='quanht6@onemount.com',
      description='Credit Scoring Python package',
      license='MIT',
      version='1.0.7',
      python_requires=">=3.7",
      url='https://vinid-team.atlassian.net/wiki/spaces/1/pages/677551034/0.+About+Hermes',
      keywords=['CreditScoring', 'Hermes', '1MG', 'CDO'],
      packages=find_packages(),
      data_files=[
            ('hermeskit', ['hermeskit/metrics/config.yaml'])
      ],
      install_requires=[
            'numpy>=1.18',
            'scikit-learn>=0.24',
            'pandas>=1.2',
            ]
      )