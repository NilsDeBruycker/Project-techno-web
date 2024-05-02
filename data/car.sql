
CREATE TABLE Utilisateurs (
    Id_Utilisateur INTEGER PRIMARY KEY AUTOINCREMENT,
    Nom TEXT NOT NULL,
    Prenom TEXT NOT NULL,
    Adresse TEXT NOT NULL,
    Num_Tel TEXT NOT NULL
);

CREATE TABLE Vehicule (
    Id_Vehicule INTEGER PRIMARY KEY AUTOINCREMENT,
    Marque_ TEXT NOT NULL,
    Couleur TEXT NOT NULL,
    Vitesse_Max REAL,
    Kilometrage REAL,
    Consommation_Moyenne REAL,
    Id_Utilisateur INTEGER,
    FOREIGN KEY(Id_Utilisateur) REFERENCES Utilisateurs(Id_Utilisateur)
);


CREATE TABLE Vendeurs (
    Id_Vendeur INTEGER PRIMARY KEY AUTOINCREMENT,
    Id_Utilisateur INTEGER,
    FOREIGN KEY(Id_Utilisateur) REFERENCES Utilisateurs(Id_Utilisateur)
);


CREATE TABLE Vente (
    Id_Vente INTEGER PRIMARY KEY AUTOINCREMENT,
    Id_Vehicule INTEGER,
    Id_Vendeur INTEGER,
    Date_mise_en_vente DATE,
    Prix_Vente REAL,
    FOREIGN KEY(Id_Vehicule) REFERENCES Vehicule(Id_Vehicule),
    FOREIGN KEY(Id_Vendeur) REFERENCES Vendeurs(Id_Vendeur)
);


CREATE TABLE Clients (
    Id_Client INTEGER PRIMARY KEY AUTOINCREMENT,
    Id_Utilisateur INTEGER,
    FOREIGN KEY(Id_Utilisateur) REFERENCES Utilisateurs(Id_Utilisateur)
);


CREATE TABLE Location (
    Id_Location INTEGER PRIMARY KEY AUTOINCREMENT,
    Id_Vehicule INTEGER,
    Id_Client INTEGER,
    Date_Debut DATE,
    Date_Fin DATE,
    Montant REAL,
    FOREIGN KEY(Id_Vehicule) REFERENCES Vehicule(Id_Vehicule),
    FOREIGN KEY(Id_Client) REFERENCES Clients(Id_Client)
);


CREATE TABLE Achat (
    Id_Achat INTEGER PRIMARY KEY AUTOINCREMENT,
    Id_Client INTEGER,
    Id_Vehicule INTEGER,
    Date_Achat DATE,
    Prix_Achat REAL,
    FOREIGN KEY(Id_Client) REFERENCES Clients(Id_Client),
    FOREIGN KEY(Id_Vehicule) REFERENCES Vehicule(Id_Vehicule)
);
