import unittest


class TestAlwaysTrue(unittest.TestCase):

    def test_assertTrue(self):
        """
        always_true returns a truthy value
        """
        result = True

        self.assertTrue(result)
