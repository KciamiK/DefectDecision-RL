from dataclasses import dataclass


@dataclass
class Plate:
    number: int
    scratches: int = 0
    cracks: int = 0
    hole_errors: int = 0
    corrosion: int = 0

    def is_defective(self) -> bool:
        return (
            self.scratches >= 2
            or self.cracks >= 1
            or self.hole_errors >= 1
            or self.corrosion >= 2
        )

    def describe(self):
        print(f"Plytka nr {self.number}")
        print(f"Rysy: {self.scratches}")
        print(f"Pekniecia: {self.cracks}")
        print(f"Bledy otworow: {self.hole_errors}")
        print(f"Korozja: {self.corrosion}")

        if self.is_defective():
            print("Status: WADLIWA")
        else:
            print("Status: POPRAWNA")


if __name__ == "__main__":
    plate = Plate(
        number=1,
        scratches=2,
        cracks=0,
        hole_errors=0,
        corrosion=1
    )

    plate.describe()
