import configparser
import logging

from paretos import (
    DesignParameter,
    DesignSpace,
    DesignValues,
    Environment,
    Goals,
    KpiParameter,
    KpiSpace,
    KpiValues,
    OptimizationProblem,
    RunTerminator,
    initialize,
    socrates,
)
from paretos.objects.parameter import ParameterValue

logging.basicConfig(level=logging.INFO)

# THIS IS ONLY AN EXAMPLE HOW TO LOAD THE ENV Variables!
# Feel Free to use the way you are most familiar with!
init_config = configparser.ConfigParser()
init_config.read("env.ini")
initialize(
    init_config["DEVELOP"]["CUSTOMER_TOKEN"].strip('"'),
    "example_db.db"
)

design_1 = DesignParameter("x", minimum=-5, maximum=5)
design_2 = DesignParameter("y", minimum=-5, maximum=5)

design_space = DesignSpace([design_1, design_2])

kpi_1 = KpiParameter("f1", Goals.minimize)
kpi_2 = KpiParameter("f2")

kpi_space = KpiSpace([kpi_1, kpi_2])

optimization_space = OptimizationProblem(design_space, kpi_space)


class TestEnvironment(Environment):
    """
    Class containing the function call to trigger new simulation runs
    """

    def simulate(self, design_values: DesignValues) -> KpiValues:
        x = design_values.get_value("x")
        y = design_values.get_value("y")

        f1 = x ** 2
        f2 = y ** 2 - x

        kpi1 = ParameterValue("f1", f1)
        kpi2 = ParameterValue("f2", f2)

        return KpiValues([kpi1, kpi2])


test_env = TestEnvironment()

run_terminator = RunTerminator(20)

logging.info("Starting optimization!")

res = socrates(
    "test_002_fr", optimization_space, test_env, [run_terminator], n_parallel=1
)

logging.info(
    f"The optimization is finished after {len(res.get_evaluations())} simulations"
)

logging.info(f"There are {len(res.get_pareto_evaluations())} pareto optimal solutions")
