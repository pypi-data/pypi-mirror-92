from .compression import encodeLZ78, decodeLZ78
from argparse import ArgumentParser

main_command = ArgumentParser(
    prog="lz78",
)

main_command.add_argument("-x", type=str, dest="extract")
main_command.add_argument("-c", type=str, dest="compress")
main_command.add_argument("-o", type=str,  dest="set_output")
main_command.add_argument("-i", type=int, default=3, dest="n_bytes_index")
main_command.add_argument("-n", type=int, default=1, dest="n_bytes_character")


if __name__ == "__main__":
    parsed = main_command.parse_args()

    if parsed.extract :
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
    # encodeLZ78("teste-duplicado.txt", "teste-duplicado.z78")
    # decodeLZ78("teste-duplicado.z78", "teste-duplicado-out.txt")
