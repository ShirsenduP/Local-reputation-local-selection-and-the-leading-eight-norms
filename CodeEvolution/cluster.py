"""
This script is a wrapper for a single parameterisation for a simulation on the UCL cluster only for LrGe networks.
"""

from argparse import ArgumentParser

from CodeEvolution.Experiment import Experiment
from CodeEvolution.agent import LrGe_Agent
from CodeEvolution.config import Config, State
from CodeEvolution.network import LrGe_Network

parser = ArgumentParser()
parser.add_argument('index', type=int)
parser.add_argument('variable', type=str)
parser.add_argument('value', type=float)
args = parser.parse_args()

print(f"args are {args.variable} and {args.value}")

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
    defaultConfig = Config(initialState=State(mainID=0, proportion=1, mutantID=8))
    setattr(defaultConfig, args.variable, args.value)

    output = Experiment.simulate(m_exp=defaultConfig, networkType=LrGe_Network, displayFull=False)

    with open(f'{args.index}.txt', 'w+') as results:
       results.write(output)