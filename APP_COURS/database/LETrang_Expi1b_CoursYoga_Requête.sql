-- I.table annulation--
-- 1 Requête pour afficher toutes les annulations en ordre croissant--
SELECT a.ID_AnnulerCours, a.Raison,
       p.Nom, p.Prenom, p.NumeroAVS, 
       c.Titre, pm.Montant_paye
FROM t_annulation a
JOIN t_inscrirecours ic ON a.FK_Inscrirecours = ic.ID_InscrireCours
JOIN t_cours c ON ic.FK_Cours = c.Id_cours
JOIN t_personne p ON ic.FK_Personne = p.Id_personne
LEFT JOIN t_payement pm ON ic.ID_InscrireCours = pm.FK_Inscrirecours
ORDER BY a.ID_AnnulerCours ASC;


-- 2.Requête pour afficher les annulations  en ordre décroissant:--

SELECT a.ID_AnnulerCours, a.Raison,
       p.Nom, p.Prenom, p.NumeroAVS, 
       c.Titre, pm.Montant_paye
FROM t_annulation a
JOIN t_inscrirecours ic ON a.FK_Inscrirecours = ic.ID_InscrireCours
JOIN t_cours c ON ic.FK_Cours = c.Id_cours
JOIN t_personne p ON ic.FK_Personne = p.Id_personne
LEFT JOIN t_payement pm ON ic.ID_InscrireCours = pm.FK_Inscrirecours
ORDER BY a.ID_AnnulerCours DESC;




-- 3. requete pour charger cours--
SELECT ic.ID_InscrireCours, 
       c.Titre
FROM t_inscrirecours ic
JOIN t_cours c ON ic.FK_Cours = c.Id_cours
WHERE ic.FK_Personne = 1 AND NOT EXISTS (
    SELECT 1 FROM t_annulation a WHERE a.FK_Inscrirecours = ic.ID_InscrireCours
);

-- 4.Requête pour obtenir les associations de la personne et du cours liés à une inscription spécifique : --
SELECT p.Nom, p.Prenom, c.Titre 
FROM t_personne p
JOIN t_inscrirecours ic ON p.Id_personne = ic.FK_Personne
JOIN t_cours c ON ic.FK_Cours = c.Id_cours
WHERE ic.ID_InscrireCours = 1;


-- 5.Requête pour obtenir les informations d'une annulation spécifique : --
SELECT * FROM t_annulation WHERE ID_AnnulerCours = 1;


-- II COURS--
-- 1.Requête pour afficher tous les cours en ordre croissant --
SELECT * FROM t_cours ORDER BY Id_cours ASC;

-- 2.Requête pour afficher un cours spécifique en ordre décroissant --
SELECT Id_cours, Titre, Niveau, Session, 
       Prix_par_session, Description, Affiche
FROM t_cours  
WHERE Id_cours = 4 -- remplacer le id cours spécifique--
ORDER BY Id_cours DESC;

-- 3.Requête pour mettre à jour un cours--
UPDATE t_cours SET 
    Titre = 'Nouveau titre', 
    Niveau = 'Nouveau niveau', 
    Session = 'Nouvelle session',
    Prix_par_session = 150.0, 
    Description = 'Nouvelle description', 
    Affiche = 'Nouvelle affiche'
WHERE Id_cours = 1;

-- 4.Requête pour obtenir les détails d'un cours spécifique  --
SELECT Id_cours, Titre, Niveau, Session, Prix_par_session, Description, Affiche 
FROM t_cours 
WHERE Id_cours = 1;

-- 5.Requête pour obtenir les associations de la personne et du cours liés à une inscription spécifique --
SELECT 
    h.date_cours,
    h.jour_semaine,
    p.Nom,
    p.Prenom,
    f.Type_fonction
FROM t_cours c
JOIN t_horaire_cours hc ON hc.FK_cours = c.Id_cours
JOIN t_horaire h ON hc.FK_horaire = h.ID_horaire
JOIN t_enseignercours ec ON ec.FK_Cours = c.Id_cours
JOIN t_personne p ON ec.FK_Personne = p.Id_personne
JOIN t_avoirfonction af ON p.Id_personne = af.FK_Personne
JOIN t_fonction f ON af.FK_Fonction = f.ID_Fonction
WHERE c.Id_cours = 1;


