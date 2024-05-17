from exercise import Exercise
from database import Database


class ExerciseHandler:
    database = Database('data/crossfiit.db')
    
    def get_exercise_by_id(id: int):
        exercise = ExerciseHandler.database.select(
            '''
            SELECT * 
            FROM exercises
            JOIN exercises_photos
            ON exercises.id = exercises_photos.id_exercise
            JOIN photos
            ON exercises_photos.id_photo = photos.id
            WHERE exercises.id = (?)
            ''', (id,))
        a = 0
    
    def get_exercise_serie(serie_num):
        serie = ExerciseHandler.database.select(
            '''
            SELECT * 
            FROM exercises
            JOIN exercises_photos
            ON exercises.id = exercises_photos.id_exercise
            JOIN photos
            ON exercises_photos.id_photo = photos.id
            WHERE exercises.serie_number = (?)
            ''', (serie_num,))