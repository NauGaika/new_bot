from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

# engine = create_engine('mssql+pyodbc://Tableau:12345@monitor')
engine = create_engine('mssql+pymssql://Tableau:12345@Vpp-monitordb/monitor')
base = declarative_base()

Session = sessionmaker(bind=engine)

UserPositions = Table(
    'UserPositions',
    base.metadata,
    Column('UserId', Integer, ForeignKey('Users.Id')),
    Column('PositionId', Integer, ForeignKey('Positions.Id'))
)


class Positions(base):
    __tablename__ = "Positions"
    Id = Column(Integer, primary_key=True)
    Name = Column(String)
    Users = relationship("Users", secondary=UserPositions, lazy='joined')


class Departments(base):
    __tablename__ = "Departments"
    Id = Column(Integer, primary_key=True)
    Name = Column(String)
    Users = relationship("Users", backref="department")
    DepartmentId = Column(Integer, ForeignKey('Departments.Id'))
    GenDepartment = relationship("Departments", remote_side="Departments.Id", backref=backref("SubDepartments"), lazy='joined')

    def department_chine(self, chine_arr):
        chine_arr.append(self)
        if self.GenDepartment:
            self.GenDepartment.department_chine(chine_arr)


class Users(base):
    __tablename__ = 'Users'

    Id = Column(Integer, primary_key=True)
    UserName = Column(String)
    Fio = Column(String)
    DepartmentId = Column(Integer, ForeignKey('Departments.Id'))
    Positions = relationship("Positions", secondary=UserPositions, lazy='joined')

    @classmethod
    def get_user_by_username(cls, username):
        username = username.split('@')[0]
        session = Session()
        res = session.query(cls).filter_by(UserName=username)
        if res.count() > 0:
            return res.one()

class CrocoTime():
    
    @classmethod
    def get_prev_day(cls, user_id):
        with engine.connect() as con:
            res = con.execute(
            """
            select 
                PermittedHours,
                ForbiddenHours,
                LateHours,
                SummaryHours
            from CrocDailyStats 
                WHERE Date >= (SELECT CAST(DATEADD(DAY, -1, SYSDATETIME()) AS DATE))
                    AND UserId={}
            """.format(user_id))
            return res.first()

    @classmethod
    def get_prev_week(cls, user_id):
        with engine.connect() as con:
            res = con.execute(
            """
            select 
                sum(PermittedHours) as 'PermittedHours',
                sum(ForbiddenHours) as 'ForbiddenHours',
                sum(LateHours) as 'LateHours',
                sum(SummaryHours) as 'SummaryHours'
            from CrocDailyStats 
                WHERE Date >= (SELECT (DATEADD(DAY, DATEDIFF(DAY,0,CAST(SYSDATETIME () AS DATE) )/7*7,0)))
                    AND UserId={}
    """.format(user_id))
            return res.first() 

    @classmethod
    def get_prev_weakend(cls, user_id):
        with engine.connect() as con:
            res = con.execute(
            """select 
                sum(PermittedHours) as 'PermittedHours',
                sum(ForbiddenHours) as 'ForbiddenHours',
                sum(LateHours) as 'LateHours',
                sum(SummaryHours) as 'SummaryHours'
            from CrocDailyStats 
                WHERE Date >=  (SELECT DATEADD(WEEK, -1, DATEADD(DAY, 5, (DATEADD(DAY, DATEDIFF(DAY,0,CAST(SYSDATETIME () AS DATE) )/7*7,0)))))
                AND Date <=  (SELECT DATEADD(WEEK, -1, DATEADD(DAY, 6, (DATEADD(DAY, DATEDIFF(DAY,0,CAST(SYSDATETIME () AS DATE) )/7*7,0)))))
                AND UserId={}
            """.format(user_id))
            return res.first()