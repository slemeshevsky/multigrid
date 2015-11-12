import unittest
import numpy as np
import mg.options as options

class TestProblem(unittest.TestCase):
    def setUp(self):
	    self.opts = options.Options()
	    self.domain = [1.0, 1.0]
	    self.X1, self.X2 = np.meshgrid(
		    np.linspace(0.,self.domain[0],self.opts.coarsest_n[0]),
	        np.linspace(0.,self.domain[1],self.opts.coarsest_n[1]))
	    lmbd = np.array([np.pi/self.domain[0],np.pi/self.domain[1]])
	    self.k1 = lambda x1, x2 : np.full(x1.shape,1.0); 
	    self.k2 = lambda x1, x2 : np.full(x1.shape,1.0)
	    self.rhs = lambda x1, x2 : lmbd[0]**2*np.sin(lmbd[0]*x1)*np.sin(lmbd[0]*x2)+lmbd[1]**2*np.sin(lmbd[1]*x1)*np.sin(lmbd[1]*x2)
	    self.exact = lambda x1, x2 : np.sin(lmbd[0]*x1)*np.sin(lmbd[0]*x2)

	    self.problem = options.Problem(
		    self.domain, self.k1, self.k2,
		    self.rhs, self.exact, self.exact)

    def test___init__(self):
        self.assertEqual(self.domain, self.problem.domain)

    def test_rhs(self) :
        valid_f = self.rhs(self.X1, self.X2)
        np.testing.assert_array_almost_equal(
            valid_f,
            self.problem.rhs(self.X1,self.X2))

    def test_k1(self) :
        valid_k1 = self.k1(self.X1, self.X2)
        np.testing.assert_array_almost_equal(
            valid_k1,
            self.problem.k1(self.X1,self.X2))
        
    def test_k2(self) :
        valid_k2 = self.k2(self.X1, self.X2)
        np.testing.assert_array_almost_equal(
            valid_k2,
            self.problem.k2(self.X1,self.X2))

    def test_bc(self) :
        valid_bc = self.exact(self.X1, self.X2)
        np.testing.assert_array_almost_equal(
            valid_bc,
            self.problem.bc(self.X1,self.X2))
        
    def test_exact(self) :
        valid_u = self.exact(self.X1, self.X2)
        np.testing.assert_array_almost_equal(
            valid_u,
            self.problem.exact(self.X1,self.X2))
        
if __name__ == '__main__':
    unittest.main()
