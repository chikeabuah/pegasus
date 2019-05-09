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
      newcs.append(np.median(index(cs,g)))
    return newcs

def old_group(counts,eps,thresh):
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

def AboveThreshold(queries, epsilon, threshold):
    T_hat = lap(threshold, 2/epsilon)

    for i, q in enumerate(queries):
      q_hat = lap(q, 4/epsilon)

      if q_hat > T_hat:
        return i

    return None


# this is epsilon-DP
def group(counts,eps,thresh):
  idx = 0
  groups = []
  while (idx < len(counts)):
    #print(f'slice is {counts[idx:idx]}')
    queries = [dev(counts[idx:p]) for p in range(idx+1, len(counts))]
    #print(f'Queries is: {queries}')
    newIdx = AboveThreshold(queries, eps, thresh)
    if (newIdx is None):
      newIdx = len(counts)
    else:
      newIdx = newIdx + 1
    #print(f'newIdx is: {newIdx}')
    #groups.append(counts[idx:newIdx])
    groups.append(list(range(idx,newIdx)))
    idx = newIdx

  return groups

# this is just postprocessing
def group_postprocess(groups, length):
  output = []
  for t in range(length):
    myOutput = []
    for g in groups:
      if t in g:
        myOutput.append(g[:g.index(t)+1])
        break
      else:
        myOutput.append(g)
    output.append(myOutput)
  return output

print(f'ex is {ex}')
print(f'Group #1 (new): {group(ex, 1.0, 2)}')
print(f'Group #2 (new): {group(ex2, 1.0, 2)}')
print(f'Group #1 (post): {group_postprocess(group(ex, 1.0, 2), len(ex))}')
print(f'Group #2 (post): {group_postprocess(group(ex2, 1.0, 2), len(ex))}')
print(f'Group #1 (old): {old_group(ex, 1.0, 2)}')
print(f'Group #2 (old): {old_group(ex2, 1.0, 2)}')
print(ex)
print(perturb(ex))
print(smooth(perturb(ex), group_postprocess(group(ex, 1.0, 2), len(ex))))
