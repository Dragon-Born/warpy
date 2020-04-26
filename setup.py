from setuptools import setup
from os import path

current_dir = path.abspath(path.dirname(__file__))

with open(path.join(current_dir, 'README.md')) as f:
    description = f.read()

setup(name='warpy',
      version='0.7.3',
      long_description=description,
      long_description_content_type='text/markdown',
      description='A simple cli to get WARP+ as WireGuard configuration',
      url='https://github.com/warp-plus/warpy',
      download_url='https://github.com/warp-plus/warpy/archive/v_07.tar.gz',
      keywords=['warpy', 'warp+', 'warp-plus', 'warp wireguard'],
      license='GPL',
      author='Arian Amiramjadi',
      author_email='me@arian.lol',
      packages=['warpy'],
      install_requires=['pynacl', "requests"],
      entry_points={'console_scripts': [
          'warpy = warpy.__main__:main',
      ]},
      classifiers=[
          'Development Status :: 3 - Alpha',
          # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Build Tools',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
      ],
      )
