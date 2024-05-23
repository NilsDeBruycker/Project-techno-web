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
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    vehicle_id : Mapped[int] = mapped_column(Integer, ForeignKey('vehicles.id'))
    vendor_id : Mapped[int] = mapped_column(Integer, ForeignKey('vendors.id'))
    date_of_sale : Mapped[Date] = mapped_column(Date)
    sale_price : Mapped[Float] = mapped_column(Float)
    vehicle : Mapped[Boolean] = mapped_column(Boolean)
    vendor : Mapped[Boolean] = mapped_column(Boolean)
    UniqueConstraint("vehicle_id", "vendor_id", name="one_sale")

class Rental(Base):
    __tablename__ = 'rentals'
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    vehicle_id : Mapped[int] = mapped_column(Integer, ForeignKey('vehicles.id'))
    client_id : Mapped[int] = mapped_column(Integer, ForeignKey('clients.id'))
    start_date : Mapped[Date] = mapped_column(Date)
    end_date : Mapped[Date] = mapped_column(Date)
    daily_rate : Mapped[Float] = mapped_column(Float)
    vehicle : Mapped[Boolean] = mapped_column(Boolean)
    client : Mapped[Boolean] = mapped_column(Boolean)

class Purchase(Base):
    __tablename__ = 'purchases'
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    vehicle_id : Mapped[int] = mapped_column(Integer, ForeignKey('vehicles.id'))
    client_id : Mapped[int] = mapped_column(Integer, ForeignKey('clients.id'))
    vendor_id : Mapped[int] = mapped_column(Integer, ForeignKey('vendors.id'))
    purchase_date : Mapped[Date] = mapped_column(Date)
    purchase_price : Mapped[Float] = mapped_column(Float)
    vehicle : Mapped[Boolean] = mapped_column(Boolean)
    client : Mapped[Boolean] = mapped_column(Boolean)
    vendor : Mapped[Boolean] = mapped_column(Boolean)

class Utilisateur(Base):
    __tablename__ = 'utilisateurs'
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    nom : Mapped[String] = mapped_column(String)
    prenom : Mapped[String] = mapped_column(String)
    adresse : Mapped[String] = mapped_column(String)
    num_tel : Mapped[String] = mapped_column(String)
    vehicles : Mapped[Boolean] = mapped_column(Boolean)
    vendors : Mapped[Boolean] = mapped_column(Boolean)
    clients : Mapped[Boolean] = mapped_column(Boolean)


class Client(Base):
    __tablename__ = 'clients'
    id : Mapped[int] = mapped_column(Integer, ForeignKey('utilisateurs.id'), primary_key=True)
    rentals : Mapped[Boolean] = mapped_column(Boolean)
    purchases : Mapped[Boolean] = mapped_column(Boolean)
    utilisateur : Mapped[Boolean] = mapped_column(Boolean)

class Vendor(Base):
    __tablename__ = 'vendors'
    id : Mapped[int] = mapped_column(Integer, ForeignKey('utilisateurs.id'), primary_key=True)
    sales : Mapped[Boolean] = mapped_column(Boolean)
    purchases : Mapped[Boolean] = mapped_column(Boolean)
    utilisateur : Mapped[Boolean] = mapped_column(Boolean)

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

