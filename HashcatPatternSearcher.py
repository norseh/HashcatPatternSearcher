import re
import itertools

# Hashcat groups for masks:
#?l = abcdefghijklmnopqrstuvwxyz
#?u = ABCDEFGHIJKLMNOPQRSTUVWXYZ
#?d = 0123456789
#?h = 0123456789abcdef
#?H = 0123456789ABCDEF
#?s = «space»!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
#?a = ?l?u?d?s
#?b = 0x00 - 0xff

# Example of complexity
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

#Trainning rockyou after strings in file


class Mask:
  def __init__(self, mask, count):
    self.mask = mask
    self.count = count
    self.length = 0

def HashcatPatternSearcher(wordlist, minimum, debug):

    if debug == True:
        print(wordlist)
    masks = []
    masks.append(Mask("('d')", 1))

    for word in wordlist:
        length = int(len(word))-1
        if debug == True:
            print("Password: ", word, "Length: ", length)
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
        if debug == True:
            print("Reduced mask: ", word_matrix)

        iterations = list(itertools.product(*word_matrix))
        if debug == True:
            print(sum(map(len, iterations)), "iterations")
            print("")

        for subset in iterations:
            mask_temp = Mask(subset, 1)
            for i in masks:
                if i.mask == subset:
                    i.count = i.count+1
            else:
                masks.append(mask_temp)

    uniquemasks = set(mascara.mask for mascara in masks)
    bestmasks = []
    highercountmask = Mask([''], 0)
    for i in uniquemasks:
        #print(len(uniquemasks), i)
        counter = 0
        for j in masks:
            if j.mask == i:
                counter = counter+1
        highercountmask = Mask(i, counter)
        bestmasks.append(highercountmask)
    
    return(bestmasks)
