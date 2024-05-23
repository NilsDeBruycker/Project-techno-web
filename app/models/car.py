from sqlalchemy.orm import relationship,Mapped,mapped_column
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Table,CheckConstraint,PrimaryKeyConstraint,UniqueConstraint,Boolean
from app.database import Base

# Define association table for many-to-many relationship between Vehicule and Utilisateur
association_table = Table(
    'association', Base.metadata,
    Column('vehicule_id', Integer, ForeignKey('vehicles.id')),
    Column('utilisateur_id', Integer, ForeignKey('utilisateurs.id'))
)

class Sale(Base):
    __tablename__ = 'sales'
    id :Mapped[Integer] =mapped_column(Integer, primary_key=True) # pas sur si int aproprier peut etre metre str
    vehicle_id :Mapped[Integer] = mapped_column(Integer, ForeignKey('vehicles.id'))
    vendor_id :Mapped[Integer] = mapped_column(Integer, ForeignKey('vendors.id'))
    date_of_sale :Mapped[Date] = mapped_column(Date)
    sale_price :Mapped[Float] = mapped_column(Float)
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

class Vehicle(Base):
    __tablename__ = 'vehicles'
    id :Mapped[String] = mapped_column(Integer, primary_key=True)
    model :Mapped[String] = mapped_column(String)
    make :Mapped[String] = mapped_column(String)
    color :Mapped[String] = mapped_column(String)
    max_speed :Mapped[Float] = mapped_column(Float)
    mileage :Mapped[Float] = mapped_column(Float)
    average_consumption :Mapped[Float] = mapped_column(Float)
    sales  :Mapped[Boolean] = mapped_column(Boolean)# = relationship("Sale", back_populates="vehicle")
    price_sell :Mapped[Float] = mapped_column(Float)
    price_rent :Mapped[Float] = mapped_column(Float)
    #ligne de rel avec rent
    rentals :Mapped[Boolean] = mapped_column(Boolean)
    #purchases = relationship("Purchase", back_populates="vehicle")
    #utilisateurs = relationship("Utilisateur", secondary=association_table, back_populates="vehicles")
    owner_email: Mapped[int] = mapped_column(ForeignKey("Utilisateur.adresse"),nullable=True)

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

class Vendeur(Base):
    __tablename__ = 'vendors'
    id = Column(Integer, ForeignKey('utilisateurs.id'), primary_key=True)
    sales = relationship("Sale", back_populates="vendor")
    purchases = relationship("Purchase", back_populates="vendor")
    utilisateur = relationship("Utilisateur", back_populates="vendors")
