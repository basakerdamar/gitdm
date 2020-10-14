# Usage: git log --numstat -M v5.4..v5.5 | python get_commits.py -d commits.csv

from gitlog import grabpatch

from patterns import patterns
import subprocess
import argparse

import csv
import sys


p = argparse.ArgumentParser()

p.add_argument('-d', '--dump', help = 'Dump commit list to file',
                   required = False, default = '')

args = p.parse_args()
results = []

input = open(0, 'rb')
patch = grabpatch(input)
while patch:
    current_patch = [patch.commit,
                    patch.date,
                    patch.author.name,
                    ','.join(patch.author.email),
                    ','.join(patch.report),
                    ','.join(patch.reviews),
                    ','.join(patch.ackedbys),
                    ','.join(patch.testedbys),
                    ','.join(patch.signoffs),
                    patch.added,
                    patch.removed,
                    ','.join(patch.files)]
    if not args.dump:
        print(*current_patch)
    results.append(current_patch)
    patch = grabpatch(input)

if args.dump:
    with open(args.dump, 'w', newline='') as csvfile:
        commitmap = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        commitmap.writerow(['commit', 
                            'date', 
                            'author.name', 
                            'author.email', 
                            'reported-by', 
                            'reviewed-by', 
                            'acked-by', 
                            'tested-by', 
                            'signoffs', 
                            'added', 
                            'removed', 
                            'files'])
        commitmap.writerows(results)