from HashcatPatternSearcher import HashcatPatternSearcher
import time
import sys

file = sys.argv[1]

def main():
    start_time = time.time()
    f = open(file, "r")
    wordlist = f.readlines()
    HashcatPatternSearcher(wordlist)
    f.close()
    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    main()
