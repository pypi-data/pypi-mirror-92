from setuptools import setup, find_packages

setup(
  name = 'darkai',         # How you named your package folder (MyLib)
  packages = find_packages(),   # Chose the same as "name"
  version = '0.5',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'DarkAI is a Machine Learning Framework, designed from the core to be simple, versatile and highly performant',   # Give a short description about your library
  author = 'Thomas Sudeep Benardo',                   # Type in your name
  author_email = 'contact@codewithzeal.com',      # Type in your E-Mail
  url = 'https://github.com/thomasb892/darkai',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/user/reponame/archive/v_03.tar.gz',    # I explain this later on
  keywords = ['machine learning', 'deep learning', 'supervised learning',
                'unsupervised learning', 'reinforcement learning'],   # Keywords that define your package best
  install_requires = [],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