-- III Route fonction ---
-- 1.Requête pour afficher toutes les fonctions en ordre croissant --
SELECT ID_Fonction, Type_fonction FROM t_fonction ORDER BY ID_Fonction ASC;

-- 2.Requête pour afficher une fonction spécifique --
SELECT ID_Fonction, Type_fonction FROM t_fonction WHERE ID_Fonction = 1;

-- 3.Requête pour obtenir les informations d'une fonction spécifique à supprimer --
SELECT ID_avoirFonction, f.ID_Fonction, f.Type_fonction, 
       p.Id_personne, p.Nom, p.Prenom, p.Date_naissance, p.NumeroAVS
FROM t_avoirFonction AS AF
INNER JOIN t_personne p ON AF.fk_personne = p.Id_personne
INNER JOIN t_fonction AS f ON AF.fk_fonction = f.ID_Fonction
WHERE fk_fonction = 1;

-- IV--
-- 1. --Requête pour afficher tous les horaires en ordre croissant--
SELECT * FROM t_horaire ORDER BY ID_horaire;

-- 2.Requête pour afficher un horaire spécifique en ordre décroissant  --
SELECT ID_horaire, date_cours, jour_semaine, heure_debut, heure_fin 
FROM t_horaire  
WHERE ID_horaire = 1
ORDER BY ID_horaire DESC;

-- 3.Requête pour ajouter un nouvel horaire --
INSERT INTO t_horaire (date_cours, jour_semaine, heure_debut, heure_fin) 
VALUES ('2021-12-01', 'Lundi', '08:00:00', '10:00:00');

-- 4. Requête pour mettre à jour un horaire --
UPDATE t_horaire SET 
    date_cours = '2021-12-01', 
    jour_semaine = 'Mardi', 
    heure_debut = '09:00:00', 
    heure_fin = '11:00:00'
WHERE ID_horaire = 1;

-- 5.Requête pour obtenir les détails d'un horaire spécifique--
SELECT ID_horaire, date_cours, jour_semaine, heure_debut, heure_fin 
FROM t_horaire 
WHERE ID_horaire = 1;

-- 6.Requête pour obtenir les associations liées à un horaire spécifique--
SELECT 
    c.Titre,
    c.Niveau,
    c.Session,
    c.Prix_par_session,
    c.Description,
    c.Affiche
FROM t_horaire h
JOIN t_horaire_cours hc ON hc.FK_Horaire = h.ID_horaire
JOIN t_cours c ON hc.FK_Cours = c.Id_cours
WHERE h.ID_horaire = 1;

-- VI inscrire cours requêtes --
-- 1. Requête pour afficher les inscriptions avec toutes les personnes --
SELECT
    p.Id_personne, p.Nom, p.Prenom, p.Date_naissance, p.Sexe,
    GROUP_CONCAT(c.Titre) AS CoursInscrits
FROM
    t_personne p
LEFT JOIN t_inscrirecours ic ON p.Id_personne = ic.FK_Personne
LEFT JOIN t_cours c ON c.Id_cours = ic.FK_Cours
WHERE p.Id_personne NOT IN (
    SELECT ec.FK_Personne
    FROM t_enseignercours ec
)
GROUP BY
    p.Id_personne;

-- 2.Requête pour afficher les inscriptions pour une personne spécifique --
SELECT
    p.Id_personne, p.Nom, p.Prenom, p.Date_naissance, p.Sexe,
    GROUP_CONCAT(c.Titre) AS CoursInscrits
FROM
    t_personne p
LEFT JOIN t_inscrirecours ic ON p.Id_personne = ic.FK_Personne
LEFT JOIN t_cours c ON c.Id_cours = ic.FK_Cours
WHERE p.Id_personne NOT IN (
    SELECT ec.FK_Personne
    FROM t_enseignercours ec
)
GROUP BY
    p.Id_personne
HAVING p.Id_personne = 1;

-- 3. Requête pour afficher les inscriptions pour une personne spécifique --
SELECT
    p.Id_personne, p.Nom, p.Prenom, p.Date_naissance, p.Sexe,
    GROUP_CONCAT(c.Titre) AS CoursInscrits
