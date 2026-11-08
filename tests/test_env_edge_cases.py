
import sys
from pathlib import Path

import pytest

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from plate import Plate
from quality_env import (
    QualityControlEnv,
    ACCEPT,
    REJECT,
    INSPECT,
)


@pytest.mark.parametrize(
    "configuration",
    [
        {"batch_size": 0},
        {"inspection_budget": -1},
    ],
)
def test_invalid_configuration(configuration):
    with pytest.raises(ValueError):
        QualityControlEnv(**configuration)


def test_zero_inspection_budget():
    env = QualityControlEnv(
        batch_size=3,
        inspection_budget=0,
        seed=42
    )

    state = env.reset()

    assert state[1] == 0
    assert env.valid_actions() == [ACCEPT, REJECT]

    with pytest.raises(ValueError):
        env.step(INSPECT)


def test_inspection_budget_shared_between_plates():
    env = QualityControlEnv(
        batch_size=6,
        inspection_budget=2,
        seed=42
    )

    state = env.reset()
    inspections = 0
    decisions = 0

    while not env.done:
        if INSPECT in env.valid_actions():
            next_state, reward, done, info = env.step(INSPECT)

            inspections += 1

            assert reward == -1
            assert next_state[0] == state[0]
            assert done is False

            state = next_state

        else:
            state, reward, done, info = env.step(ACCEPT)
            decisions += 1

    assert inspections == 2
    assert decisions == 6
    assert env.remaining_budget == 0


def test_invalid_action():
    env = QualityControlEnv(seed=42)
    env.reset()

    with pytest.raises(ValueError):
        env.step(999)


def test_single_plate_episode_and_restart():
    env = QualityControlEnv(
        batch_size=1,
        inspection_budget=0,
        seed=42
    )

    env.reset()

    state, reward, done, info = env.step(ACCEPT)

    assert state is None
    assert done is True
    assert env.done is True

    with pytest.raises(RuntimeError):
        env.step(ACCEPT)

    new_state = env.reset()

    assert new_state[0] == 1
    assert env.done is False


@pytest.mark.parametrize(
    "defective, action, expected_reward, expected_correct",
    [
        (False, ACCEPT, 2, True),
        (True, ACCEPT, -12, False),
        (True, REJECT, 5, True),
        (False, REJECT, -4, False),
    ],
)
def test_all_final_decision_rewards(
    defective,
    action,
    expected_reward,
    expected_correct,
):
    env = QualityControlEnv(
        batch_size=1,
        seed=42
    )

    env.reset()

    # Ustawiamy znana jakosc do testowania samej nagrody.
    env.plates[0] = Plate(
        number=1,
        scratches=2 if defective else 0
    )

    state, reward, done, info = env.step(action)

    assert reward == expected_reward
    assert info["correct"] == expected_correct
    assert done is True
    assert state is None
