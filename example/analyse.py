import sys, os
import numpy
import scipy, scipy.stats
import syscorr
from syscorr.binned import BinnedModel
from syscorr.poly import PolyModel

# handle command line arguments
output_basename = sys.argv[1]
files = sys.argv[2:]
resume = os.environ.get('RESUME', '0') == '1'

# choose models
example_models = dict(
	# y is drawn independently of x, from a gaussian. 2 free parameters (stdev, mean)
	independent_normal = PolyModel(1, rv_type = scipy.stats.norm),

	# y is drawn independently of x, from a uniform dist. 2 free parameters (width, low)
	independent_uniform = PolyModel(1, rv_type = scipy.stats.uniform),

	# y is drawn as a function of x, with gaussian systematic scatter 
	# y ~ N(b*x + a, s)      3 free parameters (s, a, b)
	line = PolyModel(2),

	# y is drawn as a function of x, with gaussian systematic scatter 
	# y ~ N(c*x**2 + b*x + a, s)      4 free parameters (s, a, b, c)
	square = PolyModel(3),
	
	# two gaussians before and after 0. 4 parameters (means and stdevs)
	tribinned = BinnedModel(bins = [(-0.5, 0.3), (0.3, 0.8), (0.8, 1.5)], rv_type = scipy.stats.norm)
)

# allow choosing model via environment variable
modelnames = os.environ.get('MODELS', '').split()
if len(modelnames) == 0:
	modelnames = example_models.keys()

models = []
for m in modelnames:
	print 'using model:', m
	model = example_models[m]
	models.append((m, model))

# load data
print 'loading data...'
chains = [(f, numpy.loadtxt(f)) for f in files]
print 'loading data done.'

syscorr.calc_models(models=models, 
	chains=chains, 
	output_basename=output_basename, 
	resume=resume)

