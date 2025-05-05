"""Gestion des "routes" FLASK et des données pour les genres.
Fichier : gestion_genres_crud.py
Auteur : OM 2021.03.16
"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for
from datetime import date, time, timedelta



from APP_COURS import app
from APP_COURS.horaire.horaire_wtf_forms import FormWTFAjouterHoraire,FormWTFUpdateHoraire,FormWTFDeleteHoraire
from APP_COURS.database.database_tools import DBconnection
from APP_COURS.erreurs.exceptions import *

"""
Route afficher l'horaire'
"""


@app.route("/horaire_afficher/<string:order_by>/<int:id_horaire_sel>", methods=['GET', 'POST'])
def horaire_afficher(order_by, id_horaire_sel):
    highlighted_id = request.args.get('highlighted_id', None)
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_horaire_sel == 0:
                    strsql_horaire_afficher = """SELECT * FROM t_horaire ORDER BY ID_horaire ASC"""
                    mc_afficher.execute(strsql_horaire_afficher)
                elif order_by == "ASC":
                    valeur_Id_cours_selected_dictionnaire = {"value_Id_horaire_selected": id_horaire_sel}
                    strsql_horaire_afficher = """SELECT ID_horaire, date_cours, jour_semaine, heure_debut, 
                                            heure_fin FROM t_horaire  
                                            WHERE ID_horaire = %(value_Id_horaire_selected)s
                                            ORDER BY ID_horaire DESC """
                    mc_afficher.execute(strsql_horaire_afficher, valeur_Id_cours_selected_dictionnaire)
                else:
                    strsql_cours_afficher = """SELECT * FROM t_horaire                                     
                                                ORDER BY ID_horaire DESC"""
                    mc_afficher.execute(strsql_cours_afficher)

                data_horaire = mc_afficher.fetchall()

                print("data_horaire ", data_horaire, " Type : ", type(data_horaire))

                if not data_horaire and id_horaire_sel == 0:
                    flash("""La table "t_horaire" est vide. !!""", "warning")
                elif not data_horaire and id_horaire_sel > 0:
                    flash(f"L'horaire' demandée n'existe pas !!", "warning")
                else:
                    flash(f"Données des horaires affichées !!", "success")

        except Exception as Exception_horaire_afficher:
            raise ExceptionHoraireAfficherWTF(f"fichier : {Path(__file__).name}  ;  "
                                          f"{horaire_afficher.__name__} ; "
                                          f"{Exception_horaire_afficher}")
    return render_template("horaire/horaire_afficher.html", data=data_horaire, highlighted_id=highlighted_id)




"""Route Ajouter Cours"""
@app.route("/horaire_ajouter", methods=['GET', 'POST'])
def horaire_ajouter_wtf():
    form = FormWTFAjouterHoraire()
    if request.method == "POST":
        if form.validate_on_submit():
            valeurs_insertion_dictionnaire = {
                "value_date_cours": form.date_cours_wtf.data,
                "value_jour_semaine": form.jour_semaine_wtf.data,
                "value_heure_debut": form.heure_debut_wtf.data,
                "value_heure_fin": form.heure_fin_wtf.data
            }
            strsql_insert_horaire = """INSERT INTO t_horaire (date_cours, jour_semaine, heure_debut, heure_fin) 
                                       VALUES (%(value_date_cours)s, %(value_jour_semaine)s, 
                                               %(value_heure_debut)s, %(value_heure_fin)s)"""
            try:
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_horaire, valeurs_insertion_dictionnaire)
                    mconn_bd.execute("SELECT LAST_INSERT_ID() as last_id")
                    last_id = mconn_bd.fetchone()['last_id']
                flash("Données de l'horaire insérées avec succès !", "success")
                return redirect(url_for('horaire_afficher', order_by='DESC', id_horaire_sel=0, highlighted_id=last_id))
            except Exception as Exception_horaire_afficher:
                raise ExceptionHoraireAjouterWTF(f"Erreur dans {Path(__file__).name},"
                                                  f" {horaire_ajouter_wtf.__name__}: "
                                                  f"{Exception_horaire_afficher}")
    return render_template("horaire/horaire_ajouter_wtf.html", form=form)



"""Route update"""

@app.route("/horaire_update", methods=['GET', 'POST'])
def horaire_update_wtf():
    id_horaire_update = request.values['id_horaire_btn_edit_html']
    form_update = FormWTFUpdateHoraire()
    try:
        if request.method == "POST" and form_update.submit.data:
            valeurs_update_dictionnaire = {
                "value_id_horaire": id_horaire_update,
                "value_date_cours": form_update.date_cours_Uwtf.data,
                "value_jour_semaine": form_update.jour_semaine_Uwtf.data,
                "value_heure_debut": form_update.heure_debut_Uwtf.data,
                "value_heure_fin": form_update.heure_fin_Uwtf.data
            }
            str_sql_update_horaire = """UPDATE t_horaire SET date_cours = %(value_date_cours)s, 
                                        jour_semaine = %(value_jour_semaine)s, 
                                        heure_debut = %(value_heure_debut)s, 
                                        heure_fin = %(value_heure_fin)s
                                        WHERE ID_horaire = %(value_id_horaire)s"""
            try:
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_update_horaire, valeurs_update_dictionnaire)
                flash("Données mises à jour avec succès !", "success")
                return redirect(url_for('horaire_afficher', order_by="DESC", id_horaire_sel=id_horaire_update, highlighted_id=id_horaire_update))
            except Exception as update_set:
                raise Exception(f"Erreur dans {Path(__file__).name}, {horaire_update_wtf.__name__}: {update_set}")

        elif request.method == "GET":
            str_sql_id_horaire = """SELECT ID_horaire, date_cours, jour_semaine, heure_debut, heure_fin 
                                    FROM t_horaire WHERE ID_horaire = %(value_id_horaire)s"""
            try:
                with DBconnection() as mybd_conn:
                    mybd_conn.execute(str_sql_id_horaire, {"value_id_horaire": id_horaire_update})
                    data_horaire = mybd_conn.fetchone()
                form_update.date_cours_Uwtf.data = data_horaire["date_cours"]
                form_update.jour_semaine_Uwtf.data = data_horaire["jour_semaine"]
                form_update.heure_debut_Uwtf.data = data_horaire["heure_debut"]
                form_update.heure_fin_Uwtf.data = data_horaire["heure_fin"]
            except Exception as e:
                raise Exception(f"Erreur dans {Path(__file__).name}, {horaire_update_wtf.__name__}: {e}")

    except Exception as Exception_horaire_update:
        raise ExceptionHoraireUpdateWTF(f"Erreur dans {Path(__file__).name}, "
                        f"{horaire_update_wtf.__name__}: "
                        f"{Exception_horaire_update}")

    return render_template("horaire/horaire_update_wtf.html", form_update=form_update)



"""#Route Delete"""

