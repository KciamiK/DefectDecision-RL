
import random

from quality_env import (
    QualityControlEnv,
    ACCEPT,
    REJECT,
    INSPECT,
)


class RandomAgent:
    def __init__(self, seed=None):
        self.rng = random.Random(seed)

    def choose_action(self, state, valid_actions):
        if not valid_actions:
            raise ValueError("Brak dostepnych akcji.")

        return self.rng.choice(valid_actions)


if __name__ == "__main__":
    env = QualityControlEnv(
        batch_size=10,
        inspection_budget=4,
        seed=42
    )

    agent = RandomAgent(seed=123)

    action_names = {
        ACCEPT: "ACCEPT",
        REJECT: "REJECT",
        INSPECT: "INSPECT",
    }

    state = env.reset()

    total_reward = 0
    correct_decisions = 0
    final_decisions = 0
    inspections = 0

    print("SYMULACJA AGENTA LOSOWEGO")
    print("=" * 55)

    while not env.done:
        valid_actions = env.valid_actions()

        action = agent.choose_action(
            state,
            valid_actions
        )

        next_state, reward, done, info = env.step(action)

        total_reward += reward

        if action == INSPECT:
            inspections += 1
        else:
            final_decisions += 1

            if info["correct"]:
                correct_decisions += 1

        print(
            f"Stan: {state} | "
            f"Akcja: {action_names[action]} | "
            f"Nagroda: {reward:+d}"
        )

        state = next_state

    print("\n" + "=" * 55)
    print("PODSUMOWANIE")
    print(f"Liczba ocenionych plytek: {final_decisions}")
    print(f"Poprawne decyzje: {correct_decisions}")
    print(f"Dodatkowe kontrole: {inspections}")
    print(f"Pozostaly budzet: {env.remaining_budget}")
    print(f"Suma nagrod: {total_reward}")

    accuracy = 100 * correct_decisions / final_decisions

    print(f"Skutecznosc decyzji: {accuracy:.1f}%")
