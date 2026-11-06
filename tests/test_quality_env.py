import sys
from pathlib import Path

import pytest

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from quality_env import (
    QualityControlEnv,
    ACCEPT,
    REJECT,
    INSPECT,
)


def test_reset():
    env = QualityControlEnv(seed=42)
    state = env.reset()

    assert state[0] == 10
    assert state[1] == 4
    assert state[2] in ("L", "M", "H")
    assert state[3] is None
    assert env.done is False


def test_valid_actions():
    env = QualityControlEnv(seed=42)
    env.reset()

    assert env.valid_actions() == [
        ACCEPT, REJECT, INSPECT
    ]


def test_inspection():
    env = QualityControlEnv(seed=42)
    env.reset()

    state, reward, done, info = env.step(INSPECT)

    assert state[0] == 10
    assert state[1] == 3
    assert state[3] in ("+", "-")
    assert reward == -1
    assert done is False
    assert info["action"] == "INSPECT"


def test_double_inspection():
    env = QualityControlEnv(seed=42)
    env.reset()
    env.step(INSPECT)

    with pytest.raises(ValueError):
        env.step(INSPECT)


def test_inspection_budget():
    env = QualityControlEnv(
        batch_size=3,
        inspection_budget=1,
        seed=42
    )

    env.reset()
    env.step(INSPECT)
    state, _, _, _ = env.step(ACCEPT)

    assert state[1] == 0
    assert INSPECT not in env.valid_actions()


def test_full_episode():
    env = QualityControlEnv(seed=42)
    state = env.reset()

    decisions = 0
    total_reward = 0

    while state is not None:
        state, reward, done, info = env.step(ACCEPT)

        decisions += 1
        total_reward += reward

        assert reward in (2, -12)

    assert decisions == 10
    assert done is True
    assert env.done is True
    assert env.valid_actions() == []
    assert isinstance(total_reward, int)


def test_action_after_episode():
    env = QualityControlEnv(
        batch_size=1,
        seed=42
    )

    env.reset()
    env.step(ACCEPT)

    with pytest.raises(RuntimeError):
        env.step(REJECT)


def test_reproducibility():
    env1 = QualityControlEnv(seed=42)
    env2 = QualityControlEnv(seed=42)

    assert env1.reset() == env2.reset()

    for _ in range(10):
        result1 = env1.step(ACCEPT)
        result2 = env2.step(ACCEPT)

        assert result1 == result2
