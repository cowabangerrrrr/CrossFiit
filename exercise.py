from dataclasses import dataclass


@dataclass
class Exercise:
    id: str
    name: str
    description: str
    muscle_group: int
    main_photo: str
    second_photo: str
