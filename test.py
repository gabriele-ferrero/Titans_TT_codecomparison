import os
import subprocess
import pytest

##Test Verification and validation models


def get_python_scripts(directory):
    """Return a list of all Python scripts in the given directory."""
    return [
        os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".py")
    ]


def get_notebook_scripts(directory):
    """Return a list of all Python scripts in the given directory."""
    return [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if f.endswith(".ipynb")
    ]


@pytest.mark.parametrize(
    "script",
    # get_notebook_scripts("Festim_models/Jupyter_notebooks")+
    get_notebook_scripts("MMS")
    # + get_notebook_scripts("graph_scripts_and_results/ITER2D")
    + get_notebook_scripts("graph_scripts_and_results/Purediff")
    + get_notebook_scripts("graph_scripts_and_results/Strong_Trap")
    + get_notebook_scripts("graph_scripts_and_results/TDS")
    + get_notebook_scripts("graph_scripts_and_results/TDS_EUROFER")
    + get_notebook_scripts("graph_scripts_and_results/WeakTrap"),
)
def test_notebook(script):
    """Test a Python script by running it and checking if it exits with a status of 0."""
    result = subprocess.run(
        ["jupyter", "nbconvert", "--to", "script", f"{script}"], capture_output=True
    )
    assert (
        result.returncode == 0
    ), f"Script {script} failed with output:\n{result.stdout.decode()}\n{result.stderr.decode()}"
    result = subprocess.run(["python", f"{script[:-6]}.py"], capture_output=True)
    assert (
        result.returncode == 0
    ), f"Script {script} failed with output:\n{result.stdout.decode()}\n{result.stderr.decode()}"
    os.remove(f"{script[:-6]}.py")
    


# @pytest.mark.parametrize(
#     "script",
#     get_python_scripts("Festim_models") + get_python_scripts("Festim_models/ITER2D"),
# )
# def test_script(script):
#     """Test a Python script by running it and checking if it exits with a status of 0."""
#     result = subprocess.run(["python", f"{script}"], capture_output=True)
#     assert (
#         result.returncode == 0
#     ), f"Script {script} failed with output:\n{result.stdout.decode()}\n{result.stderr.decode()}"
