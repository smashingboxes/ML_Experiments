import numpy as np
import random
import alltheprimes
allPrimes = alltheprimes.getAllThePrimes()


def somePrimes():
  return [ allPrimes[i] for i in sorted(random.sample(xrange(len(allPrimes)), 2000)) ]


def primes(n, start=0):
  primeSubList = thePrimes[start:(n+start)]
  return primeSubList

def mixedData():
  thePrimes = somePrimes()
  notPrimes = list(map(lambda x: x+3, thePrimes))

  primeSubList = list(map(lambda (i,x): [[x, (x - thePrimes[i-1]) / 2., (thePrimes[i+1] - x) / 2.],1], enumerate(thePrimes[2:-2])))
  notPrimeSubList = list(map(lambda (i,x): [[x, (x - thePrimes[i-1]) / 2., (thePrimes[i+1] - x) / 2.],0], enumerate(notPrimes[2:-2])))
  return primeSubList+notPrimeSubList