FROM
    t_personne p
LEFT JOIN t_inscrirecours ic ON p.Id_personne = ic.FK_Personne
LEFT JOIN t_cours c ON c.Id_cours = ic.FK_Cours
WHERE p.Id_personne NOT IN (
    SELECT ec.FK_Personne
    FROM t_enseignercours ec
)
GROUP BY
    p.Id_personne
HAVING p.Id_personne = 1;

-- 4.Requête pour sélectionner les détails de la personne et ses cours inscrits--
SELECT Id_personne, Nom, Prenom, Date_naissance, Sexe,
       GROUP_CONCAT(Id_cours) AS CoursInscrits
FROM t_inscrirecours
INNER JOIN t_personne ON t_personne.Id_personne = t_inscrirecours.FK_Personne
INNER JOIN t_cours ON t_cours.Id_cours = t_inscrirecours.FK_Cours
WHERE Id_personne = 1
GROUP BY Id_personne;

-- 5. Requête pour obtenir les cours non attribués à la personne --
SELECT Id_personne, Nom, Prenom, Date_naissance, Sexe,
       GROUP_CONCAT(Id_cours) AS CoursInscrits
FROM t_inscrirecours
INNER JOIN t_personne ON t_personne.Id_personne = t_inscrirecours.FK_Personne
INNER JOIN t_cours ON t_cours.Id_cours = t_inscrirecours.FK_Cours
WHERE Id_personne = 1
GROUP BY Id_personne;


-- VII payement--
-- 1. Requête pour afficher tous les paiements en ordre croissant--
SELECT pm.ID_payement, 
       p.Nom, p.Prenom, p.NumeroAVS, 
       c.Titre, c.Prix_par_session, pm.Montant_restant,
       pm.Mode_paiement, pm.Montant_paye, pm.Montant_principal, pm.Statut, pm.Rabais,
       pm.Description_Rabais
FROM t_payement pm
JOIN t_inscrirecours ic ON pm.FK_Inscrirecours = ic.ID_InscrireCours
JOIN t_cours c ON ic.FK_Cours = c.Id_cours
JOIN t_personne p ON ic.FK_Personne = p.Id_personne
ORDER BY pm.ID_payement ASC;


-- 2. Requête pour afficher les paiements pour une personne spécifique en ordre croissant--
SELECT pm.ID_payement, 
       p.Nom, p.Prenom, p.NumeroAVS, 
       c.Titre, c.Prix_par_session, pm.Montant_principal,
       pm.Mode_paiement, pm.Montant_paye, pm.Statut, pm.Rabais, pm.Montant_restant,
       pm.Description_Rabais
FROM t_payement pm
JOIN t_inscrirecours ic ON pm.FK_Inscrirecours = ic.ID_InscrireCours
JOIN t_cours c ON ic.FK_Cours = c.Id_cours
JOIN t_personne p ON ic.FK_Personne = p.Id_personne
WHERE p.Id_personne = 1
ORDER BY pm.ID_payement ASC;

-- 3.Requête pour afficher tous les paiements en ordre décroissant --
SELECT pm.ID_payement, 
       p.Nom, p.Prenom, p.NumeroAVS, 
       c.Titre, c.Prix_par_session, pm.Montant_principal,
       pm.Mode_paiement, pm.Montant_paye, pm.Statut, pm.Rabais, pm.Montant_restant,
       pm.Description_Rabais
FROM t_payement pm
JOIN t_inscrirecours ic ON pm.FK_Inscrirecours = ic.ID_InscrireCours
JOIN t_cours c ON ic.FK_Cours = c.Id_cours
JOIN t_personne p ON ic.FK_Personne = p.Id_personne
ORDER BY pm.ID_payement DESC;

-- 4. Requête pour récupérer le prix par session à partir de l'ID du cours --
SELECT c.Prix_par_session 
FROM t_inscrirecours ic
JOIN t_cours c ON ic.FK_Cours = c.Id_cours
WHERE ic.ID_InscrireCours = 1;

-- 5. Requête pour charger les cours disponibles pour une personne spécifique --
SELECT ic.ID_InscrireCours, 
       c.Titre, 
       c.Prix_par_session  
