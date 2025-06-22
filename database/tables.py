
from sqlalchemy import Column, Integer, String,Date, ForeignKey
from sqlalchemy.orm import DeclarativeBase,relationship


class Base(DeclarativeBase):
    pass


class Platform(Base):
    """
    Defines the platform table
    """
    __tablename__ = 'platform'

    p_id = Column(Integer, primary_key=True,autoincrement=False)
    p_name = Column(String(50), nullable=False)

    hackathons = relationship("Hackathon", back_populates="platform")

class Hackathon(Base):
    """
    Defines the hackathon table
    """
    __tablename__ = 'hackathon'

    Hackathon_id = Column(String(36), primary_key=True,autoincrement=False)
    Hackathon_name = Column(String(200), nullable=True)
    Hackathon_url = Column(String(200), nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    reg_start_date = Column(Date, nullable=True)
    reg_end_date = Column(Date, nullable=True)
    mode = Column(String(50), nullable=False)

    platform_id = Column(Integer, ForeignKey('platform.p_id'), nullable=False)

    platform = relationship("Platform", back_populates="hackathons")
    bookmarks = relationship("Bookmarks", back_populates="hackathon")


class Users(Base):
    """
    Defines the users table
    """
    __tablename__ = 'users'

    sub = Column(String(100), primary_key=True, autoincrement=False)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    picture = Column(String(200), nullable=True)


    bookmarks = relationship("Bookmarks", back_populates="user")


class Bookmarks(Base):
    """
    Defines the bookmarks table
    """
    __tablename__ = 'bookmarks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_sub = Column(String(100), ForeignKey('users.sub'), nullable=False)
    hackathon_id = Column(String(36), ForeignKey('hackathon.Hackathon_id'), nullable=False)

    user = relationship("Users", back_populates="bookmarks")
    hackathon = relationship("Hackathon", back_populates="bookmarks")