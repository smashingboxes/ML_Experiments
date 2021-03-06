import os.path
import sys

def factors(limit, start = 0):
  counter = start
  numberMap = []
  while len(numberMap) < limit:
    numList = getfactors(counter)
    # print(counter, numList, '+0')
    numberMap.append([counter, 0.0])

    score = 0.0
    if isPrime(counter+1):
      score = 1.0

    # print(counter+1, numList, '+1', isPrime(counter+1))
    numberMap.append([counter+1, score])
    counter += 2

  print(len(numberMap), limit, start)
  return numberMap

def primesonly(limit, start = 0):
  counter = start
  if (counter != 2 and counter % 2 == 0):
    counter += 1

  if (counter < 2):
    counter += 1

  numberMap = []
  while len(numberMap) < limit:

    if isPrime(counter):
      numberMap.append([counter, 1.0])
      sys.stdout.write("Prime factoring progress: %d   \r" % (len(numberMap)) )
      sys.stdout.flush()

    counter += 1

  print(len(numberMap), limit, start)
  return numberMap

def product(out, x):
  return out * x

def isPrime(num):
  # print(getfactors(num), num)
  if len(getfactors(num)) == 1:
    return True
  return False

def testTracker(tracker, x):
  if tracker % x == 0:
    return x
  else:
    return tracker

def getfactors(num):
  counter = 2
  factors = []
  numtemp = num
  while counter <= numtemp:
    if numtemp % counter == 0:
      factors.append(counter)
      numtemp = numtemp / counter
      while numtemp % counter == 0:
        numtemp = numtemp / counter
        factors.append(counter)
    counter += 1
  return factors

def getFactorsOfNum(num):
  # print('factoring', num)
  factors = []
  tracker = 2
  while tracker <= num:
    if (reduce(testTracker, factors, tracker) == tracker):
      if (num % tracker == 0):
        factors = factors + [tracker]
        if num / tracker >= 2:
          numSmaller = num / tracker
          while numSmaller % tracker == 0:
            factors = factors + [tracker]
            numSmaller = numSmaller / tracker

    tracker+=1
  return factors

