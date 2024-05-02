from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from app.database import Base


class Sale(Base):
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True)
    vehicle_id = Column(Integer, ForeignKey('vehicles.id'))
    vendor_id = Column(Integer, ForeignKey('vendors.id'))
    date_of_sale = Column(Date)
    sale_price = Column(Float)
    vehicle = relationship("Vehicle", back_populates="sales")
    vendor = relationship("Vendor", back_populates="sales")

class Rental(Base):
    __tablename__ = 'rentals'
    id = Column(Integer, primary_key=True)
    vehicle_id = Column(Integer, ForeignKey('vehicles.id'))
    client_id = Column(Integer, ForeignKey('clients.id'))
    start_date = Column(Date)
    end_date = Column(Date)
    daily_rate = Column(Float)
    vehicle = relationship("Vehicle", back_populates="rentals")
    client = relationship("Client", back_populates="rentals")

class Purchase(Base):
    __tablename__ = 'purchases'
    id = Column(Integer, primary_key=True)
    vehicle_id = Column(Integer, ForeignKey('vehicles.id'))
    client_id = Column(Integer, ForeignKey('clients.id'))
    vendor_id = Column(Integer, ForeignKey('vendors.id'))
    purchase_date = Column(Date)
    purchase_price = Column(Float)
    vehicle = relationship("Vehicle", back_populates="purchases")
    client = relationship("Client", back_populates="purchases")
    vendor = relationship("Vendor", back_populates="purchases")

# Relationships in other models
class Vehicle(Base):
    __tablename__ = 'vehicles'
    id = Column(Integer, primary_key=True)
    model = Column(String)
    make = Column(String)
    color = Column(String)
    max_speed = Column(Float)
    mileage = Column(Float)
    average_consumption = Column(Float)
    sales = relationship("Sale", back_populates="vehicle")
    rentals = relationship("Rental", back_populates="vehicle")
    purchases = relationship("Purchase", back_populates="vehicle")

class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    rentals = relationship("Rental", back_populates="client")
    purchases = relationship("Purchase", back_populates="client")

class Vendor(Base):
    __tablename__ = 'vendors'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    sales = relationship("Sale", back_populates="vendor")
    purchases = relationship("Purchase", back_populates="vendor")

