# decode-me
Decode-me is a python application used to decode secret messages encoded in VERY simple .WAV files using the Bell 103 Modem protocol. 

The program was written as an assignment for the Computers, Sound, and Music — Spring 2019 class. The full functionality is in place, there was a little trouble creating the goertzel filter as many of the algorithms differ and the implementation I went with required some tweaking of the coefficients in order to make it work as intended. An addition i'd like to make in the future is the other half of modem functionality; being able to encode secret messages using the Bell protocol.

The application can be run either through an IDE (Pycharm) or through the Command-Line.

To run via command line:
  1. clone the repository
  2. navigate to the src directory
  3. run 'python{version} decode.py {path-to-wav-file}'
  
