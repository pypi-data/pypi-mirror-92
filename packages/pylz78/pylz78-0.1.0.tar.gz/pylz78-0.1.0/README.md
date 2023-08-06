# Trabalho Prático 1

## Algoritmos 2 - DCC - ICEx - UFMG

### Pedro Tavares de Carvalho

Esse trabalho tem como objetivo a implementação de um compressor/decompressor padrão `lz78`, utilizando uma trie compacta como estrutura auxiliar. Esse algoritmo de compressão implica na representação do texto como um conjunto de prefixos em ordem, identificando cada sequência como um prefixo existente acoplado a um caractere novo do texto.

Em pseudocódigo, o algoritmo se dá assim:

```pseudocode
def encodeLZ78(texto):
	prefixos = map()
	prefixos.add('', 0)
	cadeia = ''
	indice = 1
	for caractere in texto:
		if cadeia + caractere in prefixos: 	// se a cadeia com o caractere
        									// já existe nos prefixos
			cadeia = cadeia + caractere 	// adicione mais um caractere
            								// à cadeia
			continue
		saida(caractere, prefixos[cadeia]) 	// caso não exista, 
											// adicione à saída a nova
                                            // sequencia que tem que ser
                                            // impressa
		
		prefixos.add(cadeia + caractere, indice) 	// adicione o prefixo
													// atual à cadeia
		indice = indice + 1 // aumente o índice
		cadeia = ''
```

No caso dessa implementação, o mapa `prefixos` de dará por uma trie compacta, porém a lógica da compressão continua a mesma.

Essa substituição tem como objetivo diminuir a memória gasta com guardar os prefixos já existentes, pois um mapa tem que guardar os prefixos completos, porém a trie compacta é construída de forma a utilizar os prefixos como parte da indexação da mesma, diminuindo a repetição de prefixos comuns.

A decompressão, porém, traz alguma dificuldade. Apesar de algoritmicamente simples, ela exige acesso aos índices já concebidos, e com a estrutura da trie esse acesso possui complexidade alta, $\mathcal O(n)$, dado que a busca por índices é basicamente uma busca em profundidade/largura o que incapacita a mesma de fazer o processo de decompressão eficientemente.

## Implementação

 Em um primeiro momento, foi implementado o algoritmo com um dicionário como estrutura auxiliar, apenas para prova de contexto. Essa implementação foi relativamente simples.

## Trie

Em termos da implementação da trie, os algoritmos foram baseados nos vistos em sala de aula, implementados à risca. 

### Inserção

O algoritmo de inserção é descrito abaixo

```pseudocode
def inserir(node, palavra, valor):
	indice_final, filho = node.comparar_prefixos(palavra)
	if !filho:
    	node.adicionar_filho(palavra, nova_folha(valor))
    	if node.is_folha:
    		node.adicionar_filho('', nova_folha(node.valor))
    		node.is_folha = false
    		node.valor = Null
    else if indice_final == palavra.tamanho():
    	inserir(filho, palavra[:indice_final], valor)
    else:
    	temp = filho
    	node.remover(filho)
    	chave_resto_filho = filho.chave[:indice_final]
    	no = novo_no()
    	filho.chave = filho.chave[indice_final:]
    	node.adicionar_filho(chave_resto_filho, no)
    	no.adicionar_filho(filho.chave, filho)
    	no.adicionar_filho(palavra[indicie_final:], nova_folha(valor))
```

A especificação do funcionamento está no código, mas se entende que existem três casos:

1. Caso, ao adicionar uma palavra ao nó, essa palavra não compartilhe prefixos com os filhos desse nó, crie um nó filho com a palavra como valor.
   1. Nesse caso ainda, se o nó no qual a palavra está sendo adicionada era uma folha, estão crie outro nó filho, com a sequência vazia como valor.
2. Caso dentre os filhos exista um prefixo da palavra em questão, adicione o resto dessa palavra ao filho.
3. Caso um dos filhos compartilhe um prefixo com a palavra em questão, crie um novo nó com o prefixo compartilhado, e adicione dois nós a esse, com o resto da palavra e o resto do prefixo.

Esse algoritmo constrói a trie a partir de um nó vazio, com o seu valor colocado como a cadeia vazia.

### Remoção

Como não havia necessidade de remoção de itens da estrutura, a remoção não foi implementada.

### Busca

A busca se dá de forma simples. A cada nó, acha a chave que compartilha um prefixo com a palavra a ser buscada. Se essa chave não existir, retorne -1. Se ela existir, repita a busca com o nó correspondente à chave, e com a palavra sem o prefixo da chave.

## Compressão

A compressão foi feita respeitando o pseudocódigo descrito na introdução do relatório, apenas substituindo o mapa utilizado para os prefixos pela implementação de trie compacta e implementando a saída como uma saída binária.

A saída do código gera um arquivo em que os índices de cada prefixo e os caracteres correspondentes a ele possuem um número específico de *bytes*, passado como parâmetro pela interface de linha de comando.

## Decompressão

A estrutura de dados utilizada na decompressão foi simplesmente um vetor de cadeias. A estrutura é ótima pois inserção e acesso é $\mathcal O(1)$, e a utilização de memória não é tão grande.

## Interface com o usuário

A interface com o usuário foi feita utilizando a biblioteca `argparse`, da biblioteca *default* da linguagem.