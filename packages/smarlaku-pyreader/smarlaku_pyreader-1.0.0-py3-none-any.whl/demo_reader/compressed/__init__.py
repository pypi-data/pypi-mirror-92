# demo_reader/compressed/__init__.py
print("Sub-Package compressed is being imported!")
from demo_reader.compressed.bzipped import opener as bz2_opener
from demo_reader.compressed.gzipped import opener as gz_opener

__all__ = ['bz2_opener', 'gz_opener']