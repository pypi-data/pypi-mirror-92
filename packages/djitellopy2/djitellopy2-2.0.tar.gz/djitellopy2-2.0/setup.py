import setuptools

with open("README.md", "r", encoding="utf-8") as fd:
    long_description = fd.read()

setuptools.setup(
    name='djitellopy2',  # How you named your package folder (MyLib)
    packages=['djitellopy2'],  # Chose the same as "name"
    version='2.0',  # Start with a small number and increase it with every change you make
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='DJI Tello drone interface using the official Tello SDK including support for state packets and video streaming',
    long_description=long_description,
    long_description_content_type='text/markdown',
    # Give a short description about your library
    author='Jakob Löw',  # Type in your name
    author_email='djitellopy2@m4gnus.de',  # Type in your E-Mail
    url='https://github.com/M4GNV5',  # Provide either the link to your github or to your website
    download_url='https://github.com/damiafuentes/TelloSDKPy/archive/v_1.5.tar.gz',  # I explain this later on
    keywords=['tello', 'dji', 'drone', 'sdk', 'official sdk'],  # Keywords that define your package best
    install_requires=[  # I get to this in a second
        'numpy',
        'opencv-python',
    ],
    python_requires='>=3.4',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
