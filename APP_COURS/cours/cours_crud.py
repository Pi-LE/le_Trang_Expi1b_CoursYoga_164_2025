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
from APP_COURS.cours.cours_wtf_forms import FormWTFAddCours, FormWTFUpdateCours, FormWTFDeleteCours
from APP_COURS.database.database_tools import DBconnection
from APP_COURS.erreurs.exceptions import *

"""
Route afficher le cours
"""


@app.route("/cours_afficher/<string:order_by>/<int:id_cours_sel>", methods=['GET', 'POST'])
def cours_afficher(order_by, id_cours_sel):
    highlighted_id = request.args.get('highlighted_id', None)
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_cours_sel == 0:
                    strsql_cours_afficher = """SELECT * FROM t_cours ORDER BY Id_cours ASC"""
                    mc_afficher.execute(strsql_cours_afficher)
                elif order_by == "ASC":
                    valeur_Id_cours_selected_dictionnaire = {"value_Id_cours_selected": id_cours_sel}
                    strsql_cours_afficher = """SELECT Id_cours, Titre, Niveau, Session, 
                                            Prix_par_session, Description, Affiche
                                            FROM t_cours  WHERE Id_cours = %(value_Id_cours_selected)s
                                            ORDER BY Id_cours DESC """
                    mc_afficher.execute(strsql_cours_afficher, valeur_Id_cours_selected_dictionnaire)
                else:
                    strsql_cours_afficher = """SELECT * FROM t_cours                                     
                                                ORDER BY Id_cours DESC"""
                    mc_afficher.execute(strsql_cours_afficher)

                data_cours = mc_afficher.fetchall()

                print("data_cours ", data_cours, " Type : ", type(data_cours))

                if not data_cours and id_cours_sel == 0:
                    flash("""La table "t_cours" est vide. !!""", "warning")
                elif not data_cours and id_cours_sel > 0:
                    flash(f"La cours demandée n'existe pas !!", "warning")
                else:
                    flash(f"Données des cours affichées !!", "success")

        except Exception as Exception_cours_afficher:
            raise ExceptionCoursAfficherWTF(f"fichier : {Path(__file__).name}  ;  "
                                          f"{cours_afficher.__name__} ; "
                                          f"{Exception_cours_afficher}")
    return render_template("cours/cours_afficher.html", data=data_cours, highlighted_id=highlighted_id)




"""Route Ajouter Cours"""
@app.route("/cours_ajouter", methods=['GET', 'POST'])
def cours_ajouter_wtf():
    form = FormWTFAddCours()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                titre_cours_wtf = form.titre_cours_wtf.data
                niveau_cours_wtf = form.niveau_cours_wtf.data
                session_cours_wtf = form.session_cours_wtf.data
                prix_par_session_cours_wtf = form.prix_par_session_cours_wtf.data
                description_cours_wtf = form.description_cours_wtf.data
                affiche_cours_wtf = form.affiche_cours_wtf.data

                valeurs_insertion_dictionnaire = {
                    "value_titre_cours": titre_cours_wtf,
                    "value_niveau_cours": niveau_cours_wtf,
                    "value_session_cours": session_cours_wtf,
                    "value_prix_par_session": prix_par_session_cours_wtf,
                    "value_description": description_cours_wtf,
                    "value_affiche": affiche_cours_wtf
                }

                strsql_insert_cours = """INSERT INTO t_cours (Titre, Niveau, Session, Prix_par_session, Description, Affiche) 
                                         VALUES (%(value_titre_cours)s, %(value_niveau_cours)s, 
                                                 %(value_session_cours)s, %(value_prix_par_session)s, 
                                                 %(value_description)s, %(value_affiche)s)"""

                with DBconnection() as mconn_bd:

                    mconn_bd.execute(strsql_insert_cours, valeurs_insertion_dictionnaire)
                    mconn_bd.execute("ALTER TABLE t_cours AUTO_INCREMENT = 1")

                    flash("Données du cours insérées avec succès !!", "success")
                    # Récupérer l'ID du cours ajouté pour la mettre en surbrillance
                    mconn_bd.execute("SELECT LAST_INSERT_ID() as last_id")
                    last_id = mconn_bd.fetchone()['last_id']

                # Rediriger vers la page d'affichage des cours
                return redirect(url_for('cours_afficher', order_by='DESC', id_cours_sel=0, highlighted_id=last_id))

        except Exception as Exception_cours_ajouter_wtf:
            raise ExceptionCoursAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                           f"{cours_ajouter_wtf.__name__} ; "
                                           f"{Exception_cours_ajouter_wtf}")

    return render_template("cours/cours_add_wtf.html", form=form)




"""Route update"""

