"""Gestion des "routes" FLASK et des données pour les genres.
Fichier : gestion_genres_crud.py
Auteur : OM 2021.03.16
"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_COURS import app
from APP_COURS.database.database_tools import DBconnection
from APP_COURS.erreurs.exceptions import *
from APP_COURS.personnes.personnes_wtf_forms import FormWTFAjouterPersonne
from APP_COURS.personnes.personnes_wtf_forms import FormWTFUpdatePersonne
from APP_COURS.personnes.personnes_wtf_forms import FormWTFDeletePersonne



"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /personnes_afficher
    
    Test : ex : http://127.0.0.1:5575/personnes_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_personne_sel = 0 >> toutes les personnes.
                id_personne_sel = "n" affiche la personne dont l'id est "n"
"""
@app.route("/personnes_afficher/<string:order_by>/<int:id_personne_sel>", methods=['GET', 'POST'])
def personnes_afficher(order_by, id_personne_sel):
    highlighted_id = request.args.get('highlighted_id', None)
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_personne_sel == 0:
                    strsql_personnes_afficher = """SELECT Id_personne, Nom, Prenom, Date_naissance, NumeroAVS, Sexe,date_enregistre 
                                                    FROM T_Personne ORDER BY Id_personne ASC"""
                    mc_afficher.execute(strsql_personnes_afficher)
                elif order_by == "ASC":
                    valeur_id_personne_selected_dictionnaire = {"value_id_personne_selected": id_personne_sel}
                    strsql_personnes_afficher = """SELECT Id_personne, Nom, Prenom, Date_naissance, NumeroAVS, Sexe,date_enregistre 
                                                    FROM T_Personne WHERE Id_personne = %(value_id_personne_selected)s
                                                    ORDER BY Id_personne DESC"""
                    mc_afficher.execute(strsql_personnes_afficher, valeur_id_personne_selected_dictionnaire)
                else:
                    strsql_personnes_afficher = """SELECT Id_personne, Nom, Prenom, Date_naissance, NumeroAVS, Sexe,date_enregistre 
                                                FROM T_Personne ORDER BY Id_personne DESC"""
                    mc_afficher.execute(strsql_personnes_afficher)

                data_personnes = mc_afficher.fetchall()

                if not data_personnes and id_personne_sel == 0:
                    flash("""La table "T_Personne" est vide. !!""", "warning")
                elif not data_personnes and id_personne_sel > 0:
                    flash(f"La personne demandée n'existe pas !!", "warning")
                else:
                    flash(f"Données personnes affichées !!", "success")

        except Exception as Exception_personnes_afficher:
            raise ExceptionPersonnesAfficher(f"fichier : {Path(__file__).name}  ;  "
                                             f"{personnes_afficher.__name__} ; "
                                             f"{Exception_personnes_afficher}")

    return render_template("personnes/personnes_afficher.html", data=data_personnes,highlighted_id=highlighted_id)


"""Route Ajouter"""
@app.route("/personnes_ajouter", methods=['GET', 'POST'])
def personnes_ajouter_wtf():
    form = FormWTFAjouterPersonne()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                nom_personne_wtf = form.nom_personne_wtf.data
                prenom_personne_wtf = form.prenom_personne_wtf.data
                date_naissance_wtf = form.date_naissance_personne_wtf.data
                numero_avs_wtf = form.numero_avs_personne_wtf.data
                sexe_wtf = form.sexe_personne_wtf.data

                valeurs_insertion_dictionnaire = {
                    "value_nom_personne": nom_personne_wtf,
                    "value_prenom_personne": prenom_personne_wtf,
                    "value_date_naissance": date_naissance_wtf,
                    "value_numero_avs": numero_avs_wtf,
                    "value_sexe": sexe_wtf
                }

                strsql_insert_personne = """INSERT INTO T_Personne (Nom, Prenom, Date_naissance, NumeroAVS, Sexe) 
                                            VALUES (%(value_nom_personne)s, %(value_prenom_personne)s, 
                                                    %(value_date_naissance)s, %(value_numero_avs)s, %(value_sexe)s)"""

                with DBconnection() as mconn_bd:
                    mconn_bd.execute("ALTER TABLE T_Personne AUTO_INCREMENT = 1")
                    mconn_bd.execute(strsql_insert_personne, valeurs_insertion_dictionnaire)

                    flash(f"Données insérées avec succès !!", "success")
                    # Récupérer l'ID du cours ajouté pour la mettre en surbrillance
                    mconn_bd.execute("SELECT LAST_INSERT_ID() as last_id")
                    last_id = mconn_bd.fetchone()['last_id']

                # Rediriger vers la page d'affichage des personnes
                return redirect(url_for('personnes_afficher', order_by='DESC', id_personne_sel=0,highlighted_id=last_id))

        except Exception as Exception_personnes_ajouter_wtf:
            raise ExceptionPersonnesAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                               f"{personnes_ajouter_wtf.__name__} ; "
                                               f"{Exception_personnes_ajouter_wtf}")

    return render_template("personnes/personnes_ajouter_wtf.html", form=form)



