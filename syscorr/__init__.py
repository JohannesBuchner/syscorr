import pymultinest
import matplotlib.pyplot as plt, matplotlib.patches as patches
import numpy
import scipy, scipy.stats
from numpy import log, exp

def multinest(parameter_names, transform, loglikelihood, output_basename, **problem):
	parameters = parameter_names
	n_params = len(parameters)
	
	def myprior(cube, ndim, nparams):
		params = transform([cube[i] for i in range(ndim)])
		for i in range(ndim):
			cube[i] = params[i]
	
	def myloglike(cube, ndim, nparams):
		l = loglikelihood([cube[i] for i in range(ndim)])
		return l
	
	# run MultiNest
	mn_args = dict(
		outputfiles_basename = output_basename,
		resume = problem.get('resume', False), 
		verbose = True,
		n_live_points = problem.get('n_live_points', 400))
	if 'seed' in problem:
		mn_args['seed'] = problem['seed']
	pymultinest.run(myloglike, myprior, n_params, **mn_args)

	import json
	# store name of parameters, always useful
	with file('%sparams.json' % output_basename, 'w') as f:
		json.dump(parameters, f, indent=2)
	# analyse
	a = pymultinest.Analyzer(n_params = n_params, 
		outputfiles_basename = output_basename)
	s = a.get_stats()
	with open('%sstats.json' % a.outputfiles_basename, mode='w') as f:
		json.dump(s, f, indent=2)
	return a

def calc_model(output_basename, chains, model, modelname, **args):
	model.chains = chains

	mins = None
	maxs = None
	for f, v in chains:
		newlimits = [v.min(axis=0), v.max(axis=0)]
		if mins is None:
			mins, maxs = newlimits
		for i, newmin in enumerate(newlimits[0]):
			mins[i] = min(mins[i], newmin)
		for i, newmax in enumerate(newlimits[1]):
			maxs[i] = max(maxs[i], newmax)
	print 'running multinest on model "%s" (saving to "%s")' % (modelname, output_basename)
	
	a = multinest(
		parameter_names=model.parameter_names,
		transform=model.transform,
		loglikelihood=model.loglikelihood,
		output_basename=output_basename, **args)
	
	print 'Analysing multinest output...'
	logZ = a.get_stats()['global evidence'] / numpy.log(10)
	
	plt.figure(figsize=(7,7))
	x = numpy.linspace(mins[0], maxs[0], 400)
	rows = a.get_equal_weighted_posterior()[:,:-1]
	ids = range(len(rows))
	numpy.random.shuffle(ids)
	rows = rows[ids[::40],:]
	models = [model.model(row) for row in rows]
	for q in 0.1, 0.5, 0.9:
		for m in models:
			y = [m([xi]).ppf(q) for xi in x]
			plt.plot(x, y, '-', alpha=0.3 if q == 0.5 else 0.1, color='red' if q == 0.5 else 'grey')
	plt.xlim(mins[0], maxs[0])
	plt.ylim(mins[1], maxs[1])
	plt.title('Model "%s" ($\log Z=%.1f$)' % (modelname, logZ))
	plt.savefig('%spost_model.pdf' % output_basename)
	# add data points
	for f, v in chains:
		x0, y0 = v.min(axis=0)
		x1, y1 = v.max(axis=0)
		plt.gca().add_patch(patches.Rectangle((x0, y0), x1 - x0, y1 - y0, edgecolor='blue', facecolor='None', ls='solid'))
		plt.plot(numpy.median(v[:,0]), numpy.median(v[:,1]), 'x', color='blue')
	plt.savefig('%spost_model_data.pdf' % output_basename)
	plt.close()
	print 'posterior plot written to "%spost_model_data.pdf"' % output_basename
	#a.get_equal_weight_points
	return dict(logZ=logZ, stats=a.get_stats())


def calc_models(models, chains, output_basename, **problem):
	results = []
	keys = []
	for modelname, model in models:
		keys.append(modelname)
		res = calc_model(chains=chains, modelname = modelname, 
			model=model, output_basename=output_basename + modelname, **problem)
		results.append((modelname, model, res))
	
	results = sorted(results, key=lambda (modelname, model, res): res['logZ'])
	bestmodelname, bestmodel, bestresults = results[-1]
	logZmax = bestresults['logZ']
	
	print
	print 'calculation results:', '='*40
	print
	print '%20s | %s' % ('model name', 'log Z')
	for modelname, model, res in results:
		print '%20s : %3.1f %s' % (modelname, res['logZ'], '<- BEST MODEL' if bestmodelname == modelname else '')
	
	print
	print 'Parameters for model "%s":' % (bestmodelname)
	stats = bestresults['stats']
	for p, s in zip(bestmodel.parameter_names, stats['marginals']):
		try:
			import uncertainties
			v = str(uncertainties.Variable(s['median'], s['sigma']))
		except:
			v = '%.5f +- %.5f' % (s['median'], s['sigma'])
		print '%20s: %s' % (p, v)
	
	
	


