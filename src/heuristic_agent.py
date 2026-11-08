
from quality_env import (
    QualityControlEnv,
    ACCEPT,
    REJECT,
    INSPECT,
)


class HeuristicAgent:
    def choose_action(self, state, valid_actions):
        remaining_plates, remaining_budget, risk, detailed_result = state

        if detailed_result == "+":
            return REJECT

        if detailed_result == "-":
            return ACCEPT

        if risk == "L":
            return ACCEPT

        if risk == "M":
            if INSPECT in valid_actions:
                return INSPECT

            return ACCEPT

        if risk == "H":
            return REJECT

        raise ValueError("Nieznana kategoria ryzyka.")


if __name__ == "__main__":
    env = QualityControlEnv(
        batch_size=10,
        inspection_budget=4,
        seed=42
    )

    agent = HeuristicAgent()

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
    missed_defects = 0
    false_rejections = 0

    print("SYMULACJA AGENTA HEURYSTYCZNEGO")
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

            elif action == ACCEPT:
                missed_defects += 1

            elif action == REJECT:
                false_rejections += 1

        print(
            f"Stan: {state} | "
            f"Akcja: {action_names[action]} | "
            f"Nagroda: {reward:+d}"
        )

        if "correct" in info:
            print(
                f"  Decyzja poprawna: {info['correct']}"
            )

        state = next_state

    accuracy = 100 * correct_decisions / final_decisions

    print("\n" + "=" * 55)
    print("PODSUMOWANIE")
    print(f"Liczba ocenionych plytek: {final_decisions}")
    print(f"Poprawne decyzje: {correct_decisions}")
    print(f"Przeoczone wady: {missed_defects}")
    print(f"Bledne odrzucenia: {false_rejections}")
    print(f"Dodatkowe kontrole: {inspections}")
    print(f"Pozostaly budzet: {env.remaining_budget}")
    print(f"Suma nagrod: {total_reward}")
    print(f"Skutecznosc decyzji: {accuracy:.1f}%")
