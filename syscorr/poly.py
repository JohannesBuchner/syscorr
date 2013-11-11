import scipy.stats
import numpy

def poly_transform(u):
	v = numpy.copy(u)
	v[0] = 10**(v[0]*10 - 5)
	v[1:] = 20*v[1:] - 10
	return v

class PolyModel(object):
	"""
	A gaussian (or other) distribution of width 'syserror' around a polynomial
	of the given degree.
	
	degree = 1: 
		y is distributed independently of x. 
		The parameter 'a' specifies the location of the distribution.
	degree = 2: 
		y is correlated with x according to a line, whose parameters are
		y ~ N(a + b*x; syserror)
	degree = 3: 
		same as above with a quadratic function.
	"""
	def __init__(self, degree, rv_type = scipy.stats.norm):
		self.degree = degree
		self.parameter_names = ['syserror'] + ['a', 'b', 'c', 'd', 'e', 'f', 'g'][:degree]
		self.chains = None

		def poly_model(v):
			sys_error = v[0]
			params = v[1:]
			poly = numpy.poly1d(params)
			def model(x):
				y_model = poly(x)
				rv_sys = rv_type(y_model, sys_error)
				return rv_sys
			return model

		def poly_likelihood(v):
			model = poly_model(v)
			like = 0
			for k, c in self.chains:
				x = c[:,0]
				y = c[:,1]
				rv = model(x)
				prob = rv.pdf(y).mean()
				if prob == 0:
					print 'parameters %s ruled out by object %s' % (str(v), k)
					return -1e100
				like += numpy.log(prob)
			return like
		
		self.transform = poly_transform
		self.loglikelihood = poly_likelihood
		self.model = poly_model

