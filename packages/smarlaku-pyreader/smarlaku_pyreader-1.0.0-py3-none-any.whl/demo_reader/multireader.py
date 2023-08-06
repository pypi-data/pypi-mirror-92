import os

print("sub-modules of compressed sub-package are being imported.")

import demo_reader.compressed.bzipped as bzipped# sub-module import
import demo_reader.compressed.gzipped as gzipped# sub-module import

extension_map = {
    'bz2': bzipped.opener,
    'gz': gzipped.opener
}

print("MultiReader Class is being imported!")

class MultiReader:
    # MultiReader class contains 3 methods.
    def __init__(self, filename):
        extension = os.path.splitext(filename)[1]
        opener = extension_map.get(extension, open) #falls back to open if no matching extension is found.
        self.f = opener(filename, mode='rt')

    def close(self):
        self.f.close()

    def read(self):
        return self.f.read()