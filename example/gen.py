import numpy
import os

numpy.random.seed(0)

# generate test data sets

def write(prefix, data):
	if not os.path.exists(prefix):
		os.mkdir(prefix)
	for i, (x, y) in enumerate(data):
		numpy.savetxt('%s/chain%02d' % (prefix, i), numpy.transpose([x, y]))


# random
write('random', [[numpy.random.normal(x, 0.1, size=50), numpy.random.normal(y, 0.1, size=50)]
	for x, y in zip(numpy.random.uniform(0, 1, size=100), numpy.random.uniform(0, 1, size=40))])

# perfect line
write('line', [[numpy.random.normal(x, 0.1, size=50), numpy.random.normal(x*2 + 0.1, 0.1, size=50)]
	for x in numpy.random.uniform(0, 1, size=40)])

# line with systematic error
write('sysline', [[numpy.random.normal(x, 0.1, size=50), numpy.random.normal(numpy.random.normal(x*2 + 0.1, 0.3), 0.1, size=50)]
	for x in numpy.random.uniform(0, 1, size=40)])



