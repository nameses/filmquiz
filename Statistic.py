from database import db, mycursor


class Statistic:
    def __init__(self, id: int, *args, **kwargs):
        self.id = id
        self.inserting_person()

    @classmethod
    def all_people(cls):
        mycursor.execute('SELECT * FROM Person')
        result = [item[0] for item in mycursor.fetchall()]
        return result

    def inserting_person(self):
        ids = self.all_people()
        if self.id not in ids:
            mycursor.execute(f'INSERT INTO Person(PersonID) VALUES ({self.id})')
            db.commit()

    def photo_quiz_points(self):
        mycursor.execute(f'SELECT PointsPhotoQuiz FROM Person WHERE PersonID={self.id}')
        result = [item[0] for item in mycursor.fetchall() or 0]
        # result = mycursor.fetchall()[0] or 0
        result = sum(point for point in result)
        return result

    def description_quiz_points(self):
        mycursor.execute(f'SELECT PointsDescriptionQuiz FROM Person WHERE PersonID={self.id}')
        result = [item[0] for item in mycursor.fetchall() or 0]
        # result = mycursor.fetchall()[0] or 0
        result = sum(point for point in result)
        return result

    def updating_photo_points(self, win: bool):
        existing_points = self.photo_quiz_points()
        points = existing_points+2 if win else existing_points-3
        if existing_points < 3 and not win:
            points = 0
        update_person = f'UPDATE Person SET PointsPhotoQuiz={points} ' \
                        f'WHERE PersonID="{self.id}"'
        mycursor.execute(update_person)
        db.commit()

    def updating_description_points(self, win: bool):
        existing_points = self.description_quiz_points()
        points = existing_points+2 if win else existing_points-3
        if existing_points < 3 and not win:
            points = 0
        update_person = f'UPDATE Person SET PointsDescriptionQuiz={points} ' \
                        f'WHERE PersonID="{self.id}"'
        mycursor.execute(update_person)
        db.commit()

    def updating_dq_options(self, ids):
        # update_person = f'UPDATE Person SET PointsPhotoQuiz={ids} ' \
        #                 f'WHERE PersonID="{self.id}"'
        for i, id in enumerate(ids):
            update_person = f'UPDATE Person SET dq{i+1}={id} ' \
                            f'WHERE PersonID="{self.id}"'
            mycursor.execute(update_person)
            db.commit()

    def updating_pq_options(self, ids):
        # update_person = f'UPDATE Person SET PointsPhotoQuiz={ids} ' \
        #                 f'WHERE PersonID="{self.id}"'
        for i, id in enumerate(ids):
            update_person = f'UPDATE Person SET pq{i+1}={id} ' \
                            f'WHERE PersonID="{self.id}"'
            mycursor.execute(update_person)
            db.commit()

    def get_pq_ids(self):
        ids = []
        for i in range(1, 5):
            mycursor.execute(f'SELECT pq{i} FROM Person WHERE PersonID={self.id}')
            ids.append([item[0] for item in mycursor.fetchall() or None])
        return ids

    def get_dq_ids(self):
        ids = []
        for i in range(1, 5):
            mycursor.execute(f'SELECT dq{i} FROM Person WHERE PersonID={self.id}')
            ids.append([item[0] for item in mycursor.fetchall() or None])
        return ids
