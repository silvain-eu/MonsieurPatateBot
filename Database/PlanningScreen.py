import Database.DatabseManager


class PlanningScreen(Database.DatabseManager.DataBaseObject):
    week: int
    year: int
    file: str
    createdDate: str
    modifiedDate: str

    @staticmethod
    def create():
        pass

    @staticmethod
    def update():
        pass

    @staticmethod
    def delete():
        pass

    @staticmethod
    def findAll():
        pass

    @staticmethod
    def findOne(week: int, year: int):
        dbConn = Database.DatabseManager.connect();
        c = dbConn.cursor()
        c.execute(
            "select week,year,file,created_date, modified_date from planning_screen where week = %s and year = %s limit 1;",
            (week, year,))

        res = c.fetchone()
        if res is None:
            return None
        Database.DatabseManager.disconnect(dbConn)
        return PlanningScreen.serialize(res)

    @staticmethod
    def serialize(data):
        res = PlanningScreen()
        res.week = data[0]
        res.year = data[1]
        res.file = data[2]
        res.createdDate = data[3]
        res.modifiedDate = data[4]

        return res
