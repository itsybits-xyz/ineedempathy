from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=False)
    is_superuser = Column(Boolean(), default=False)
    trips = relationship("Trip", back_populates="user")


# trip_trails = Table(
#     "trip_trails",
#     Base.metadata,
#     Column("trip_id", Integer, ForeignKey("trips.id")),
#     Column("trail_id", Integer, ForeignKey("trails.id")),
# )


class Trail(Base):
    __tablename__ = "trails"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    length = Column(Float)

    # trips = relationship("Trip", secondary=trip_trails, back_populates="trails")


class Trip(Base):
    __tablename__ = "trips"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, index=True, nullable=False)
    distance = Column(Float, index=True)
    average_speed = Column(Float, index=True)
    max_speed = Column(Float, index=True)
    duration_s = Column(Integer, index=True)
    date = Column(DateTime, index=True)
    comments = Column(Text, index=False)

    # trails = relationship("Trail", secondary=trip_trails, back_populates="trips")
    user = relationship("User", back_populates="trips")
