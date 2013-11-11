SysCorr - Bayesian correlation swiss army knife
=================================================

Tests correlations between datapoints with uncertainties.

What can it do?
-----------------
* Testing if correlation exists (vs independence)
* Estimating parameters of the dependence (line + systematic error, or higher-order polynomial, ...)
* Plot the resulting correlation with its uncertainty
* Hierarchical Bayesian analysis (with intermediate prior)

Usage
-------

* Provide the individual data points (see below)
* Choose all the models you would like to run
** Uncorrelated uniform distributions
** Uncorrelated gaussian distributions
** Line with systematic error
** Square law with systematic error
** etc.
* Run. This will automatically
** estimate parameters for the chosen models
** compute the evidence for the chosen models
** plot the model posterior predictions with uncertainties
** select the best model
** print the parameters with uncertainties
* (optional) Plot marginal distributions using multinest_marginals.py

Follow the manual for details.

Requirements
-------------

* pymultinest
* jbopt
* uncertainties
* numpy/scipy
* matplotlib

Data Input format
------------------
For maximum flexibility, the data points have to be provided as Markov Chains (points of equal weight),
with one chain file per data point.
The first and second column specify the x and y data.

For example, creating a chain for a datapoint at (2, 3) with normal errors 0.1 in both dimensions::

	x = numpy.random.norm(2, 0.1, size=100)
	y = numpy.random.norm(2, 0.1, size=100)
	chain = numpy.transpose([x, y])
	numpy.savetxt('datapoint01.txt', chain)

This allows specifying correlated errors, and handing over analysis results from
Monte Carlo analyses (e.g. MCMC, MultiNest) output.

The application (see the example) is then called like so::

	$ python analyse.py out/ datapoint01.txt datapoint02.txt ...


