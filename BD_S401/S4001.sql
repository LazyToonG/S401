DROP TABLE IF EXISTS Jouer;
DROP TABLE IF EXISTS Enregistre;
DROP TABLE IF EXISTS Identifier;
DROP TABLE IF EXISTS Lecteur;
DROP TABLE IF EXISTS Logs;
DROP TABLE IF EXISTS Message;
DROP TABLE IF EXISTS Utilisateur;
DROP TABLE IF EXISTS Planning;
DROP TABLE IF EXISTS Playlist;
DROP TABLE IF EXISTS Serveur;
DROP TABLE IF EXISTS Entreprise;
DROP TABLE IF EXISTS Musique;


CREATE TABLE Musique(
   idMusique INT,
   nomMusique VARCHAR(50),
   genre VARCHAR(50) NOT NULL,
   auteur VARCHAR(50) NOT NULL,
   durée DECIMAL(15,2) NOT NULL,
   lien VARCHAR(50) NOT NULL,
   PRIMARY KEY(idMusique)
);

CREATE TABLE Entreprise(
   idEntreprise INT,
   nomEntreprise VARCHAR(50) NOT NULL,
   type VARCHAR(50),
   lieu VARCHAR(50) NOT NULL,
   PRIMARY KEY(idEntreprise)
);

CREATE TABLE Playlist(
   idPlaylist INT,
   idMusique INT,
   PRIMARY KEY(idPlaylist),
   FOREIGN KEY(idMusique) REFERENCES Musique(idMusique)
);

CREATE TABLE Serveur(
   idServeur INT,
   PRIMARY KEY(idServeur)
);

CREATE TABLE Planning(
   idPlanning INT,
   jour VARCHAR(10),
   idPlaylist INT NOT NULL,
   PRIMARY KEY(idPlanning),
   FOREIGN KEY(idPlaylist) REFERENCES Playlist(idPlaylist)
);

CREATE TABLE Utilisateur(
   idUtilisateur INT,
   nom VARCHAR(50) NOT NULL,
   mdp VARCHAR(20) NOT NULL,
   role VARCHAR(15) NOT NULL,
   idEntreprise INT NOT NULL,
   PRIMARY KEY(idUtilisateur),
   FOREIGN KEY(idEntreprise) REFERENCES Entreprise(idEntreprise)
);

CREATE TABLE Message(
   idMessage INT,
   theme VARCHAR(50),
   idEntreprise INT,
   message VARCHAR(100),
   idPlanning INT NOT NULL,
   PRIMARY KEY(idMessage),
   FOREIGN KEY(idPlanning) REFERENCES Planning(idPlanning)
);

CREATE TABLE Logs(
   idLogs INT,
   idServeur INT NOT NULL,
   PRIMARY KEY(idLogs),
   FOREIGN KEY(idServeur) REFERENCES Serveur(idServeur)
);

CREATE TABLE Lecteur(
   idLecteur INT,
   localisation VARCHAR(50) NOT NULL,
   etat BOOLEAN NOT NULL,
   idServeur INT NOT NULL,
   PRIMARY KEY(idLecteur),
   FOREIGN KEY(idServeur) REFERENCES Serveur(idServeur)
);

CREATE TABLE Identifier(
   idEntreprise INT,
   idServeur INT,
   PRIMARY KEY(idEntreprise, idServeur),
   FOREIGN KEY(idEntreprise) REFERENCES Entreprise(idEntreprise),
   FOREIGN KEY(idServeur) REFERENCES Serveur(idServeur)
);

CREATE TABLE Enregistre(
   idServeur INT,
   idPlanning INT,
   PRIMARY KEY(idServeur, idPlanning),
   FOREIGN KEY(idServeur) REFERENCES Serveur(idServeur),
   FOREIGN KEY(idPlanning) REFERENCES Planning(idPlanning)
);

CREATE TABLE Jouer(
   idMusique INT,
   idPlanning INT,
   PRIMARY KEY(idMusique, idPlanning),
   FOREIGN KEY(idMusique) REFERENCES Musique(idMusique),
   FOREIGN KEY(idPlanning) REFERENCES Planning(idPlanning)
);
