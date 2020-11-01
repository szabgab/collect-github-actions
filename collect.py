import argparse
import glob
import os
import re
import subprocess
import tempfile
import yaml
from pymongo import MongoClient


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
                dir_name = self.get_repo_name(repo)
                if dir_name is None:
                    continue

                if not self.clone_repository(repo):
                    continue

                self.list_yaml_files(dir_name)


                self.count += 1
                if self.args.limit and self.count >= self.args.limit:
                    break


        except Exception as err:
            print(err)
        os.chdir(original_dir)

    def list_yaml_files(self, dir_name):
        dir_path = os.path.join(dir_name, '.github', 'workflows')
        if not os.path.exists(dir_path):
            print(f"Could not find workflows directory in '{dir_path}'")
            return []
        files = glob.glob(os.path.join(dir_path, '*.yml')) + glob.glob(os.path.join(dir_path, '*.yaml'))
        print(files)
        for filename in files:
            with open(filename) as fh:
                config_data = yaml.load(fh, Loader=yaml.Loader)
                print(config_data)


    def get_repo_name(self, repo):
        match = re.search(r'([^/]+)/?$', repo)
        if not match:
            print("Could not figure out the actual name of this repo")
            return None
        return match.group(1)

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