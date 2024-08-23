import subprocess


def run_sh(
    command: list,
    inputs: str = None,
):
    result = subprocess.run(
        command,
        input=inputs,
        text=True,
        capture_output=True,
        shell=True,
    )
    event = result.stderr
    return event
