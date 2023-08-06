from distutils.core import setup

setup(
    name='eliteapi',
    packages=['eliteapi'],
    version='0.1',
    license='MIT',
    description='eliteapi is a Python wrapper for Elite Creative allowing you to easly interact with the API.',
    author='Kappa',
    author_email='f.cappetti.05@gmail.com',
    url='https://github.com/KappaOnGit/eliteapi',
    download_url='https://github.com/FraKappa/eliteapi/archive/v_01.tar.gz',
    keywords=['eliteapi', 'elite'],
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
