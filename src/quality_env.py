import random

from detailed_scanner import DetailedScanner
from plate_generator import generate_plates
from scanner import BasicScanner


ACCEPT = 0
REJECT = 1
INSPECT = 2


class QualityControlEnv:
    def __init__(self, batch_size=10, inspection_budget=4, seed=None):
        if batch_size < 1 or inspection_budget < 0:
            raise ValueError("Niepoprawny rozmiar partii lub budzet.")

        self.batch_size = batch_size
        self.inspection_budget = inspection_budget
        self.rng = random.Random(seed)

        self.plates = []
        self.index = 0
        self.remaining_budget = 0
        self.basic_scan = None
        self.detailed_scan = None
        self.done = True

    @staticmethod
    def risk_category(scan):
        points = {
            "scratches": (0, 40, 80, 100),
            "cracks": (0, 85, 95, 100),
            "hole_errors": (0, 85, 95, 100),
            "corrosion": (0, 35, 80, 100),
        }

        score = max(
            points[name][value]
            for name, value in scan.items()
        )

        if score < 30:
            return "L"
        if score < 70:
            return "M"
        return "H"

    @staticmethod
    def scan_indicates_defect(scan):
        return (
            scan["scratches"] >= 2
            or scan["cracks"] >= 1
            or scan["hole_errors"] >= 1
            or scan["corrosion"] >= 2
        )

    def _observation(self):
        if self.done:
            return None

        detailed_result = None

        if self.detailed_scan is not None:
            detailed_result = (
                "+"
                if self.scan_indicates_defect(self.detailed_scan)
                else "-"
            )

        return (
            self.batch_size - self.index,
            self.remaining_budget,
            self.risk_category(self.basic_scan),
            detailed_result,
        )

    def reset(self):
        self.plates = generate_plates(
            count=self.batch_size,
            seed=self.rng.randrange(2**32),
        )

        self.basic_scanner = BasicScanner(
            seed=self.rng.randrange(2**32)
        )

        self.detailed_scanner = DetailedScanner(
            seed=self.rng.randrange(2**32)
        )

        self.index = 0
        self.remaining_budget = self.inspection_budget
        self.detailed_scan = None
        self.done = False

        self.basic_scan = self.basic_scanner.scan(
            self.plates[self.index]
        )

        return self._observation()

    def valid_actions(self):
        if self.done:
            return []

        actions = [ACCEPT, REJECT]

        if self.remaining_budget > 0 and self.detailed_scan is None:
            actions.append(INSPECT)

        return actions

    def step(self, action):
        if self.done:
            raise RuntimeError(
                "Epizod juz sie zakonczyl. Wywolaj reset()."
            )

        if action not in self.valid_actions():
            raise ValueError(
                "Niedozwolona akcja w aktualnym stanie."
            )

        if action == INSPECT:
            self.remaining_budget -= 1

            self.detailed_scan = self.detailed_scanner.scan(
                self.plates[self.index]
            )

            return self._observation(), -1, False, {
                "action": "INSPECT"
            }

        defective = self.plates[self.index].is_defective()

        if action == ACCEPT:
            reward = -12 if defective else 2
        else:
            reward = 5 if defective else -4

        info = {
            "action": "ACCEPT" if action == ACCEPT else "REJECT",
            "plate_number": self.index + 1,
            "correct": (action == REJECT) == defective,
        }

        self.index += 1

        if self.index >= self.batch_size:
            self.done = True
            self.basic_scan = None
            self.detailed_scan = None

            return None, reward, True, info

        self.detailed_scan = None
        self.basic_scan = self.basic_scanner.scan(
            self.plates[self.index]
        )

        return self._observation(), reward, False, info


if __name__ == "__main__":
    env = QualityControlEnv(seed=42)

    state = env.reset()
    total_reward = 0

    while state is not None:
        if state[0] >= 7 and state[1] > 0 and state[3] is None:
            action = INSPECT

        elif state[3] == "+" or (
            state[3] is None and state[2] == "H"
        ):
            action = REJECT

        else:
            action = ACCEPT

        next_state, reward, done, info = env.step(action)
        total_reward += reward

        print(
            f"Stan: {state} | "
            f"Akcja: {info['action']} | "
            f"Nagroda: {reward:+d}"
        )

        if "correct" in info:
            print(f"  Decyzja poprawna: {info['correct']}")

        state = next_state

    print(f"\nKoniec partii. Suma nagrod: {total_reward}")
    print(f"Pozostaly budzet: {env.remaining_budget}")
