DROP TABLE IF EXISTS Entreprise;
DROP TABLE IF EXISTS Lecteur;
DROP TABLE IF EXISTS Planning;
DROP TABLE IF EXISTS Musique;
DROP TABLE IF EXISTS Utilisateur;
DROP TABLE IF EXISTS Message;
DROP TABLE IF EXISTS Playlist;
DROP TABLE IF EXISTS Logs;
DROP TABLE IF EXISTS Ajouter;



CREATE TABLE Entreprise(
   idEntreprise INT,
   nomEntreprise VARCHAR(50) NOT NULL,
   PRIMARY KEY(idEntreprise),
   UNIQUE(nomEntreprise)
);

CREATE TABLE Lecteur(
   idLecteur INT,
   ip VARCHAR(50) NOT NULL,
   nomLecteur VARCHAR(50) NOT NULL,
   idEntreprise INT NOT NULL,
   PRIMARY KEY(idLecteur),
   UNIQUE(ip),
   FOREIGN KEY(idEntreprise) REFERENCES Entreprise(idEntreprise)
);

CREATE TABLE Planning(
   idPlanning INT,
   heureDiffusion TIME NOT NULL,
   jour VARCHAR(10) NOT NULL,
   intervalle VARCHAR(50),
   idUtilisateur INT NOT NULL,
   PRIMARY KEY(idPlanning),
   UNIQUE(idUtilisateur),
   FOREIGN KEY(idUtilisateur) REFERENCES Utilisateur(idUtilisateur)
);

CREATE TABLE Musique(
   idMusique INT,
   nomMusique VARCHAR(50) NOT NULL,
   duree INT NOT NULL,
   idEntreprise INT NOT NULL,
   PRIMARY KEY(idMusique),
   FOREIGN KEY(idEntreprise) REFERENCES Entreprise(idEntreprise)
);

CREATE TABLE Utilisateur(
   idUtilisateur INT,
   nom VARCHAR(50) NOT NULL,
   mdp VARCHAR(100) NOT NULL,
   role VARCHAR(15) NOT NULL,
   mail VARCHAR(50) NOT NULL,
   idEntreprise INT NOT NULL,
   PRIMARY KEY(idUtilisateur),
   UNIQUE(mail),
   FOREIGN KEY(idEntreprise) REFERENCES Entreprise(idEntreprise)
);

CREATE TABLE Message(
   idMessage INT,
   nomFichierMessage VARCHAR(100) NOT NULL,
   duree INT NOT NULL,
   idEntreprise INT NOT NULL,
   idPlanning INT,
   PRIMARY KEY(idMessage),
   FOREIGN KEY(idEntreprise) REFERENCES Entreprise(idEntreprise),
   FOREIGN KEY(idPlanning) REFERENCES Planning(idPlanning)
);

CREATE TABLE Playlist(
   idPlaylist INT,
   idUtilisateur INT NOT NULL,
   idPlanning INT,
   PRIMARY KEY(idPlaylist),
   FOREIGN KEY(idUtilisateur) REFERENCES Utilisateur(idUtilisateur),
   FOREIGN KEY(idPlanning) REFERENCES Planning(idPlanning)
);

CREATE TABLE Logs(
   idLogs INT,
   nomFichierLog VARCHAR(25) NOT NULL,
   idLecteur INT NOT NULL,
   PRIMARY KEY(idLogs),
   UNIQUE(nomFichierLog),
   FOREIGN KEY(idLecteur) REFERENCES Lecteur(idLecteur)
);

CREATE TABLE Ajouter(
   idMusique INT,
   idPlaylist INT,
   PRIMARY KEY(idMusique, idPlaylist),
   FOREIGN KEY(idMusique) REFERENCES Musique(idMusique),
   FOREIGN KEY(idPlaylist) REFERENCES Playlist(idPlaylist)
);
