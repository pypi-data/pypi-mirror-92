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
import argparse
import shutil
import sys
import os
from rich.console import Console

console = Console()

def rename(path, old_key, new_key, preview):
    files = sorted([f for f in os.listdir(path) if old_key in f])
    for f in files:
        old_name = f
        new_name = f.replace(old_key, new_key)
        console.print('[bold cyan]{}[/bold cyan] -> [bold green]{}[/bold green]'.format(old_name, new_name))
        if not preview:
            os.rename(os.path.join(path, old_name), os.path.join(path, new_name))


def copy(path, old_key, new_key, preview):
    files = sorted([f for f in os.listdir(path) if old_key in f])
    for f in files:
        old_name = f
        new_name = f.replace(old_key, new_key)
        console.print('[bold cyan]{}[/bold cyan] -> [bold green]{}[/bold green]'.format(old_name, new_name))
        if not preview:
            shutil.copyfile(os.path.join(path, old_name), os.path.join(path, new_name))

