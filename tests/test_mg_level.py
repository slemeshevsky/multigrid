import unittest
import mg.options as options
import mg.smoother as sm
import mg.level as lv
import numpy as np

class TestLevel(unittest.TestCase):
    def setUp(self):
        self.opts = options.Options()
        self.domain = [1.0, 1.0]
        self.smoother = sm.GSSmoother()

        lmbd = np.array([np.pi/self.domain[0],np.pi/self.domain[1]])
        k1 = lambda x1, x2 : np.full(x1.shape,1.0); 
        k2 = lambda x1, x2 : np.full(x1.shape,1.0)
        rhs = lambda x1, x2 : lmbd[0]**2*np.sin(lmbd[0]*x1)*np.sin(lmbd[0]*x2)+lmbd[1]**2*np.sin(lmbd[1]*x1)*np.sin(lmbd[1]*x2)
        exact = lambda x1, x2 : np.sin(lmbd[0]*x1)*np.sin(lmbd[0]*x2)
        problem = options.Problem(self.domain, k1, k2, rhs, exact, exact)
        
        self.level = lv.Level(problem, self.opts.coarsest_n, self.smoother)

        self.u = np.full(self.level.n,1.0)
        self.valid_L_value = self.valid_L(self.u)

    def valid_L(self, u) :
	    lmbd = np.array([np.pi/self.domain[0],np.pi/self.domain[1]])
	    k1 = lambda x1, x2 : np.full(x1.shape,1.0); 
	    k2 = lambda x1, x2 : np.full(x1.shape,1.0)
	    rhs = lambda x1, x2 : lmbd[0]**2*np.sin(lmbd[0]*x1)*np.sin(lmbd[0]*x2)+lmbd[1]**2*np.sin(lmbd[1]*x1)*np.sin(lmbd[1]*x2)
	    exact = lambda x1, x2 : np.sin(lmbd[0]*x1)*np.sin(lmbd[0]*x2)
	    
	    A1 = k1(self.level.X1 - 0.5*self.level.h[0],
	            self.level.X2) / self.level.h[0]**2
	    A2 = k2(self.level.X1, self.level.X2 - 0.5*self.level.h[1]) / self.level.h[1]**2
	    left = exact(self.level.X1[self.level.boundaries[0]], self.level.X2[self.level.boundaries[0]])
	    right = exact(self.level.X1[self.level.boundaries[1]], self.level.X2[self.level.boundaries[1]])
	    bottom = exact(self.level.X1[self.level.boundaries[2]], self.level.X2[self.level.boundaries[2]])
	    top = exact(self.level.X1[self.level.boundaries[3]], self.level.X2[self.level.boundaries[3]])
	    N1 = self.level.n[0]; N2 = self.level.n[1]
	    res = np.zeros(self.level.n)
	    res[1:N1-1,1:N1-1] = - A1[1:N1-1,1:N2-1]*u[:N1-2,1:N2-1] \
	      - A1[2:,1:N2-1]*u[2:,1:N2-1] \
	      - A2[1:N1-1,1:N2-1]*u[1:N1-1,:N2-2] \
	      - A2[1:N1-1,2:]*u[1:N1-1,2:] \
	      + (A1[1:N1-1,1:N2-1]+A1[2:,1:N2-1] \
	         + A2[1:N1-1,1:N2-1]+A2[1:N1-1,2:])*u[1:N1-1,1:N2-1]
	    res[self.level.boundaries[0]] = left
	    res[self.level.boundaries[1]] = right  
	    res[self.level.boundaries[2]] = bottom
	    res[self.level.boundaries[3]] = top
	    return res
	    
    def test_L(self):
        # level = Level(domain, n, smoother, coarse_level, interpolator, restrictor)
        # self.assertEqual(expected, level.L(u))
        np.testing.assert_array_almost_equal(
            self.valid_L_value, self.level.L(self.u))

    def test___init__(self):
        print self.domain
        print self.opts.coarsest_n
        np.testing.assert_array_almost_equal(np.array(self.domain),
                                             self.level.domain) 

    def test_smoother(self):
        self.assertTrue(self.level.smoother)

    def test_interpolator(self):
        self.assertFalse(self.level.interpolator)

    def test_restrictor(self):
        self.assertFalse(self.level.restrictor)
        
    def test_residual(self):
        np.testing.assert_array_almost_equal(
            self.level.f - self.valid_L(self.u), self.level.residual(self.u))

    def test_set_level_number(self):
        self.level.set_level_number(1)
        self.assertEqual(1, self.level.number)

if __name__ == '__main__':
    unittest.main()
