import unittest
import mg.smoother as smoother

class TestGSSmoother(unittest.TestCase):
    def test___init__(self):
        g_s_smoother = smoother.GSSmoother()
        self.assertEqual("Gauss-Seidel", g_s_smoother.name)

if __name__ == '__main__':
    unittest.main()
