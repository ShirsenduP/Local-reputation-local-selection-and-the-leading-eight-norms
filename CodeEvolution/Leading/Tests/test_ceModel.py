import random

from ..config import Config
from ..models import ceModel, GrLeERNetwork


class TestCeModel:

    def test_equal(self):
        """This test makes sure that the model builder has the same functionality as the pre-built model. """
        seed = 1
        C = Config(size=10)

        random.seed(seed)
        N = GrLeERNetwork(C)
        df = N.runSimulation()

        random.seed(seed)
        N2 = ceModel.build(config=C, structure="erdos renyi", reputation="global", evolution="local")
        df2 = N2.runSimulation()

        assert (df == df2).all()
