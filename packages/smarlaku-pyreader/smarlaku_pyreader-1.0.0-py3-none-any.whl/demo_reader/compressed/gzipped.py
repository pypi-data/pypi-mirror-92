print("Gzipped Module is being imported!")
import gzip
from ..util import writer

opener = gzip.open

if __name__ == "__main__":
    writer.main(opener)
    # f = gzip.open(sys.argv[1], mode='wt')
    # f.write(' '.join(sys.argv[2:]))
    # f.close()