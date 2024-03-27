#!/usr/bin/env python3
import argparse
import sys
sys.path.append('../../')
from Drain import LogParser


def parse(input_dir,log_file,output_dir):
    log_format = '<Date> <Time>,<Pid> <Level> <Component>: <Content>' # HDFS log format
    regex      = [
        r'blk_(|-)[0-9]+' , # block id
        r'(/|)([0-9]+\.){3}[0-9]+(:[0-9]+|)(:|)', # IP
        r'(?<=[^A-Za-z0-9])(\-?\+?\d+)(?=[^A-Za-z0-9])|[0-9]+$', # Numbers
    ]
    st         = 0.5  # Similarity threshold
    depth      = 4  # Depth of all leaf nodes
    parser = LogParser(log_format,indir=input_dir,outdir=output_dir,depth=depth,st=st,rex=regex)
    parser.parse(log_file)

def main():
    arg_parser = argparse.ArgumentParser(description='Please specify the input dir, the log file and the output dir.')
    arg_parser.add_argument('-i',metavar = 'Input Dir',type=str,help='specify the input dir.')
    arg_parser.add_argument('-l',metavar ='Log File',type=str,help='specify the name of the input log file.')
    arg_parser.add_argument('-o',metavar='Output Dir',type=str,help='specify the output dir.')
    args = arg_parser.parse_args()
    input_dir = args.i
    log_file = args.l
    output_dir = args.o
    if input_dir == None or output_dir == None or log_file == None:
        arg_parser.print_help()
        exit(1)
    parse(input_dir, log_file, output_dir)
        
    
if __name__ == "__main__":
    main()