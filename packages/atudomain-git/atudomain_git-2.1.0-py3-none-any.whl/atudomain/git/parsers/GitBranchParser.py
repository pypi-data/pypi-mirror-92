import re

from typing import List


class GitBranchParser:
    @staticmethod
    def _extract_branch_strings(
            branches_string: str
    ) -> List[str]:
        return branches_string.split('\n')[:-1]

    def extract_branches(
            self,
            branches_string: str
    ) -> List[str]:
        branch_strings = self._extract_branch_strings(branches_string)
        branches = [
            x.strip().replace('* ', '')
            for x in branch_strings
            if not re.search(r'\s->\s', x)
            and not re.search(r'HEAD detached', x)
        ]
        return branches
