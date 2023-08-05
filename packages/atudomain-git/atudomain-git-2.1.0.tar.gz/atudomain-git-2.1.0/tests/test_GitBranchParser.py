import os
import unittest

from atudomain.git.parsers.GitBranchParser import GitBranchParser
from ResourceReader import ResourceReader


class GitBranchParserTest(unittest.TestCase):
    RESOURCES_DIR = os.path.dirname(os.path.realpath('__file__')) + '/resources/test_GitBranchParser/'

    def setUp(self) -> None:
        self.git_branch_parser = GitBranchParser()

    def test_extract_branch_strings(self) -> None:
        branches_string_1 = ResourceReader.read(
            file=self.RESOURCES_DIR + 'test__extract_branch_strings_1.txt'
        )

        branch_strings_1 = self.git_branch_parser._extract_branch_strings(
            branches_string=branches_string_1
        )

        self.assertListEqual(
            [
                '  branch/1/2019',
                '  branch/2/2019',
                '  branch/3/2019',
                '* master'
            ],
            branch_strings_1
        )

    def test_extract_branches(self) -> None:
        branches_string_1 = ResourceReader.read(
            file=self.RESOURCES_DIR + 'test_extract_branches_1.txt'
        )
        branches = self.git_branch_parser.extract_branches(
            branches_string=branches_string_1
        )
        self.assertListEqual(
            [
                'master',
                'remotes/origin/master'
            ],
            branches
        )


if __name__ == '__main__':
    unittest.main()
