######################################################################
# Gauss-Seidel sweep for solving disctrete elliptic Dirichlet problem
#
# u[i1,i2] is approcximate solution (initial guess) at grid point (i_1h,i_2h)
# A1[i1,i2] is the value of coefficient k1(i_1h, i_2h)/h_1^2
# A2[i1,i2] is the value of coefficient k2(i_1h, i_2h)/h_2^2
# F[i1,i2] is the value h^2f(i_1h,i_2h)
#
######################################################################
import numpy as np
from level import *

class GSSmoother :
	def __init__(self) :
		self.u = None; self.name = "Gauss-Seidel"
		
	def sweep(self, level, guess) :
		u = guess
		N1 = u.shape[0]-1
		N2 = u.shape[1]-1
	
		u[1:N1,1:N2] = level.f[1:N1,1:N2] + \
		  level.A1[1:N1,1:N2]*u[:N1-1,1:N2] + \
		  level.A1[2:,1:N2]*u[2:,1:N2] + \
		  level.A2[1:N1,1:N2]*u[1:N1,:N2-1] + \
		  level.A2[1:N1,2:]*u[1:N1,2:]

		u[1:N1,1:N2] /= (level.A1[1:N1,1:N2]+level.A1[2:,1:N2] + \
		                 level.A2[1:N1,1:N2]+level.A2[1:N1,2:])
		return u
