import scipy.stats
import numpy
from numpy import logical_and

def binned_transform(u):
	v = numpy.copy(u)
	v[:len(v)/2] = 20*v[:len(v)/2] - 10
	v[len(v)/2:] = 10**(v[len(v)/2:]*10 - 5)
	return v

class BinnedModel(object):
	"""
	Each bin in the x variable has a distribution (Gaussian or other).
	The bin borders have to be specified.
	"""
	def __init__(self, bins, rv_type = scipy.stats.norm):
		self.bins = bins
		self.parameter_names = ['y%d' % (i+1) for i in range(len(bins))] + ['ys%d' % (i+1) for i in range(len(bins))]
		self.chains = None

		def binned_model(v):
			params = zip(v[:len(v)/2], v[len(v)/2:])
			
			def model(x):
				yvec = numpy.empty_like(x)
				svec = numpy.empty_like(x)
				for j, (lo, hi) in enumerate(bins):
					mask = logical_and(x >= lo, x < hi)
					if mask.any():
						yvec[mask] = params[j][0]
						svec[mask] = params[j][1]
				
				rv = rv_type(yvec, svec)
				return rv
			return model
		
		def binned_likelihood(v):
			model = binned_model(v)
			like = 0
			for k, c in self.chains:
				x = c[:,0]
				y = c[:,1]
				w = c[:,2] if c.shape[1] > 2 else 1
				rv = model(x)
				prob = (rv.pdf(y) * w).mean()
				if prob == 0:
					print 'parameters %s ruled out by object %s' % (str(v), k)
					return -1e100
				like += numpy.log(prob)
			return like
		
		self.transform = binned_transform
		self.loglikelihood = binned_likelihood
		self.model = binned_model

class RvSwitch(object):
	def __init__(self, p, a, b):
		self.p = p
		self.a = a
		self.b = b
	def ppf(self, q):
		return numpy.where(q < self.p, self.a.ppf(q / self.p), self.b.ppf((1 - q) / (1 - self.p)))
	def pdf(self, y):
		return self.a.pdf(y) + self.b.pdf(y)

class BinnedEnableModel(object):
	"""
	The distribution is such that with probability 1-'p', the value is uniformly
	in the 'yzerorange', and with probability 1-'p', the value is distributed
	at location 'y' with width 'ys'.
	Each bin in the x variable has such a distribution with 3 variables. The bin borders have to be specified.
	"""
	def __init__(self, bins, yzerorange, rv_type = scipy.stats.norm):
		self.bins = bins
		self.parameter_names =  ['p%d' % (i+1) for i in range(len(bins))] + \
			['y%d' % (i+1) for i in range(len(bins))] + \
			['ys%d' % (i+1) for i in range(len(bins))]
		self.chains = None

		def binned_model(v):
			params = zip(v[:len(v)/3], v[len(v)/3:2*len(v)/3], v[2*len(v)/3:])
			
			def model(x):
				pvec = numpy.empty_like(x)
				yvec = numpy.empty_like(x)
				svec = numpy.empty_like(x)
				for j, (lo, hi) in enumerate(bins):
					mask = logical_and(x >= lo, x < hi)
					if mask.any():
						pvec[mask] = params[j][0]
						yvec[mask] = params[j][1]
						svec[mask] = params[j][2]
				rv = RvSwitch(pvec, 
					rv_type(yvec, svec), 
					scipy.stats.uniform(yzerorange[0], yzerorange[1] - yzerorange[0]))
				return rv
			return model
		
		def binned_likelihood(v):
			model = binned_model(v)
			like = 0
			for k, c in self.chains:
				x = c[:,0]
				y = c[:,1]
				w = c[:,2] if c.shape[1] > 2 else 1
				rv = model(x)
				prob = (rv.pdf(y) * w).mean()
				if prob == 0:
					print 'parameters %s ruled out by object %s' % (str(v), k)
					return -1e100
				like += numpy.log(prob)
			return like
		
		self.transform = binned_transform
		self.loglikelihood = binned_likelihood
		self.model = binned_model

