import level as lm

class MultiLevelBuilder :
	def __init__(self, opts, problem) :
		self.options = opts; self.problem = problem
		self.levels = []

	def build(self) :
		n = self.options.coarsest_n

		coarsest_level = lm.Level(
			self.problem, n,
			self.options.smoother)
		coarsest_level.print_log_info()
		
		coarsest_level.f = self.problem.rhs(
			coarsest_level.X1,
			coarsest_level.X2)
		# coarsest_level.f[coarsest_level.boundaries] = self.problem.bc(
		# 	coarsest_level.X1[coarsest_level.boundaries], 
		# 	coarsest_level.X2[coarsest_level.boundaries])

		self.levels.append(coarsest_level)
		
		for i in range(1, self.options.num_levels) :
			n *= 2
			level = lm.Level(
				self.problem, n, self.options.smoother,
				self.levels[i-1], self.options.interpolator, 
				self.options.restrictor)
			level.f = self.problem.rhs(level.X1, level.X2)
			level.f[level.boundaries] = self.problem.bc(
				level.X1[level.boundaries], 
				level.X2[level.boundaries])
			level.set_level_number(i)
			self.levels.append(level)
