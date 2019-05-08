import numpy as np

x = [5.0, 5.0, 6.0, 9.0, 10.0]

eps = 0.001

def lap(v, epsilon):
  return v + np.random.laplace(loc=0,scale=1/epsilon)

def pert(v):
  return lap(v,eps)

def perturb(l):
  return map(pert,l)

def dev(counts):
  rhs = sum(counts)/len(counts)
  return sum(map(lambda c: abs(c - rhs),counts))

def index(l,idxs):
  return list(map(lambda i: l[i], idxs))

def group(counts,eps,thresh):
  output = []
  thresh1 = thresh
  for i in range(len(counts)):
    print(f'partition before time {i} is {output}')
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
        print("here")
      else:
        output.append([i])
        closed = True
        print("here1")
  return output
