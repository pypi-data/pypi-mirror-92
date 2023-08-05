import unittest

from atudomain.git.Git import Git


class GitTest(unittest.TestCase):
    def setUp(self) -> None:
        self.git = Git('.')

    def test_readonly_methods(self) -> None:
        self.git.get_commits()
        self.git.get_branches()


if __name__ == '__main__':
    unittest.main()
