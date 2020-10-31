import os
import re

class Collector():
    def __init__(self):
        self.root = os.path.dirname(os.path.abspath(__file__))

    def run(self):
        #print(self.root)
        repos = self.get_repos_iterator()
        for repo in repos:
            print(repo)

    def get_repos_iterator(self):
        repos_file = os.path.join(self.root, 'repos.txt')
        with open(repos_file) as fh:
            for row in fh:
                row = row.rstrip("\n")
                if re.search(r'^\s*$', row):
                    continue
                yield row


if __name__ == '__main__':
    Collector().run()