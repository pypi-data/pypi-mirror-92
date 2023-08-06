from .compression import encodeLZ78, decodeLZ78
from argparse import ArgumentParser

main_command = ArgumentParser(
    prog="pylz78",
    description="""A program for compressing and decompressing files using lz78 encoding.
    

    The number of bytes in both the character and index representations must be the same when
    encoding and decoding.
    

    When output is not set, the output of the extraction of a file.z78 is file.txt, and vice 
    versa for compression."""
)

main_command.add_argument("-x", "--extract",
                          type=str,
                          dest="extract",
                          help="extract a lz78 compressed file"
                          )
main_command.add_argument("-c", "--compress",
                          type=str,
                          dest="compress",
                          help="compress a file in lz78"
                          )
main_command.add_argument("-o", "--output",
                          type=str,
                          dest="set_output",
                          help="set the output file name"
                          )
main_command.add_argument("-i",
                          type=int,
                          default=3,
                          dest="n_bytes_index",
                          help="number of bytes for the index representation on the compressed file"
                          )
main_command.add_argument("-n", type=int,
                          default=1,
                          dest="n_bytes_character",
                          help="number of bytes for the character representation on the compressed file"
                          )


def main():
    parsed = main_command.parse_args()

    if parsed.extract:
        if parsed.set_output:
            decodeLZ78(parsed.extract, parsed.set_output,
                       parsed.n_bytes_index, parsed.n_bytes_character)
        else:
            decodeLZ78(parsed.extract, '.'.join(parsed.extract.split('.')[
                       :-1] + ['txt']), parsed.n_bytes_index, parsed.n_bytes_character)
    elif parsed.compress:
        if parsed.set_output:
            encodeLZ78(parsed.compress, parsed.set_output,
                       parsed.n_bytes_index, parsed.n_bytes_character)
        else:
            encodeLZ78(parsed.compress, '.'.join(parsed.compress.split('.')[
                       :-1] + ['z78']), parsed.n_bytes_index, parsed.n_bytes_character)
