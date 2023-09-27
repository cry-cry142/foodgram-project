from dataclasses import dataclass


@dataclass
class Ingredient:
    key: int
    name: str
    count: int
    unit: str

    def __str__(self):
        return f'{self.name} - {self.count} {self.unit}'
