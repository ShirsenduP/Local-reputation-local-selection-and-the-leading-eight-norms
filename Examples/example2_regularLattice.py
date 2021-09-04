import CodeEvolution as ce

config = ce.Config(
    structure="reg lattice",  # Options: ["erdos renyi", "reg lattice", "small world", "watts strogatz"] (see models.py)
    reputation="global",  # Options: ["global", "local"]
    evolution="local",  # Options: ["global", "local"]
    size=300,
    initialState=ce.State(mainID=0, proportion=1, mutantID=8),
    socialDilemma=ce.config.Dilemma(type="PD", benefit=2, cost=1),
    omegas=0.99,
    maxPeriods=2000,
    alpha=0.1,
    delta=1,
    mutationProbability=0.1,
    degree=4,
)
model = ce.ceModel.build(config)
df = model.runSimulation()
print(df)