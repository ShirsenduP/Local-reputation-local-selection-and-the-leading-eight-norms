import random

from CodeEvolution import Config
from CodeEvolution import ceModel, GrLeERNetwork


class TestceModel:
    def test_equal(self):
        """This test makes sure that the model builder has the same functionality as the pre-built model. """
        seed = 1
        C = Config(testcase="grle")
        random.seed(seed)
        N = GrLeERNetwork(C)
        df = N.runSimulation()

        random.seed(seed)
        N2 = ceModel.build(config=C)
        df2 = N2.runSimulation()

        assert (df == df2).all()
