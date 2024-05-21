from dataclasses import dataclass


@dataclass
class Exercise:
    id: str
    name: str
    description: str
    muscle_group: int
    main_photo_path: str
    second_photo_path: str

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'muscle_group': self.muscle_group,
            'main_photo_path': self.main_photo_path,
            'second_photo_path': self.second_photo_path,
        }
