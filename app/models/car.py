from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from app.database import Base

# Define association table for many-to-many relationship between Vehicule and Utilisateur
association_table = Table(
    'association', Base.metadata,
    Column('vehicule_id', Integer, ForeignKey('vehicule.id')),
    Column('utilisateur_id', Integer, ForeignKey('utilisateur.id'))
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
    vendeur = relationship("Vendor", back_populates="purchases")

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
    utilisateurs = relationship("Utilisateur", secondary=association_table, back_populates="vehicules")

class Utilisateur(Base):
    __tablename__ = 'utilisateurs'
    id = Column(Integer, primary_key=True)
    nom = Column(String)
    prenom = Column(String)
    adresse = Column(String)
    num_tel = Column(String)
    vehicules = relationship("Vehicle", secondary=association_table, back_populates="utilisateurs")
    vendeurs = relationship("Vendor", back_populates="utilisateur")
    clients = relationship("Client", back_populates="utilisateur")

class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, ForeignKey('utilisateurs.id'), primary_key=True)
    rentals = relationship("Rental", back_populates="client")
    purchases = relationship("Purchase", back_populates="client")
    Utilisateur =relationship("Utilisateur",back_populates="clients ")
class Vendeur(Base):
    __tablename__ = 'vendors'
    id = Column(Integer, ForeignKey('utilisateurs.id'), primary_key=True)
    sales = relationship("Sale", back_populates="vendor")
    purchases = relationship("Purchase", back_populates="vendor")
    utilisateur = relationship("Utilisateur", back_populates="vendeurs")
