#!/usr/bin/env python3

import argparse
import datetime
import os
import subprocess

OPERF_BINARY = '/Users/ctk21/proj/operf-micro/test/bin/operf-micro'
BENCHMARKS = [
	'almabench',
	'nucleic',
	'boyer',
	'kb',
	'num_analysis',
	'bigarray_rev',
	'fibonnaci',
	'lens',
	'vector_functor',
	'kahan_sum',
	'hamming',
	'sieve',
	'list',
	'format',
	'fft',
	'bdd',
	'sequence',
	'nullable_array',
	]
DEFAULT_TIME_QUOTA = 5.0

parser = argparse.ArgumentParser(description='Run operf-micro and collate results')
parser.add_argument('bindir', type=str, help='binary directory of ocaml compiler to use')
parser.add_argument('outdir', type=str, help='output directory for results')
parser.add_argument('--results_timestamp', type=str, help='explicit timestamp to use', default=datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
parser.add_argument('--benchmarks', type=str, help='comma seperated list of benchmarks to run', default=','.join(BENCHMARKS))
parser.add_argument('--time_quota', help='time_quota for operf-micro (default: %s)'%DEFAULT_TIME_QUOTA, default=DEFAULT_TIME_QUOTA)
parser.add_argument('--operf_binary', type=str, help='operf binary to use', default=OPERF_BINARY)
parser.add_argument('-v', '--verbose', action='store_true', default=False)

args = parser.parse_args()

def shell_exec(cmd, verbose=args.verbose, check=True):
	if verbose:
		print('+ %s'%cmd)
	subprocess.run(cmd, shell=True, check=check)

# setup the directories
bindir = os.path.abspath(args.bindir)
outdir = os.path.abspath(args.outdir)
resultdir = os.path.join(outdir, args.results_timestamp)

shell_exec('mkdir -p %s'%resultdir)

# get git source and checkout the hash
if args.verbose: print('changing working directory to %s to run operf-micro'%resultdir)
os.chdir(resultdir)

tag = 'Test%s'%datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

def operf_cmd(s):
	return '%s %s'%(args.operf_binary, s)

shell_exec(operf_cmd('clean'), check=False) ## TODO: sometimes this fails, what is the correct thing to do?
shell_exec(operf_cmd('init --bin-dir %s %s'%(bindir, tag)))
shell_exec(operf_cmd('build'))

for b in args.benchmarks.split(','):
	try:
		print('%s: running %s'%(str(datetime.datetime.now()), b))
		shell_exec(operf_cmd('run --time-quota %s -o %s %s'%(args.time_quota, resultdir, b)))
		shell_exec(operf_cmd('results %s --selected %s --more-yaml > %s.summary'%(tag, b, os.path.join(resultdir, b))))
	except:
		print('ERROR: operf run failed for %s'%b)
