from util.argument import Argument
from util.config import Config

with open(args.input, 'r') as input:
    with open(args.output, 'a') as output:
        for line in input:
            output.write(line)
