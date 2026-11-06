import random
from plate import Plate


def generate_plates(count=10, seed=None):
    rng = random.Random(seed)
    plates = []

    for number in range(1, count + 1):
        plate = Plate(
            number=number,
            scratches=rng.choices(
                [0, 1, 2, 3],
                weights=[55, 25, 15, 5]
            )[0],
            cracks=rng.choices(
                [0, 1, 2, 3],
                weights=[85, 8, 5, 2]
            )[0],
            hole_errors=rng.choices(
                [0, 1, 2, 3],
                weights=[85, 7, 5, 3]
            )[0],
            corrosion=rng.choices(
                [0, 1, 2, 3],
                weights=[75, 14, 8, 3]
            )[0]
        )

        plates.append(plate)

    return plates


if __name__ == "__main__":
    plates = generate_plates(count=10, seed=42)

    for plate in plates:
        plate.describe()
        print("-" * 30)
