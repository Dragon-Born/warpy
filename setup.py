from setuptools import setup

setup(name='WARP+ to WireGuard',
      version='0.5',
      description='A simple cli to get WARP+ as WireGuard configuration',
      url='https://github.com/warp-plus/warpy-python',
      author='Arian Amiramjadi',
      author_email='me@arian.lol',
      packages=['warpy'],
      install_requires=['pynacl', "requests"],
      entry_points={'console_scripts': [
            'warpy = warpy.__main__',
        ]}
      )
