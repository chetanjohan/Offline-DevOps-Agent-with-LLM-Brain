"""agent.py

Small agent module that exposes a run_agent_task function.
"""

def run_agent_task(task_name: str) -> None:
    """Run a specified agent task.

    Args:
        task_name: Name of the task to run.
    """
    print(f"Running task: {task_name}")


if __name__ == "__main__":
    run_agent_task("example_task")