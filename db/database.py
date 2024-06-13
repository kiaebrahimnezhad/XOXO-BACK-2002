from sqlalchemy import create_engine , Boolean , Column , ForeignKey , Integer , String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ---------- session and engine

# it's in database.db.txt
URL_DATABASE = "sqlite:///./databse.db"

engine = create_engine(
    URL_DATABASE, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit = False , autoflush = False , bind = engine)

Base = declarative_base()

# ---------- my Users class
class User(Base):
    __tablename__  = 'users'
    id = Column(Integer , primary_key = True , unique = True)
    userName = Column(String , nullable = False , unique = True , default = any)
    victorieCount = Column(Integer , default = 0)

# ----------

Base.metadata.create_all(bind = engine)
