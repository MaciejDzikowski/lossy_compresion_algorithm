A lossy compression algorithm for .png files.

Components:
- encode.py
    An encoding tool which compressing any set of .png files to a numpy array.
    User can choose a degree of compressing (between [1] and [number of files - 1]).
    
- decode.py
    An decoding tool which decompresing a chosen number of compressed pictures.
