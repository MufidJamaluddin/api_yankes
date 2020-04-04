import peewee as pw

class AppDatabase(object):
    __db = None

    @staticmethod
    def create(config):
        if AppDatabase.__db is None:
            __db = pw.MySQLDatabase(config['NAME_DB'], user=config['USER_DB'], password=config['PASS_DB'], host='127.0.0.1', port=3306)
        return AppDatabase.__db
