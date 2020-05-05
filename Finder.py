from HashcatPatternSearcher import HashcatPatternSearcher
import time
import os
import argparse

def main():

    start_time = time.time()

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', default='testlist.txt', help='File: clear passwords to verify patterns')
    parser.add_argument('-o', type=int, default=4, help='Occurrence: Minimum occurrence of hashcat mask in list')
    parser.add_argument('-c', type=int, default=5, help='Chars: Minimum chars in hashcat mask mask')
    parser.add_argument('-d', type=bool, default=False, help='Debug mode')
    args = parser.parse_args()

    file = args.f
    minimumcount = args.o
    minimummask = args.c
    debug = args.d

    print(args)

    if os.path.isfile(file):
        f = open(file, "r")
        wordlist = f.readlines()
        f.close()
        bestmasks = HashcatPatternSearcher(wordlist, minimumcount, debug)

        # Order and filter by minimumcount defined
        orderedlist = sorted(bestmasks, key=lambda x: x.count, reverse=False)

        #print(dict(filter(lambda x: x.length >= minimummask, orderedlist)))

        for y in orderedlist:
            y.length = len(y.mask)
            if (y.count >= minimumcount) and (y.length >= minimummask):
                var = ""
                for z in range(0, len(y.mask)):
                    var = var + "?" + y.mask[z]
                print(y.count, var)

    else:
        print("Missing file (clear text passwords). Please verify if file exists!")

    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    main()
