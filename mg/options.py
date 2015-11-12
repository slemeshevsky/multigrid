from smoother import *
from transfer import *

class Problem :
    def __init__(self, domain, k1, k2, f, bc, u) :
	    self.k1 = k1; self.k2 = k2; self.rhs = f; self.exact = u
	    self.domain = domain; self.bc = bc

class Options :
	def __init__(self) :
		# Number of intervals on coarsest grid
		self.coarsest_n = [4, 4]
		# Number of levels
		self.num_levels = 7
		# Numbers of pre and post smoothing sweeps
		self.num_presweeps = 2; self.num_postsweeps = 1
		# Type of cycle: 1 - V-cycle, 2 - Warning-cycle
		self.cycle_index = 1
		# Number of sweeps on coarsest level
		self.num_coarsest_sweeps = 5
		# Smoother
		self.smoother = GSSmoother()
		self.interpolator = Interpolator()
		self.restrictor = Restrictor()

	def print_log_info(self) :
		if self.cycle_index == 1:
			print "V-cycle options:"
		elif self.cycle_index == 2:
			print "W-cycle options:"
		else:
			print "Other-cycle options:"

		print "\t Numbers of coarsest intervals: [%g, %g]" \
		  % (self.coarsest_n[0], self.coarsest_n[1])
		print "\t Number of presmooth iterations: %g" \
		  % (self.num_presweeps)
		print "\t Number of postsmooth iterations: %g" \
		  % (self.num_postsweeps)
