import CodeEvolution as ce

config = ce.Config(
    structure="erdos renyi",  # Options: ["erdos renyi", "reg lattice", "small world", "watts strogatz"] (see models.py)
    reputation="global",  # Options: ["global", "local"]
    evolution="global",  # Options: ["global", "local"]
    size=300,
    initialState=ce.State(mainID=0, proportion=1, mutantID=8),
    socialDilemma=ce.config.Dilemma(type="PD", benefit=2, cost=1),
    omegas=0.99,
    maxPeriods=2000,
    alpha=0.1,
    delta=1,
    mutationProbability=0.1,
    sparseDensity=True,
)
model = ce.ceModel.build(config)
df = model.runSimulation()
print(df)