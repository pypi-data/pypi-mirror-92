from setuptools import setup, find_packages
setup_args = dict(
name = 'MoSeka',  # How you named your package folder (MyLib)
version = '2.5',  # Start with a small number and increase it with every change you make
license = 'MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
description = 'Deep learning framework',  # Give a short description about your library
author = 'Mohamed elsayed',  # Type in your name
packages=find_packages(),
author_email = 'mohamedelsayed16397@gmail.com',  # Type in your E-Mail
url = 'https://github.com/Muhamedelsayed/MNiST',  # Provide either the link to your github or to your website
download_url = 'https://github.com/Muhamedelsayed/MNiST/archive/2.5.tar.gz',  # I explain this later on
keywords = ['Lenet5', 'Framework', 'MNIST'],  # Keywords that define your package best
include_package_data=True
)
install_requires = [  # I get to this in a second
                       'numpy',
                       'pandas',
                       'matplotlib',
                   ],
if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
