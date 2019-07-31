"""
This script is a wrapper for a single parameterisation for a simulation on the UCL cluster.
"""

from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('config')
parser.add_argument('variable')
parser.add_argument('value')
args = parser.parse_args()

print(f"args are {args.config}, {args.variable}, {args.value}")


"""
Inputs:
    arg1: default config, need to serialise config object to and from text files PATH TO CONFIG OBJ SAVED IN DIR
    arg2: single variable, name of variable to be changed
    arg3: single value, value of the variable 
    
Method:
    
    load config 
    if population, create state/population named tuples, (remember to change the socialNormID too) 

Output:
    txt file: give it a ID (same as job id) -> post simulation need to accumulate all into excel

"""

if __name__ == '__main__':
    pass
