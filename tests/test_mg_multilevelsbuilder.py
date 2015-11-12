import unittest
import numpy as np
import mg.options as opts
import mg.multilevelsbuilder as multilevels

class TestMultiLevelBuilder(unittest.TestCase):
    def setUp(self):
        self.options = opts.Options()
        self.domain = [1.0, 1.0]

        lmbd = np.array([np.pi/self.domain[0],np.pi/self.domain[1]])
        k1 = lambda x1, x2 : np.full(x1.shape,1.0); 
        k2 = lambda x1, x2 : np.full(x1.shape,1.0)
        rhs = lambda x1, x2 : lmbd[0]**2*np.sin(lmbd[0]*x1)*np.sin(lmbd[0]*x2)+lmbd[1]**2*np.sin(lmbd[1]*x1)*np.sin(lmbd[1]*x2)
        exact = lambda x1, x2 : np.sin(lmbd[0]*x1)*np.sin(lmbd[0]*x2)
        problem = opts.Problem(self.domain, k1, k2, rhs, exact, exact)

        self.ml_builder = multilevels.MultiLevelBuilder(self.options, problem)
        
    def test___init__(self):
        self.assertEqual(7,self.ml_builder.options.num_levels)

    def test_build(self):
        self.ml_builder.build()
        self.assertEqual(self.ml_builder.options.num_levels,len(self.ml_builder.levels))

if __name__ == '__main__':
    unittest.main()
