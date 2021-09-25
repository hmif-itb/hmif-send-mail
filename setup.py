from setuptools import setup

setup(name='sendmail',
      version='0.1.1',
      description='Template for sending email',
      url='https://github.com/hmif-itb/hmif-send-mail',
      author='HMIF Tech',
      author_email='hmif_itb@km.itb.ac.id',
      license='MIT',
      packages=['sendmail'],
      install_requires=[
          'pyyaml',
          'requests',
          'boto3'
      ],
      python_requires='>=3',
      zip_safe=False)
