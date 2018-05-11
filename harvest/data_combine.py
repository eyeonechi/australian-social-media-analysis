"""
COMP90024 Cluster and Cloud Computing
Semester 1 2018
Assignment 2 - Australian Social Media Analysis
data_combine.py

Team 42
963370 Thuy Ngoc Ha
824371 Lan Zhou
950618 Zijian Wang
736901 Ivan Chee
824325 Duer Wang
"""

from util.argument import Argument
from util.config import Config

with open(args.input, 'r') as input:
    with open(args.output, 'a') as output:
        for line in input:
            output.write(line)
