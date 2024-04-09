import os
import subprocess
import pytest

def get_python_scripts(directory):
    """Return a list of all Python scripts in the given directory."""
    return [f for f in os.listdir(directory) if f.endswith('.py')]

@pytest.mark.parametrize('script', get_python_scripts('Festim models'))
def test_script(script):
    """Test a Python script by running it and checking if it exits with a status of 0."""
    result = subprocess.run(['python', f'Festim models/{script}'], capture_output=True)
    assert result.returncode == 0, f"Script {script} failed with output:\n{result.stdout.decode()}\n{result.stderr.decode()}"