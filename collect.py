import argparse
import os
import re
import tempfile
import subprocess

class Collector():
    def __init__(self, args):
        self.root = os.path.dirname(os.path.abspath(__file__))
        self.args = args
        self.count = 0

    def run(self):
        repos = self.get_repos_iterator()
        temp_dir = tempfile.mkdtemp()
        print(temp_dir)
        original_dir = os.getcwd()
        os.chdir(temp_dir)
        try:
            for repo in repos:
                print(repo)
                if not self.clone_repository(repo):
                    continue
                self.count += 1
                if self.args.limit and self.count >= self.args.limit:
                    break


        except Exception as err:
            print(err)
        os.chdir(original_dir)

    def clone_repository(self, repo):
        cmd = ["git", "clone", "--depth", "1", repo]
        proc = subprocess.Popen(cmd,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
        )
        _, _ = proc.communicate()
        return proc.returncode == 0



    def get_repos_iterator(self):
        repos_file = os.path.join(self.root, 'repos.txt')
        with open(repos_file) as fh:
            for row in fh:
                row = row.rstrip("\n")
                if re.search(r'^\s*$', row):
                    continue
                yield row


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()
    Collector(args=args).run()