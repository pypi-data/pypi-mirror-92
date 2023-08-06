import configparser
from pathlib import Path

from dotenv import load_dotenv

from paretos import (
    DesignParameter,
    DesignSpace,
    Goals,
    KpiParameter,
    KpiSpace,
    OptimizationProblem,
)
from paretos.client import SocratesAPIClient
from paretos.objects.evaluation import Evaluations

init_config = configparser.ConfigParser()
init_config.read("env.ini")

env_path = Path("") / "env.ini"
load_dotenv(dotenv_path=env_path)

client = SocratesAPIClient(
    "https://api.paretos.io/socrates/",
    init_config["DEVELOP"]["CUSTOMER_TOKEN"].strip('"'),
)
design_1 = DesignParameter("x", minimum=-5, maximum=5)
design_2 = DesignParameter("y", minimum=-5, maximum=5)

design_space = DesignSpace([design_1, design_2])

kpi_1 = KpiParameter("f1", Goals.minimize)
kpi_2 = KpiParameter("f2")

kpi_space = KpiSpace([kpi_1, kpi_2])

optimization_space = OptimizationProblem(design_space, kpi_space)
resp = client.predict_design(
    optimization_space,
    Evaluations(),
    1000,
)
designs = client.predict_design(
    optimization_space,
    Evaluations(),
    10000,
)

print(len(designs.get_designs()))
