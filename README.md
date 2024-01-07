# github-profile-rename
Small python script to change git remote urls after profile rename.

### Usage
```
usage: github-rename.py [-h] [--recursive] [--max-depth MAX_DEPTH]
                        pattern replacement dir_path

positional arguments:
  pattern               e.g. 'git@github.com:oldname/'
  replacement           e.g. 'git@github.com:newname/'
  dir_path              Directory to search for repos

options:
  -h, --help            show this help message and exit
  --recursive, -r       Recursively search for repos
  --max-depth MAX_DEPTH, -d MAX_DEPTH
                        Maximum recursion depth
```
