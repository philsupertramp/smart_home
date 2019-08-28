from networking.database import DB

if __name__ == '__main__':
    database = DB()
    # obj_creation = database.execute('INSERT INTO test (num, data) VALUES (100, \'abcdef\')')
    # obj_creation = database.execute('INSERT INTO test (num, data) VALUES (200, \'abcdef\')')
    # obj_creation = database.execute('INSERT INTO test (num, data) VALUES (300, \'abcdef2\')')
    selection = database.select('test', columns=['id', 'num', 'data'], where=['data LIKE \'%abcdef%\''])

    print(selection)
