import numpy as np
from typing import Union, Tuple, Dict


class CTrie:
    def _get_biggest_prefix(self, word: str):
        ret: Tuple[int, Union[str, None]] = (-1, None)
        for key in self.children.keys():
            last = len(key)
            while last > 0:
                if key[:last] == word[:last]:
                    return (last, key)
                last -= 1
        return ret

    def __init__(self, value='', text=None, is_word=False, numeric_value=None, parent=None):
        self.children = {}
        self.value = value
        self.numeric_value = numeric_value
        self.is_word = is_word
        self.parent = parent

    def add(self, word, value):
        self._add(word, value)


    def _add_node(self, key: str, node=None) -> None:
        if node == None:
            node = CTrie()
        node.parent = self
        node.value = key
        self.children[key] = node

    def _add(self, word: str, value: int):
        last, key = self._get_biggest_prefix(word)

        if key == None: # caso não exista nenhum nó com o prefixo da palavra
            self._add_node(word, CTrie(is_word=True, numeric_value=value))  # adicione uma folha com esse prefixo
            
            if self.is_word and self.numeric_value != 0: # caso eu seja uma folha
                self._add_node( # adicione uma folha com valor vazio no meu nó
                    '', CTrie(is_word=True, numeric_value=self.numeric_value))
                self.is_word = False
                self.numeric_value = None

        elif last == len(key): # caso a chave seja um prefixo da palavra
            self.children[key].add(word[last:], value)  # adicione o sufixo da palavra ao nó correspondente
                                                        # a essa chave

        else:   # caso uma chave tenha um prefixo em comum com a palavra
            temp = self.children.pop(key)
            temp.value = key[last:]

            self._add_node(word[:last]) # crie um nó com o prefixo em comum
            self.children[word[:last]]._add_node(   # adicione um nó a esse filho com o sufixo da palavra
                word[last:], CTrie(is_word=True, numeric_value=value))

            self.children[word[:last]]._add_node(key[last:], temp)  # e recoloque a estrutura da árvore
                                                                    # no nó correspondente ao sufixo da chave


    def contains(self, word):
        if word == '' and '' in self.children.keys():
            return self.children[''].numeric_value
        if word == self.value:
            if self.numeric_value != None:
                return self.numeric_value

        last, key = self._get_biggest_prefix(word)

        if key == None:
            return -1
        return self.children[key].contains(word[last:])

    def __str__(self, level=0):
        ret = ""
        for child in self.children.values():
            ret += child.__str__(level + 1)
        ret += f"{level}" + str(self.value)
        ret += "\n"
        return ret
