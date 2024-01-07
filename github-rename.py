import argparse
import os
import subprocess


def handle_dir(dir_path: str, max_depth: int, pattern: str, replacement: str) -> None:
	for entry in os.listdir(dir_path):
		entry_path = os.path.join(dir_path, entry)
		if os.path.isdir(entry_path):
			if os.path.isdir(os.path.join(entry_path, '.git')):
				git_repo_rename(entry_path, pattern, replacement)
			if entry != '.git' and max_depth > 1 and os.access(entry_path, os.W_OK | os.R_OK):
				handle_dir(entry_path, max_depth - 1, pattern, replacement)  # Recurse


def git_repo_rename(repo_path: str, pattern: str, replacement: str) -> None:
	if not os.path.isdir(os.path.join(repo_path, '.git')):
		print('Not a git repo: {}'.format(repo_path))
		return

	git_check_remotes = subprocess.Popen(['git', 'remote', '-v'], cwd=repo_path, stdout=subprocess.PIPE)
	git_check_remotes.wait()
	if git_check_remotes.returncode != 0:
		print(f'Failed to check remotes for {repo_path}')
		return

	git_remotes = []
	git_check_remotes_output = git_check_remotes.stdout.read().decode('utf-8')
	for line in git_check_remotes_output.split('\n'):
		if '(fetch)' in line:
			line = line.replace('(fetch)', '').strip()
			remote_name, remote_url = line.split('\t')
			git_remotes.append({'name': remote_name, 'url': remote_url})

	for git_remote in git_remotes:
		new_url = git_remote['url'].replace(pattern, replacement)
		if new_url != git_remote['url']:
			print('Updating remote {} from {} to {}'.format(git_remote['name'], git_remote['url'], new_url))
			git_remote_update = subprocess.Popen(['git', 'remote', 'set-url', git_remote['name'], new_url], cwd=repo_path)
			git_remote_update.wait()
			if git_remote_update.returncode != 0:
				print('Failed to update remote {} from {} to {}'.format(git_remote['name'], git_remote['url'], new_url))


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Rename a GitHub repo')
	parser.add_argument('--recursive', '-r', action='store_true', help='Recursively search for repos')
	parser.add_argument('--max-depth', '-d', type=int, default=1000, help='Maximum recursion depth')
	parser.add_argument('pattern', help="e.g. 'git@github.com:oldname/'")
	parser.add_argument('replacement', help="e.g. 'git@github.com:newname/'")
	parser.add_argument('dir_path', help='Directory to search for repos')
	args = parser.parse_args()

	if args.recursive:
		handle_dir(args.dir_path, args.max_depth, args.pattern, args.replacement)
	else:
		git_repo_rename(args.dir_path, args.pattern, args.replacement)
