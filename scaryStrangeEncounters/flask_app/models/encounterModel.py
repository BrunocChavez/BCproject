from flask_app.config.mysqlconnection import connectToMySQL

class Encounter:
    db = 'scaryStrangeEncounters'
    def __init__(self, data):
        self.id = data['id']
        self.category = data['category']
        self.location = data['location']
        self.encounterReport = data['encounterReport']
        self.dateEncounter = data['dateEncounter']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']
        self.user_id = data['user_id']

# Get All 
    @classmethod # if it doesn't work double ss encounters just in this section.
    def getAll(cls):
        query = 'SELECT * FROM encounter;'
        results = connectToMySQL(cls.db).query_db(query)
        encounters = []
        for row in results:
            encounters.append(cls(row))
        return encounters
# Get one
    @classmethod
    def getOne(cls, data):
        query = 'SELECT * FROM encounter WHERE id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
# Save
    @classmethod
    def save(cls, data):
        query = 'INSERT INTO encounter (category, location, encounterReport, dateEncounter, user_id) VALUES (%(category)s, %(location)s, %(encounterReport)s, %(dateEncounter)s, %(user_id)s);'
        return connectToMySQL(cls.db).query_db(query, data)

# Update
    @classmethod
    def update(cls, data):
        query = 'UPDATE encounter SET category=%(category)s, location=%(location)s, encounterReport=%(encounterReport)s, dateEncounter=%(dateEncounter)s WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)

# Delete
    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM encounter WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)

