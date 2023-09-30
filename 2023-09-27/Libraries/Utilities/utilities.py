import sys


BLOCK_SIZE = 4096
GB = 2**30


def memory_size():
    nb_blocks = sys.getallocatedblocks()
    nb_bytes = nb_blocks * 4096
    nb_GB = nb_bytes / GB
    return f"{nb_GB:.2f} GB"
