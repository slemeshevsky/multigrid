from smoother import *
from level import *
from options import *

def mgc(level, options, u) :
	# Pre-smoothing iterations
	for i in range(options.num_presweeps) :
		smooth = level.sweep(u)

	# Coarse grid correction
	r = level.residual(smooth)
	level.coarse_level.f = level[1].restrict(r)
	vc = np.zeros(level.coarse_level.n)
	if(level.number == 0) :
		for i in range(options.num_coarsest_sweeps) :
			vc = level.sweep(vc)
	else :
		for i in range(options.cycle_index) :
			vc = mgc(level.coarse_level, options, vc)

	# Interpolate error
	v = level.interpolate(vc)
	u += v

	# Post-smoothing iterations
	for i in range(options.num_postsweeps) :
		u = level.sweep(u)

	return u
