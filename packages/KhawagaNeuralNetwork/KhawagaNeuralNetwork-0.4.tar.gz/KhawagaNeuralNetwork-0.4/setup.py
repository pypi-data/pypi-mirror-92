from distutils.core import setup
setup (
  name = 'KhawagaNeuralNetwork',         # How you named your package folder (MyLib)
  packages = ['KhawagaNeuralNetwork'],   # Chose the same as "name"
  version = '0.4',      # Start with a small number and increase it with every change you make
  license='Apache License 2.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Deep Learning Framework that has multiple operations that could preprocess data, train and test the model with good accuracy.',   # Give a short description about your library
  author = 'Youssef khawaga',                   # Type in your name
  author_email = 'yousefkhawaga@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/YousefKhawaga/KhawagaNeuralNetwork',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/YousefKhawaga/KhawagaNeuralNetwork/archive/0.2.tar.gz',    # I explain this later on
  keywords = ['DeepLearning', 'Tool', 'Framework'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'numpy',
          'pandas',
          'matplotlib'
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: Apache Software License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)