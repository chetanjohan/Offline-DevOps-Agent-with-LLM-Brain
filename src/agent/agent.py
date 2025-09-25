"""agent.py

Small agent module exposing `run_agent_task`.

This is intentionally simple: it simulates running a task and returns a
boolean success flag so callers can act on the result.
"""

from typing import Optional, Dict, Any


def run_agent_task(task_name: str, context: Optional[Dict[str, Any]] = None) -> bool:
    """Simulate running an agent task.

    Args:
        task_name: Name of the task to run.
        context: Optional context/config for the task.

    Returns:
        True on simulated success, False on simulated failure.
    """
    # Very small simulation: treat tasks whose name contains 'fail' as failures
    print(f"[Agent] Starting task: {task_name}")
    if context:
        print(f"[Agent] Context: {context}")

    if "fail" in task_name.lower():
        print(f"[Agent] Task {task_name} failed (simulated)")
        return False

    print(f"[Agent] Task {task_name} completed successfully (simulated)")
    return True


if __name__ == "__main__":
    run_agent_task("example_task")


