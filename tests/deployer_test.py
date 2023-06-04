import sys
import pytest
from pathlib import Path
import pprint


sys.path.append(str(Path(__file__).parents[1]))
# sys.path.append(str(Path(__file__).parents[0]))

from airdot.deployer import build_deployment, deploy
from tests.test_files.example_1 import func_4


@pytest.mark.parametrize(
    "input, input_func, function, expected", [(4, func_4, build_deployment, dict)]
)
def test_build_deployment(input, input_func, function, expected):
    type(function(input_func)) == expected


print(deploy(func_4))
