from scanner import BasicScanner
from plate_generator import generate_plates


class DetailedScanner(BasicScanner):
    def __init__(self, seed=None):
        super().__init__(
            error_probability=0.05,
            seed=seed
        )


if __name__ == "__main__":
    plates = generate_plates(count=10, seed=42)

    basic_scanner = BasicScanner(
        error_probability=0.25,
        seed=10
    )

    detailed_scanner = DetailedScanner(seed=20)

    features = [
        "scratches",
        "cracks",
        "hole_errors",
        "corrosion"
    ]

    basic_errors = 0
    detailed_errors = 0

    print("POROWNANIE SKANEROW")
    print("Kolejnosc: rysy, pekniecia, otwory, korozja")
    print("=" * 55)

    for plate in plates:
        basic_result = basic_scanner.scan(plate)
        detailed_result = detailed_scanner.scan(plate)

        actual = tuple(
            getattr(plate, feature)
            for feature in features
        )

        basic = tuple(
            basic_result[feature]
            for feature in features
        )

        detailed = tuple(
            detailed_result[feature]
            for feature in features
        )

        basic_errors += sum(
            a != b for a, b in zip(actual, basic)
        )

        detailed_errors += sum(
            a != b for a, b in zip(actual, detailed)
        )

        print(f"\nPlytka nr {plate.number}")
        print(f"Rzeczywiste: {actual}")
        print(f"Podstawowy:  {basic}")
        print(f"Dokladny:   {detailed}")

    total = len(plates) * len(features)

    print("\n" + "=" * 55)
    print("PODSUMOWANIE")
    print(f"Liczba wszystkich pomiarow: {total}")
    print(f"Bledy skanera podstawowego: {basic_errors}")
    print(f"Bledy skanera dokladnego:   {detailed_errors}")
    print(f"Skutecznosc podstawowego: {(1 - basic_errors / total) * 100:.1f}%")
    print(f"Skutecznosc dokladnego:   {(1 - detailed_errors / total) * 100:.1f}%")
