# -*- conding:utf-8 -*-
# Ip address aggregation and sorting

__author__  = 'babyshen'
__version__ = '2.0.0'

import ipaddress
import sys
import argparse

def ip_main(sourcefile,outputfile,*args,**kwargs):
    try:
        with open(sourcefile,'r',encoding='utf-8') as f:
            allip = f.readlines()
        ip = [ipaddress.IPv4Network(net.strip('\n ')) for net in allip]
        ip2 = [addr for addr in ipaddress.collapse_addresses(ip)]

        with open(outputfile,'w',encoding='utf-8') as f1:
            for i in ip2:
                f1.write(str(i)+'\n')
    except Exception as e :
        sys.exit(e)

def args_parser():
    description="""Ip address aggregation and sorting,
                source and output files can be either the same or different. """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-V', '--version', action='version', version='%(prog)s '+__version__)
    parser.add_argument('-s','--sourcefile',help='IPAddress source file',required=True)
    parser.add_argument('-o','--outputfile',help='output file',required=True)
    args = parser.parse_args()
    return args.sourcefile,args.outputfile

if __name__ == '__main__':
    try:
        sourcefile,outputfile = args_parser()
        ip_main(sourcefile,outputfile)
    except Exception as e:
        sys.exit(e)
