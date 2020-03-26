import pandas as pd

from CodeEvolution.models import GrGeERNetwork, LrGeERNetwork, GrLeERNetwork, LrLeERNetwork
from CodeEvolution.config import Config, State
from CodeEvolution.experiment import Experiment

pd.set_option("display.max_rows", None, "display.max_columns", None)
pd.set_option('display.width', 320)

desc = """
Experiment #TEST

Thisd asdjaoidsaoisdaiodaisdsjdia djisd isd aisjd asdjia dsj
asd osdj asofj aisf jisdj aidojfiasjf asjdiaosfjia fiasodasid 
asjdoasdja ifjsof ajsif jfiaosf jiasj igoajsf iaosj aiodj asidjaosi

"""

if __name__=="__main__":

    con = Config(
        initialState=State(0,0.5,8),
        size=300,
        maxPeriods=2000,
        sparseDensity=True,
        mutationProbability=0.1
    )
    E = Experiment(
        description=desc,
        networkType=LrGeERNetwork,
        variable='delta',
        values=[0.25, 0.5, 0.75],
        defaultConfig=con,
        repeats=2
    )

    results = E.run(export=True)

    print(results)

