from setuptools import setup

setup(name='WARP+ to WireGuard',
      version='0.7',
      description='A simple cli to get WARP+ as WireGuard configuration',
      url='https://github.com/warp-plus/warpy-python',
      download_url='https://github.com/warp-plus/warpy-python/archive/v_05.tar.gz',
      keywords = ['warpy', 'warp+', 'warp-plus', 'warp wireguard'],
      license='gpl',
      author='Arian Amiramjadi',
      author_email='me@arian.lol',
      packages=['warpy'],
      install_requires=['pynacl', "requests"],
      entry_points={'console_scripts': [
            'warpy = warpy.__main__:main',
        ]},
      classifiers=[
          'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
          'Intended Audience :: Developers',      # Define that your audience are developers
          'Topic :: Software Development :: Build Tools',
          'License :: OSI Approved :: gpl License',   # Again, pick a license
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
        ],
      )
