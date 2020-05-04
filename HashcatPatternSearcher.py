import re
import itertools

# contém bugs (lista com itens duplicados, triplicados, etc pela quantidade de acontecimentos

# Hashcat groups for masks:
#?l = abcdefghijklmnopqrstuvwxyz
#?u = ABCDEFGHIJKLMNOPQRSTUVWXYZ
#?d = 0123456789
#?h = 0123456789abcdef
#?H = 0123456789ABCDEF
#?s = «space»!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
#?a = ?l?u?d?s
#?b = 0x00 - 0xff

# Ideia
# foco em l, u, d, h, H e s
# Abrir tabela binária para cada letra de cada senha
# Montar todos os padrões encontrados por palavra
# Somar o número de cada acontecimento de novo padrão encontrado

# Exemplo de complexidade
#
# |Dead1234
# |____________
#l|01110000
#u|10000000
#d|00001111
#h|01111111
#H|10001111
#s|00000000
#
# |Dead1234
# |____________
# |ullldddd
# |Hllldddd
# |uhlldddd
# |Hhlldddd
# |ulhldddd
# |Hlhldddd
# |ullhdddd
# |Hllhdddd
# |ulllhhhh
# |Hlllhhhh
# |uhllhhhh
# |Hhllhhhh
# |ulhlhhhh
# |Hlhlhhhh
# |ullhhhhh
# |Hllhhhhh
# |ulllHHHH
# |HlllHHHH
# |uhllHHHH
# |HhllHHHH
# |ulhlHHHH
# |HlhlHHHH
# |ullhHHHH
# |HllhHHHH

#Treino rockyou



class Mask:
  def __init__(self, mask, count):
    self.mask = mask
    self.count = count

def HashcatPatternSearcher(wordlist):

    print(wordlist)
    masks = []
    masks.append(Mask("('d')", 1))

    for word in wordlist:
        length = int(len(word))-1
        print("Word: ", word)
        print("Length: ", length)
        word_matrix = []
        for char in range(0, length):
            char_matrix = []
            if (bool(re.search('[a-z]', word[char]))):
                char_matrix.append("l")
            if (bool(re.search('[A-Z]', word[char]))):
                char_matrix.append("u")
            if (bool(re.search('[0-9]', word[char]))):
                char_matrix.append("d")
            if (bool(re.search('[a-f0-9]', word[char]))):
                char_matrix.append("h")
            if (bool(re.search('[A-F0-9]', word[char]))):
                char_matrix.append("H")
            if (bool(re.search('[^a-zA-Z0-9]', word[char]))):
                char_matrix.append("s")

            #best char finder to a better performance (less groups to combine)
            if char_matrix == ['d', 'h', 'H']:
                char_matrix = ['d']
            if char_matrix == ['l', 'h']:
                char_matrix = ['h']
            if char_matrix == ['u', 'H']:
                char_matrix = ['H']

            word_matrix.append(char_matrix)
        print("Masks: ", word_matrix)
        print()

        iterations = list(itertools.product(*word_matrix))
        print(sum(map(len, iterations)), "iterations")

        for subset in iterations:
            mask_temp = Mask(subset, 1)
            for i in masks:
                if i.mask == subset:
                    i.count = i.count+1
            else:
                masks.append(mask_temp)
    newlist = sorted(masks, key=lambda x: x.count, reverse=False)
    for x in newlist:
        print(x.mask, x.count)
