import numpy as np

class Interpolator :
	def __init__(self) :
		self.nf = None; self.nc = None
		
	def interpolate(self, uc, coarse_level, fine_level) :
		self.nf = fine_level.n, self.nc = coarse_level.n
		u = np.zeros(self.nf)

		u[::2,::2] = uc
		u[1::2,::2] = 0.5*(uc[:self.nc-1,:] + uc[1:,:])
		u[::2,1::2] = 0.5*(uc[:,:self.nc-1] + uc[:,1:])
		u[1::2,1::2] = 0.5*(uc[:self.nc-1,:self.nc-1] + uc[1:,1:])

		return u

class Restrictor:
	def __init__(self) :
		self.nf = None; self.nc = None

	def restrict(self,f) :
		return f[::2,::2]

