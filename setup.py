from distutils.core import setup

with open('requirements.txt') as f:
        requirements = f.read().splitlines()

setup(
    name='cern_webinfra_inventory_client',
    packages=['cern_webinfra_inventory_client'],
    version='0.0.3',
    description='Library for managing CERN web infrastructure inventory',
    author='CERN / Wojciech Kulma',
    author_email='wojciech.kulma@cern.ch',
    url='https://github.com/wklm/cern_webinfra_inventory_client.git',
    download_url='https://github.com/wklm/cern_webinfra_inventory_client.git',
    keywords=['cern', 'webinfra', 'inventory', 'client'],
    classifiers=[],
    install_requires=requirements
)
