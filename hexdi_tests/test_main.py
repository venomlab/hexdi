import unittest
import os

if __name__ == '__main__':
    loader = unittest.TestLoader()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    start_dir = os.path.join(current_dir, 'tests')
    base_dir = os.path.dirname(current_dir)
    tests = loader.discover(start_dir=start_dir, top_level_dir=base_dir)
    runner = unittest.TextTestRunner()
    runner.run(tests)
