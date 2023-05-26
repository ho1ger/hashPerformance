import hashlib
import os
import time

import matplotlib.pyplot as plt
import pandas as pd

# this should be all hashes hashlib implements...
hashes = ('md5',
          'sha1', 'sha224', 'sha256', 'sha384', 'sha512',
          'blake2b', 'blake2s',
          'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512',
          'shake_128', 'shake_256')

basePath = "./"
inputDataFiles = ['random_100k.dat', 'random_500k.dat', 'random_1M.dat',
                  'random_5M.dat', 'random_10M.dat']


def hashFile(hash, filePath):
    # ... but at least on MacOS some are not implemented, let's try and see if we
    # get the according hash object
    try: 
        hashObject = getattr(hashlib, hash)()
        with open(filePath, 'rb') as inputDataFile:
            for chunk in iter(lambda: inputDataFile.read(4096), b''):
                hashObject.update(chunk)
        hashObject.hexdigest()
        return True  # all ok
    except:
        print(f"Hash function {hash} not available.")
        return False  # something broken


def runTest(inputDataFile):
    measurements = pd.DataFrame()
    for hash in hashes:
        print(hash)
        repetitions = 50
        iterations = []
        for i in range(0, repetitions):
            start = time.time()
            res = hashFile(hash, filePath)
            end = time.time()
            duration = end - start
            iterations.append(duration)
            # this hash function is not implemented, we don't have to try anymore
            if res is False:
                break
        if res:
            measurements[hash] = iterations
    return measurements


for inputDataFile in inputDataFiles:
    filePath = os.path.join(basePath, inputDataFile)

    res = runTest(filePath)

    plt.figure(figsize=(1200/100, 800/100), dpi=100)
    res.boxplot()
    plt.title(f"Runtimes of different Hash functions -- {inputDataFile}")
    plt.xlabel('Hash Functions')
    plt.ylabel('time [s]')
    plt.xticks(rotation=90)
    plt.tight_layout() 
    plt.savefig(os.path.join(basePath, inputDataFile + ".pdf"))
