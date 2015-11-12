import numpy as np

class Level:
	def __init__(
			self, problem, n, smoother, coarse_level = None,
			interpolator = None, restrictor = None) :
		self.domain = problem.domain 
		self.h = self.domain/np.array(n)
		self.n = tuple(np.array(n)+1)
		
		self.X1, self.X2 = np.meshgrid(
			np.linspace(0, self.domain[0], self.n[0]), 
			np.linspace(0, self.domain[1], self.n[1]))

		self.boundaries = np.array([
			np.where(self.X1 == 0.0), 
			np.where(self.X1 == self.domain[0]),
			np.where(self.X2 == 0.0),
			np.where(self.X2 == self.domain[1])])
		self.A1 = problem.k1(self.X1 - 0.5*self.h[0], self.X2) / self.h[0]**2
		self.A2 = problem.k2(self.X1, self.X2 - 0.5*self.h[1]) / self.h[1]**2
		
		self.f = problem.rhs(self.X1, self.X2)
		for b in self.boundaries :
			self.f[b] = problem.bc(self.X1[b],self.X2[b])
		
		self.coarse_level = coarse_level
		self.number = 0
		self.smoother = smoother
		self.interpolator = interpolator
		self.restrictor = restrictor

	def residual(self, u) :
		return self.f - self.L(u)

	def L(self, u) :
		N1 = self.n[0]; N2 = self.n[1]
		res = np.zeros(self.n)
		res[1:N1-1,1:N1-1] = - self.A1[1:N1-1,1:N2-1]*u[:N1-2,1:N2-1] \
		  - self.A1[2:,1:N2-1]*u[2:,1:N2-1] \
		  - self.A2[1:N1-1,1:N2-1]*u[1:N1-1,:N2-2] \
		  - self.A2[1:N1-1,2:]*u[1:N1-1,2:] \
		  + (self.A1[1:N1-1,1:N2-1]+self.A1[2:,1:N2-1] \
		     + self.A2[1:N1-1,1:N2-1]+self.A2[1:N1-1,2:])*u[1:N1-1,1:N2-1]

		for b in self.boundaries :
			res[b] = self.f[b]

		return res

	def sweep(self, u) :
		return self.smoother.sweep(self,u)

	def interpolate(self, uc) :
		return self.interpolator.interpolate(uc,self.coarse_level,self)

	def restrict(self, f) :
		return self.restrictor.restrict(f)

	def set_level_number(self, num) :
		self.number = num

	def print_log_info(self) :
		print "Level %g:" % (self.number)
		print "\t Domain: [%f, %f]" % (self.domain[0],self.domain[1])
		print "\t Number of intervals: [%g, %g]" % (self.n[0]-1, self.n[1]-1)
		print "\t Steps =  " % (self.h)
		print "\t f = " % (self.f)
		print "\t X1 = " % (self.X1)
		print "\t X2 = " % (self.X2)
