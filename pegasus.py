# based on https://people.cs.umass.edu/~miklau/assets/pubs/dp/Chen17PeGaSus.pdf
import numpy as np
import copy
import statistics as stats

ex = [5.0, 5.0, 6.0, 9.0, 10.0]
ex2 = [5.6, 4.4, 6.7, 9.5, 10.2]
ex3 = [[[0]], [[0, 1]], [[0, 1, 2]], [[0, 1, 2], [3]], [[0, 1, 2], [3], [4]]]


eps = 0.001
eps = 1

def lap(v, epsilon):
  return v + np.random.laplace(loc=0,scale=1/epsilon)

def pert(v):
  return lap(v,eps)

def perturb(l):
  return list(map(pert,l))

def dev(counts):
  rhs = sum(counts)/len(counts)
  return sum(map(lambda c: abs(c - rhs),counts))

def index(l,idxs):
  return list(map(lambda i: l[i], idxs))

def smooth(cs,ps):
  if len(cs) != len(ps):
    raise Exception('arg length mismatch')
  else:
    newcs = []
    for i in range(len(cs)):
      p = ps[i]
      g = p[-1]
      newcs.append(stats.median(index(cs,g)))
    return newcs

def group(counts,eps,thresh):
  final_output = []
  output = []
  thresh1 = thresh
  for i in range(len(counts)):
    if i == 0:
      g = []
      closed = True
    else:
      g = output[-1]
    if closed:
      output.append([i])
      closed = False
      thresh1 = lap(thresh,4.0/eps)
    else:
      g1 = g.copy()
      g1.append(i)
      if (lap(dev(index(counts,g1)),8.0/eps)) < thresh1:
        g = output.pop()
        g.append(i)
        output.append(g)
        closed = False
      else:
        output.append([i])
        closed = True
    print(f'partition at time {i} is {output}')
    final_output.append(copy.deepcopy(output))
  return final_output
