from sqlalchemy import Column, Integer, String, Date
from user_gcp.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    project_id = Column(Integer, index=True)
    company_name = Column(String, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    password = Column(String)
    mobile_number = Column(String, index=True)
    date_of_birth = Column(Date)  