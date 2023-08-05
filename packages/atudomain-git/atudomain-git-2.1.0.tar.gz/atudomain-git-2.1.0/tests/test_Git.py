import unittest

from atudomain.git.Git import Git


class GitTest(unittest.TestCase):
    def setUp(self) -> None:
        self.git = Git('.')

    def test_something(self) -> None:
        print("Nevermind")


if __name__ == '__main__':
    unittest.main()
