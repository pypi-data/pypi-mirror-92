print("Bzipped Module is being imported!")
import bz2
from ..util import writer

# Relative Imports
# from . import name ==> from demo_reader.compressed import name
# from .. import name ==> from demo_reader import name
# from ..util import name ==> from demo_reader.util import name

# define an alias for bz2.open, returns file handler like object. 
# But these kinds of open always de-compresses files during reading.
opener = bz2.open

if __name__ == "__main__": # see module#4 of Python fundamentals.
    writer.main(opener)
    # f = bz2.open(sys.argv[1], mode='wt')
    # f.write(' '.join(sys.argv[2:]))
    # f.close()

