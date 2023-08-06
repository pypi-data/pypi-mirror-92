'''
usage: filenames.py [-h] [--preview] cmd path old_key new_key

positional arguments:
  cmd         command to run [rename] or [copy]
  path        path to directory containing files to rename
  old_key     old key term to replace
  new_key     new key term to replace old with

optional arguments:
  -h, --help  show this help message and exit
  --preview   Only Preview Changes!
'''
import sys
import argparse
from filenames.filenames import copy, rename


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', help = 'command to run [rename] or [copy]')
    ap.add_argument('path', help = 'path to directory containing files to rename')
    ap.add_argument('old_key', help = 'old key term to replace')
    ap.add_argument('new_key', help = 'new key term to replace old with')
    ap.add_argument('--preview', default=False, action='store_true', help = 'Only Preview Changes!')
    args = ap.parse_args()

    cmd = args.cmd
    path = args.path
    old_key = args.old_key
    new_key = args.new_key

    if cmd == 'rename':
        rename(path, old_key, new_key, preview=args.preview)
    if cmd == 'copy':
        copy(path, old_key, new_key, preview=args.preview)


if __name__ == '__main__':
    sys.exit(main())