@app.route("/horaire_delete", methods=['GET', 'POST'])
def horaire_delete_wtf():
    data_horaire_delete = None
    associations = None
    btn_submit_del = None
    id_horaire_delete = request.values['id_horaire_btn_delete_html']
    form_delete = FormWTFDeleteHoraire()
    try:
        if request.method == "POST":
            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("horaire_afficher", order_by='ASC', id_horaire_sel=0))

            if form_delete.submit_btn_confirmation.data:
                data_horaire_delete = session['data_horaire_delete']
                print("data_horaire_delete ", data_horaire_delete)
                flash("Effacer l'horaire de façon définitive de la BD !!!", "danger")
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_horaire": id_horaire_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                # Suppression des associations avec les tables intermédiaires
                delete_horaire_cours = """DELETE FROM t_horaire_cours WHERE FK_Horaire = %(value_id_horaire)s"""
                delete_horaire = """DELETE FROM t_horaire WHERE ID_horaire = %(value_id_horaire)s"""

                try:
                    with DBconnection() as mconn_bd:
                        # Suppression des associations liées à l'horaire
                        mconn_bd.execute(delete_horaire_cours, valeur_delete_dictionnaire)
                        # Suppression de l'horaire
                        mconn_bd.execute(delete_horaire, valeur_delete_dictionnaire)

                    flash("Horaire définitivement effacé !", "success")
                    return redirect(url_for('horaire_afficher', order_by="ASC", id_horaire_sel=0))
                except Exception as e:
                    raise ExceptionHoraireDeleteWTF(f"Erreur dans {Path(__file__).name}, {horaire_delete_wtf.__name__}: {e}")

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_horaire": id_horaire_delete}
            print(id_horaire_delete, type(id_horaire_delete))

            # Requête qui affiche l'horaire qui doit être effacé.
            select_horaire_info = """SELECT * FROM t_horaire WHERE ID_horaire = %(value_id_horaire)s"""

            data_associations = """SELECT 
                                     c.Titre,
                                     c.Niveau,
                                     c.Session,
                                     c.Prix_par_session,
                                     c.Description,
                                     c.Affiche
                                   FROM t_horaire h
                                   JOIN t_horaire_cours hc ON hc.FK_Horaire = h.ID_horaire
                                   JOIN t_cours c ON hc.FK_Cours = c.Id_cours
                                   WHERE h.ID_horaire = %(value_id_horaire)s
                                """

            try:
                with DBconnection() as mydb_conn:
                    mydb_conn.execute(select_horaire_info, valeur_select_dictionnaire)
                    data_horaire_delete = mydb_conn.fetchone()
                    print(data_horaire_delete)  # Ajoutez ceci pour déboguer
                    if data_horaire_delete:
                        # car les objets de type timedelta ne peuvent pas être sérialisés directement en JSON.
                        # Nous devons nous assurer que tous les champs de type timedelta (de date et de temps )sont convertis en chaînes de caractères
                        # avant d'être stockés dans la session.
                        if isinstance(data_horaire_delete['date_cours'], date):
                            data_horaire_delete['date_cours'] = data_horaire_delete['date_cours'].strftime("%Y-%m-%d")

                        if isinstance(data_horaire_delete['heure_debut'], time):
                            data_horaire_delete['heure_debut'] = data_horaire_delete['heure_debut'].strftime("%H:%M:%S")
                        if isinstance(data_horaire_delete['heure_fin'], time):
                            data_horaire_delete['heure_fin'] = data_horaire_delete['heure_fin'].strftime("%H:%M:%S")

                        if isinstance(data_horaire_delete['heure_debut'], timedelta):
                            total_seconds = int(data_horaire_delete['heure_debut'].total_seconds())
                            hours, remainder = divmod(total_seconds, 3600)
                            minutes, seconds = divmod(remainder, 60)
                            data_horaire_delete['heure_debut'] = f"{hours:02}:{minutes:02}:{seconds:02}"

                        if isinstance(data_horaire_delete['heure_fin'], timedelta):
                            total_seconds = int(data_horaire_delete['heure_fin'].total_seconds())
                            hours, remainder = divmod(total_seconds, 3600)
                            minutes, seconds = divmod(remainder, 60)
                            data_horaire_delete['heure_fin'] = f"{hours:02}:{minutes:02}:{seconds:02}"

                    session['data_horaire_delete'] = data_horaire_delete

                    mydb_conn.execute(data_associations, valeur_select_dictionnaire)
                    associations = mydb_conn.fetchall()

                btn_submit_del = False

            except Exception as e:
                raise ExceptionHoraireDeleteWTF(f"Erreur dans {Path(__file__).name}, {horaire_delete_wtf.__name__}: {e}")

    except Exception as Exception_horaire_delete:
        raise ExceptionHoraireDeleteWTF(f"Erreur dans {Path(__file__).name}, {horaire_delete_wtf.__name__}: {Exception_horaire_delete}")

    return render_template("horaire/horaire_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_horaire_delete=data_horaire_delete,
                           associations=associations)