"""
    Auteur : OM 2021.03.22
    Définition d'une "route" /personnes_ajouter

    Test : ex : http://127.0.0.1:5575/personnes_ajouter

    Paramètres : sans

    But : Ajouter une personne

    Remarque :  Dans les champs du formulaire "personnes/personnes_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On ne doit pas accepter des valeurs vides pour Nom et Prenom.
                La Date de Naissance doit être une date valide au format "YYYY-MM-DD".
                Le Numéro AVS doit être une chaîne de 13 caractères.
                Le sexe doit être 'Masculin' ou 'Féminin'.
"""


@app.route("/personne_update", methods=['GET', 'POST'])
def personne_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_personne"
    id_personne_update = request.values['id_personne_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdatePersonne()
    try:
        # 2023.05.14 OM S'il y a des listes déroulantes dans le formulaire
        # La validation pose quelques problèmes
        if request.method == "POST" and form_update.submit.data:
            # Récupèrer la valeur du champ depuis "personne_update_wtf.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.
            nom_personne_update = form_update.nom_personne_update_wtf.data
            nom_personne_update = nom_personne_update.lower()
            prenom_personne_update = form_update.prenom_personne_update_wtf.data
            prenom_personne_update = prenom_personne_update.lower()
            date_naissance_personne_essai = form_update.date_naissance_personne_wtf_essai.data
            numero_avs_personne_update = form_update.numero_avs_personne_wtf.data
            sexe_personne_update = form_update.sexe_personne_wtf.data

            valeur_update_dictionnaire = {
                "value_id_personne": id_personne_update,
                "value_nom_personne": nom_personne_update,
                "value_prenom_personne": prenom_personne_update,
                "value_date_naissance_personne_essai": date_naissance_personne_essai,
                "value_numero_avs_personne": numero_avs_personne_update,
                "value_sexe_personne": sexe_personne_update
            }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_personne = """UPDATE T_Personne SET Nom = %(value_nom_personne)s, 
            Prenom = %(value_prenom_personne)s, Date_naissance = %(value_date_naissance_personne_essai)s,
            NumeroAVS = %(value_numero_avs_personne)s, Sexe = %(value_sexe_personne)s
            WHERE Id_personne = %(value_id_personne)s"""
            with DBconnection() as mconn_bd:
                mconn_bd.execute("ALTER TABLE T_Personne AUTO_INCREMENT = 1")

                mconn_bd.execute(str_sql_update_personne, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_personne_update"
            return redirect(url_for('personnes_afficher', order_by="DESC", id_personne_sel= id_personne_update,highlighted_id=id_personne_update ))

        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_personne", "nom" et "prenom" de la "T_Personne"
            str_sql_id_personne = "SELECT Id_personne, Nom, Prenom, Date_naissance, NumeroAVS, Sexe FROM T_Personne " \
                                   "WHERE Id_personne = %(value_id_personne)s"
            valeur_select_dictionnaire = {"value_id_personne": id_personne_update}

            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_personne, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom personne" pour l'UPDATE
            data_nom_prenom_personne = mybd_conn.fetchone()
            print("data_nom_prenom_personne ", data_nom_prenom_personne, " type ", type(data_nom_prenom_personne))

            # Afficher la valeur sélectionnée dans les champs du formulaire "personne_update_wtf.html"
            form_update.nom_personne_update_wtf.data = data_nom_prenom_personne["Nom"]
            form_update.prenom_personne_update_wtf.data = data_nom_prenom_personne["Prenom"]
            form_update.date_naissance_personne_wtf_essai.data = data_nom_prenom_personne["Date_naissance"]
            form_update.numero_avs_personne_wtf.data = data_nom_prenom_personne["NumeroAVS"]
            form_update.sexe_personne_wtf.data = data_nom_prenom_personne["Sexe"]

    except Exception as Exception_personne_update_wtf:
        raise ExceptionPersonneUpdateWtf(f"fichier : {Path(__file__).name}  ; "
                                         f"{personne_update_wtf.__name__} ; "
                                         f"{Exception_personne_update_wtf}")

    return render_template("personnes/personne_update_wtf.html", form_update=form_update)





"""#Route Delete"""


@app.route("/personne_delete", methods=['GET', 'POST'])
def personne_delete_wtf():
    data_personne_delete = None
    associations = None
    btn_submit_del = None
    id_personne_delete = request.values['id_personne_btn_delete_html']
    form_delete = FormWTFDeletePersonne()
    try:
        if request.method == "POST":
            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("personnes_afficher", order_by='ASC', id_personne_sel=0))

            if form_delete.submit_btn_conf_del.data:
                data_personne_delete = session['data_personne_delete']
                flash("Effacer la personne de façon définitive de la BD !!!", "danger")
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_personne": id_personne_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                # des tables intermédiaires avec t personne
                delete_avoir_fonction = """DELETE FROM T_AvoirFonction WHERE FK_Personne = %(value_id_personne)s"""
                delete_inscrire_cours = """DELETE FROM T_InscrireCours WHERE FK_Personne = %(value_id_personne)s"""
                delete_enseigner_cours = """DELETE FROM T_EnseignerCours WHERE FK_Personne = %(value_id_personne)s"""
                delete_payement = """DELETE FROM t_payement 
                                    WHERE FK_Inscrirecours IN (SELECT ID_InscrireCours FROM T_InscrireCours WHERE FK_Personne = %(value_id_personne)s)"""
                delete_annulation = """DELETE FROM t_annulation 
                                                    WHERE FK_Inscrirecours IN (SELECT ID_InscrireCours FROM T_InscrireCours WHERE FK_Personne = %(value_id_personne)s)"""
                delete_personne = """DELETE FROM T_Personne WHERE Id_personne = %(value_id_personne)s"""

                with DBconnection() as mconn_bd:
                    # Suppression des associations (FK) liées à la personne
                    mconn_bd.execute(delete_avoir_fonction, valeur_delete_dictionnaire)
                    mconn_bd.execute(delete_payement, valeur_delete_dictionnaire)
                    mconn_bd.execute(delete_annulation, valeur_delete_dictionnaire)
                    mconn_bd.execute(delete_inscrire_cours, valeur_delete_dictionnaire)
                    mconn_bd.execute(delete_enseigner_cours, valeur_delete_dictionnaire)
                    # Suppression de la personne
                    mconn_bd.execute(delete_personne, valeur_delete_dictionnaire)

                flash("Personne définitivement effacée !!", "success")
                return redirect(url_for('personnes_afficher', order_by="ASC", id_personne_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_personne": id_personne_delete}
            print(id_personne_delete, type(id_personne_delete))

            # Requête qui affiche la personne qui doit être effacée.
            select_personne_info = """SELECT * FROM T_Personne WHERE Id_personne = %(value_id_personne)s"""

            data_associations = """SELECT 
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
                                WHERE t_personne.Id_personne = %(value_id_personne)s
                                """

            with DBconnection() as mydb_conn:
                mydb_conn.execute(select_personne_info, valeur_select_dictionnaire)
                data_personne_delete = mydb_conn.fetchall()
                print(data_personne_delete)  # Ajoutez ceci pour déboguer
                session['data_personne_delete'] = data_personne_delete

                mydb_conn.execute(data_associations, valeur_select_dictionnaire)
                associations = mydb_conn.fetchall()

            btn_submit_del = False

    except Exception as Exception_personne_delete_wtf:
        raise ExceptionPersonneDeleteWtf(f"fichier : {Path(__file__).name}; "
                                         f"{personne_delete_wtf.__name__}; "
                                         f"{Exception_personne_delete_wtf}")

    return render_template("personnes/personne_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_personne_del=data_personne_delete,
                           associations=associations)