FROM t_inscrirecours ic
JOIN t_cours c ON ic.FK_Cours = c.Id_cours
WHERE ic.FK_Personne = 1 AND NOT EXISTS (
    SELECT 1 FROM t_payement pm WHERE pm.FK_Inscrirecours = ic.ID_InscrireCours);

-- 6. Requête pour obtenir les détails d'un paiement spécifique --
SELECT 
    ID_payement, 
    FK_Inscrirecours, 
    Montant_principal, 
    Rabais, 
    Description_Rabais, 
    Montant_paye,
    Montant_restant,
    Mode_paiement,
    Statut 
FROM t_payement 
WHERE ID_payement = 1;

-- 7.Requête pour obtenir les informations de la personne et du cours liés à une inscription spécifique--
SELECT 
    p.Nom, 
    p.Prenom, 
    c.Titre 
FROM t_personne p
JOIN t_inscrirecours ic ON p.Id_personne = ic.FK_Personne
JOIN t_cours c ON ic.FK_Cours = c.Id_cours
WHERE ic.ID_InscrireCours = 1;

-- 8.Requête pour obtenir les informations de la personne et du cours liés à une inscription spécifique--
SELECT 
    p.Nom, 
    p.Prenom, 
    c.Titre 
FROM t_personne p
JOIN t_inscrirecours ic ON p.Id_personne = ic.FK_Personne
JOIN t_cours c ON ic.FK_Cours = c.Id_cours
WHERE ic.ID_InscrireCours = 1;


-- VIII Personne--
-- 1. Requête pour afficher toutes les personnes en ordre croissant--
SELECT Id_personne, Nom, Prenom, Date_naissance, NumeroAVS, Sexe, date_enregistre 
FROM T_Personne 
ORDER BY Id_personne ASC;

-- 2. Requête pour afficher toutes les personnes en ordre décroissant--
SELECT Id_personne, Nom, Prenom, Date_naissance, NumeroAVS, Sexe, date_enregistre 
FROM T_Personne 
ORDER BY Id_personne DESC;

-- 3. ajouter une nouvelle personne--
INSERT INTO T_Personne (Nom, Prenom, Date_naissance, NumeroAVS, Sexe) 
VALUES ('Nom', 'Prenom', '2000-01-01', '756.1234.5678.90', 'Masculin');

-- 4. Requête pour mettre à jour une personne--
UPDATE T_Personne SET 
    Nom = 'nouveau_nom', 
    Prenom = 'nouveau_prenom', 
    Date_naissance = '2000-01-01',
    NumeroAVS = '756.1234.5678.90', 
    Sexe = 'Masculin'
WHERE Id_personne = 1;

-- 5. Requête pour obtenir les détails d'une personne spécifique  --
SELECT Id_personne, Nom, Prenom, Date_naissance, NumeroAVS, Sexe 
FROM T_Personne 
WHERE Id_personne = 1;

-- 6. Requête pour obtenir les associations liées à une personne spécifique-- 
SELECT 
    t_personne.Id_personne,
    t_fonction.Type_fonction,
    t_cours.Titre AS Titre_cours,
    t_inscrirecours.date_inscrire AS Date_inscription,
    t_payement.Statut AS Statut_paiement,
    t_annulation.Raison AS Raison_annulation,
    t_enseignercours.Description AS Description_enseignement
FROM t_personne
LEFT JOIN t_avoirfonction ON t_avoirfonction.FK_Personne = t_personne.Id_personne
LEFT JOIN t_fonction ON t_avoirfonction.FK_Fonction = t_fonction.ID_Fonction
LEFT JOIN t_inscrirecours ON t_inscrirecours.FK_Personne = t_personne.Id_personne
LEFT JOIN t_cours ON t_inscrirecours.FK_Cours = t_cours.Id_cours
LEFT JOIN t_payement ON t_payement.FK_Inscrirecours = t_inscrirecours.ID_InscrireCours
LEFT JOIN t_annulation ON t_annulation.FK_Inscrirecours = t_inscrirecours.ID_InscrireCours
LEFT JOIN t_enseignercours ON t_enseignercours.FK_Personne = t_personne.Id_personne
WHERE t_personne.Id_personne = 1;











