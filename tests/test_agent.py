from src.agent.agent import run_agent_task


def test_agent_success():
    assert run_agent_task("do_something") is True


def test_agent_failure():
    assert run_agent_task("this_should_fail") is False


if __name__ == "__main__":
    test_agent_success()
    test_agent_failure()
