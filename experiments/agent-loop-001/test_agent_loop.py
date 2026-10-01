from agent_loop import AgentLoop


def test_successful_verification() -> None:
    loop = AgentLoop(
        observe=lambda: "task",
        plan=lambda _: "plan",
        act=lambda _: "answer",
        verify=lambda value: value == "answer",
    )
    result = loop.run()
    assert result.verified is True
    assert result.attempts == 1


def test_failed_verification_retries() -> None:
    attempts = {"n": 0}

    def act(_: str) -> str:
        attempts["n"] += 1
        return "answer" if attempts["n"] == 2 else "wrong"

    loop = AgentLoop(
        observe=lambda: "task",
        plan=lambda _: "plan",
        act=act,
        verify=lambda value: value == "answer",
    )
    result = loop.run()
    assert result.verified is True
    assert result.attempts == 2