@app.route("/cours_update", methods=['GET', 'POST'])
def cours_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_personne"
    id_cours_update = request.values['id_cours_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdateCours()
    try:
        # 2023.05.14 OM S'il y a des listes déroulantes dans le formulaire
        # La validation pose quelques problèmes
        if request.method == "POST" and form_update.submit.data:

            titre_cours_update = form_update.titre_cours_Uwtf.data
            niveau_cours_update = form_update.niveau_cours_Uwtf.data
            session_cours_update = form_update.session_cours_Uwtf.data
            prix_par_session_cours_update = form_update.prix_par_session_cours_Uwtf.data
            description_cours_update= form_update.description_cours_Uwtf.data
            affiche_cours_update = form_update.affiche_cours_Uwtf.data

            valeur_update_dictionnaire = {
                "value_id_cours": id_cours_update,
                "value_titre_cours": titre_cours_update,
                "value_niveau_cours": niveau_cours_update,
                "value_session_cours": session_cours_update,
                "value_dprix_par_session_cours": prix_par_session_cours_update,
                "value_description_cours": description_cours_update,
                "value_affiche_cours": affiche_cours_update
            }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_cours = """UPDATE t_cours SET Titre = %(value_titre_cours)s, 
            Niveau = %(value_niveau_cours)s, Session = %(value_session_cours)s,
            Prix_par_session = %(value_dprix_par_session_cours)s, 
            Description = %(value_description_cours)s,Affiche =%(value_affiche_cours)s
            WHERE Id_cours = %(value_id_cours)s"""
            with DBconnection() as mconn_bd:

                mconn_bd.execute(str_sql_update_cours, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.

            return redirect(url_for('cours_afficher', order_by="DESC", id_cours_sel= id_cours_update, highlighted_id=id_cours_update))

        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_personne", "nom" et "prenom" de la "T_Personne"
            str_sql_id_cours = "SELECT Id_cours, Titre, Niveau, Session, Prix_par_session, Description,Affiche FROM t_cours " \
                                   "WHERE Id_cours = %(value_id_cours)s"
            valeur_select_dictionnaire = {"value_id_cours": id_cours_update,
                                        }

            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_cours, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom personne" pour l'UPDATE
            data_cours = mybd_conn.fetchone()
            print("data_cours ", data_cours, " type ", type(data_cours))

            # Afficher la valeur sélectionnée dans les champs du formulaire "personne_update_wtf.html"
            form_update.titre_cours_Uwtf.data = data_cours["Titre"]
            form_update.niveau_cours_Uwtf.data = data_cours["Niveau"]
            form_update.session_cours_Uwtf.data = data_cours["Session"]
            form_update.prix_par_session_cours_Uwtf.data = data_cours["Prix_par_session"]
            form_update.description_cours_Uwtf.data = data_cours["Description"]
            form_update.affiche_cours_Uwtf.data = data_cours["Affiche"]

    except Exception as Exception_cours_update_wtf:
        raise ExceptionCoursUpdaterWTF(f"fichier : {Path(__file__).name}  ; "
                                         f"{cours_update_wtf.__name__} ; "
                                         f"{Exception_cours_update_wtf}")

    return render_template("cours/cours_update_wtf.html", form_update=form_update)


"""#Route Delete"""


@app.route("/cours_delete", methods=['GET', 'POST'])
def cours_delete_wtf():
    data_cours_delete = None
    associations = None
    btn_submit_del = None
    id_cours_delete = request.values['id_cours_btn_delete_html']
    form_delete = FormWTFDeleteCours()
    try:
        if request.method == "POST":
            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("cours_afficher", order_by='ASC', id_cours_sel=0))

            if form_delete.submit_btn_confirmation.data:
                data_personne_delete = session['data_cours_delete']
                print("data_personne_delete ", data_personne_delete)
                flash("Effacer le cours de façon définitive de la BD !!!", "danger")
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_cours": id_cours_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                # des tables interméraires avec t cours
                delete_horaire_cours = """DELETE FROM t_horaire_cours WHERE FK_Cours = %(value_id_cours)s"""
                delete_inscrire_cours = """DELETE FROM T_InscrireCours WHERE FK_Cours = %(value_id_cours)s"""
                delete_enseigner_cours = """DELETE FROM T_EnseignerCours WHERE FK_Cours = %(value_id_cours)s"""
                delete_cours = """DELETE FROM t_cours WHERE Id_cours = %(value_id_cours)s"""

                with DBconnection() as mconn_bd:
                    # Suppression des associations (FK) liées à la personne
                    mconn_bd.execute(delete_horaire_cours,
                                     valeur_delete_dictionnaire)
                    mconn_bd.execute(delete_inscrire_cours,
                                     valeur_delete_dictionnaire)
                    mconn_bd.execute(delete_enseigner_cours,
                                     valeur_delete_dictionnaire)
                    # Suppression de la personne
                    mconn_bd.execute(delete_cours, valeur_delete_dictionnaire)

                flash("Cours définitivement effacée !!", "success")
                return redirect(url_for('cours_afficher', order_by="ASC", id_cours_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_cours": id_cours_delete}
            print(id_cours_delete, type(id_cours_delete))

            # Requête qui affiche la personne qui doit être efffacé.
            select_cours_info = """SELECT * FROM t_cours WHERE Id_cours = %(value_id_cours)s"""

            data_associations = """SELECT 
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
                            WHERE c.Id_cours = %(value_id_cours)s
                                """

            with DBconnection() as mydb_conn:
                mydb_conn.execute(select_cours_info, valeur_select_dictionnaire)
                data_cours_delete = mydb_conn.fetchall()
                print(data_cours_delete)  # Ajoutez ceci pour déboguer
                session['data_cours_delete'] = data_cours_delete

                mydb_conn.execute(data_associations, valeur_select_dictionnaire)
                associations = mydb_conn.fetchall()

            btn_submit_del = False

    except Exception as Exception_cours_delete_wtf:
        raise ExceptionCoursDeleteWtf(f"fichier : {Path(__file__).name}; "
                                         f"{cours_delete_wtf.__name__}; "
                                         f"{Exception_cours_delete_wtf}")

    return render_template("cours/cours_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_cours_delete=data_cours_delete,
                           associations=associations)


