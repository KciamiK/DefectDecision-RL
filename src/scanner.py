import random

from plate import Plate
from plate_generator import generate_plates


class BasicScanner:
    def __init__(self, error_probability=0.25, seed=None):
        if not 0 <= error_probability <= 1:
            raise ValueError(
                "Prawdopodobienstwo bledu musi byc od 0 do 1."
            )

        self.error_probability = error_probability
        self.rng = random.Random(seed)

    def measure(self, actual_value):
        if self.rng.random() >= self.error_probability:
            return actual_value

        possible_values = [
            value
            for value in (actual_value - 1, actual_value + 1)
            if 0 <= value <= 3
        ]

        return self.rng.choice(possible_values)

    def scan(self, plate: Plate):
        return {
            "scratches": self.measure(plate.scratches),
            "cracks": self.measure(plate.cracks),
            "hole_errors": self.measure(plate.hole_errors),
            "corrosion": self.measure(plate.corrosion),
        }


if __name__ == "__main__":
    plates = generate_plates(count=10, seed=42)
    scanner = BasicScanner(
        error_probability=0.25,
        seed=10
    )

    for plate in plates:
        result = scanner.scan(plate)

        print(f"\nPlytka nr {plate.number}")
        print("Cecha           Rzeczywista  Skaner")
        print("-" * 40)

        features = {
            "Rysy": (plate.scratches, result["scratches"]),
            "Pekniecia": (plate.cracks, result["cracks"]),
            "Bledy otworow": (
                plate.hole_errors,
                result["hole_errors"]
            ),
            "Korozja": (plate.corrosion, result["corrosion"]),
        }

        for name, (actual, measured) in features.items():
            print(f"{name:<16}{actual:<13}{measured}")

        print("-" * 40)
