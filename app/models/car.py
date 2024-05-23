from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Table, CheckConstraint, PrimaryKeyConstraint, UniqueConstraint, Boolean
from app.database import Base

# Define association table for many-to-many relationship between Vehicle and Utilisateur
association_table = Table(
    'association', Base.metadata,
    Column('vehicle_id', Integer, ForeignKey('vehicles.id')),
    Column('utilisateur_id', Integer, ForeignKey('utilisateurs.id'))
)

class Sale(Base):
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True)
    vehicle_id = Column(Integer, ForeignKey('vehicles.id'))
    vendor_id = Column(Integer, ForeignKey('vendors.id'))
    date_of_sale = Column(Date)
    sale_price = Column(Float)
    vehicle = relationship("Vehicle", back_populates="sales")
    vendor = relationship("Vendor", back_populates="sales")
    UniqueConstraint("vehicle_id", "vendor_id", name="one_sale")

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


class Utilisateur(Base):
    __tablename__ = 'utilisateurs'
    id = Column(Integer, primary_key=True)
    nom = Column(String)
    prenom = Column(String)
    adresse = Column(String)
    num_tel = Column(String)
    vehicles = relationship("Vehicle", secondary=association_table, back_populates="utilisateurs")
    vendors = relationship("Vendor", back_populates="utilisateur")
    clients = relationship("Client", back_populates="utilisateur")

class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, ForeignKey('utilisateurs.id'), primary_key=True)
    rentals = relationship("Rental", back_populates="client")
    purchases = relationship("Purchase", back_populates="client")
    utilisateur = relationship("Utilisateur", back_populates="clients")

class Vendor(Base):  
    __tablename__ = 'vendors'
    id = Column(Integer, ForeignKey('utilisateurs.id'), primary_key=True)
    sales = relationship("Sale", back_populates="vendor")
    purchases = relationship("Purchase", back_populates="vendor")
    utilisateur = relationship("Utilisateur", back_populates="vendors")

class Vehicle(Base):
    __tablename__ = 'vehicles'
    id = Column(Integer, primary_key=True)
    model = Column(String)
    make = Column(String)
    color = Column(String)
    max_speed = Column(Float)
    mileage = Column(Float)
    average_consumption = Column(Float)
    sales = Column(Boolean)
    price_sell = Column(Float)
    price_rent = Column(Float)
    rentals = Column(Boolean)
    owner_email = Column(Integer, ForeignKey("utilisateurs.id"), nullable=True)
