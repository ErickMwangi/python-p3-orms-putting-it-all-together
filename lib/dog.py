import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    def __init__(self, name, breed, id=None):
        self.name = name
        self.breed = breed
        self.id = id

    @classmethod
    def create_table(cls):
        CURSOR.execute('''CREATE TABLE IF NOT EXISTS dogs
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          name TEXT,
                          breed TEXT)''')
        CONN.commit()

    @classmethod
    def drop_table(cls):
        CURSOR.execute('''DROP TABLE IF EXISTS dogs''')
        CONN.commit()

    @classmethod
    def create(cls, name, breed):
        dog = cls(name, breed)
        dog.save()
        return dog

    @classmethod
    def new_from_db(cls, row):
        id, name, breed = row[0], row[1], row[2]
        return cls(name, breed, id)

    @classmethod
    def get_all(cls):
        CURSOR.execute('''SELECT * FROM dogs''')
        rows = CURSOR.fetchall()
        dogs = []
        for row in rows:
            dog = cls.new_from_db(row)
            dogs.append(dog)
        return dogs

    @classmethod
    def find_by_name(cls, name):
        CURSOR.execute('''SELECT * FROM dogs WHERE name = ?''', (name,))
        row = CURSOR.fetchone()
        if row:
            return cls.new_from_db(row)
        return None

    @classmethod
    def find_by_id(cls, id):
        CURSOR.execute('''SELECT * FROM dogs WHERE id = ?''', (id,))
        row = CURSOR.fetchone()
        if row:
            return cls.new_from_db(row)
        return None

    @classmethod
    def find_or_create_by(cls, name, breed):
        dog = cls.find_by_name(name)
        if dog:
            return dog
        return cls.create(name, breed)

    def save(self):
        if self.id:
            self.update()
        else:
            CURSOR.execute('''INSERT INTO dogs (name, breed)
                             VALUES (?, ?)''', (self.name, self.breed))
            CONN.commit()
            self.id = CURSOR.lastrowid

    def update(self):
        CURSOR.execute('''UPDATE dogs SET name = ?, breed = ? WHERE id = ?''',
                       (self.name, self.breed, self.id))
        CONN.commit()

