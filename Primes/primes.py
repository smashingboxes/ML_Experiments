import numpy as np
import random
import alltheprimes
allPrimes = alltheprimes.getAllThePrimes()

MAX_DIGITS = 200

def somePrimes():
  return [ allPrimes[i] for i in sorted(random.sample(xrange(len(allPrimes)), 2000)) ]

def primes(n, start=0):
  primeSubList = thePrimes[start:(n+start)]
  return primeSubList

def primeToArray(prime):
  outputSplitList = list(0.0 for d in range(0,MAX_DIGITS))
  outputSplitListLen = len(outputSplitList)

  primeStringList = list((float(d) / 10.0) for d in str(prime))
  primeStringLen = len(primeStringList)

  index = outputSplitListLen - primeStringLen
  for digit in primeStringList:
    outputSplitList[index] = digit
    index += 1

  # print(outputSplitList)
  return outputSplitList

def mixedData():
  thePrimes = somePrimes()
  notPrimes = list(map(lambda x: x+3, thePrimes))

  # primeSubList = list(map(lambda (i,x): [[x, (x - thePrimes[i-1]) / 2., (thePrimes[i+1] - x) / 2.],1], enumerate(thePrimes[2:-2])))
  # notPrimeSubList = list(map(lambda (i,x): [[x, (x - thePrimes[i-1]) / 2., (thePrimes[i+1] - x) / 2.],0], enumerate(notPrimes[2:-2])))
  primeSubList = list(map(lambda (i,x): [primeToArray(x),1], enumerate(thePrimes)))
  notPrimeSubList = list(map(lambda (i,x): [primeToArray(x),0], enumerate(notPrimes)))
  return primeSubList+notPrimeSubList

primeToArray(100)
