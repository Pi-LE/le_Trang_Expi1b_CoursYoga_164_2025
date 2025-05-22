from pathlib import Path

from flask import redirect, request, session, url_for, flash, render_template

from APP_COURS import app
from APP_COURS.database.database_tools import DBconnection
from APP_COURS.erreurs.exceptions import *
from APP_COURS.personnes.personnes_wtf_forms import (
    FormWTFAjouterPersonne,
    FormWTFUpdatePersonne,
    FormWTFDeletePersonne,
)

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /personnes_afficher

    Test : ex : http://127.0.0.1:5575/personnes_afficher

    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_personne_sel = 0 >> toutes les personnes.
                id_personne_sel = "n" affiche la personne dont l'id est "n"
"""
@app.route("/personnes_afficher/<string:order_by>/<int:id_personne_sel>", methods=["GET", "POST"])
def personnes_afficher(order_by, id_personne_sel):
    highlighted_id = request.args.get('highlighted_id', None)
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_personne_sel == 0:
                    strsql_personnes_afficher = (
                        """SELECT Id_personne, Nom, Prenom, Date_naissance, NumeroAVS, Sexe, date_enregistre
                            FROM t_personne ORDER BY Id_personne ASC"""
                    )
                    mc_afficher.execute(strsql_personnes_afficher)
                elif order_by == "ASC":
                    valeur = {"value_id_personne_selected": id_personne_sel}
                    strsql_personnes_afficher = (
                        """SELECT Id_personne, Nom, Prenom, Date_naissance, NumeroAVS, Sexe, date_enregistre
                            FROM t_personne WHERE Id_personne = %(value_id_personne_selected)s
                            ORDER BY Id_personne DESC"""
                    )
                    mc_afficher.execute(strsql_personnes_afficher, valeur)
                else:
                    strsql_personnes_afficher = (
                        """SELECT Id_personne, Nom, Prenom, Date_naissance, NumeroAVS, Sexe, date_enregistre
                            FROM t_personne ORDER BY Id_personne DESC"""
                    )
                    mc_afficher.execute(strsql_personnes_afficher)

                data_personnes = mc_afficher.fetchall()

                if not data_personnes and id_personne_sel == 0:
                    flash("La table \"t_personne\" est vide. !!", "warning")
                elif not data_personnes and id_personne_sel > 0:
                    flash("La personne demandée n'existe pas !!", "warning")
                else:
                    flash("Données personnes affichées !!", "success")

        except Exception as e:
            raise ExceptionPersonnesAfficher(
                f"fichier : {Path(__file__).name}  ;  {personnes_afficher.__name__} ; {e}"
            )

    return render_template(
        "personnes/personnes_afficher.html",
        data=data_personnes,
        highlighted_id=highlighted_id,
    )

"""Route Ajouter"""
@app.route("/personnes_ajouter", methods=["GET", "POST"])
def personnes_ajouter_wtf():
    form = FormWTFAjouterPersonne()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                valeurs = {
                    "value_nom_personne": form.nom_personne_wtf.data,
                    "value_prenom_personne": form.prenom_personne_wtf.data,
                    "value_date_naissance": form.date_naissance_personne_wtf.data,
                    "value_numero_avs": form.numero_avs_personne_wtf.data,
                    "value_sexe": form.sexe_personne_wtf.data,
                }
                strsql_insert = (
                    """INSERT INTO t_personne (Nom, Prenom, Date_naissance, NumeroAVS, Sexe)
                        VALUES (%(value_nom_personne)s, %(value_prenom_personne)s,
                                %(value_date_naissance)s, %(value_numero_avs)s, %(value_sexe)s)"""
                )
                with DBconnection() as mconn_bd:
                    mconn_bd.execute("ALTER TABLE t_personne AUTO_INCREMENT = 1")
                    mconn_bd.execute(strsql_insert, valeurs)
                    flash("Données insérées avec succès !!", "success")
                    mconn_bd.execute("SELECT LAST_INSERT_ID() as last_id")
                    last_id = mconn_bd.fetchone()['last_id']
                return redirect(
                    url_for(
                        'personnes_afficher',
                        order_by='DESC',
                        id_personne_sel=0,
                        highlighted_id=last_id,
                    )
                )
        except Exception as e:
            raise ExceptionPersonnesAjouterWtf(
                f"fichier : {Path(__file__).name}  ;  {personnes_ajouter_wtf.__name__} ; {e}"
            )
    return render_template("personnes/personnes_ajouter_wtf.html", form=form)

"""
    Route Update
"""
@app.route("/personne_update", methods=["GET", "POST"])
def personne_update_wtf():
    id_personne_update = request.values['id_personne_btn_edit_html']
    form_update = FormWTFUpdatePersonne()
    try:
        if request.method == "POST" and form_update.submit.data:
            valeurs_update = {
                "value_id_personne": id_personne_update,
                "value_nom_personne": form_update.nom_personne_update_wtf.data.lower(),
                "value_prenom_personne": form_update.prenom_personne_update_wtf.data.lower(),
                "value_date_naissance_personne_essai": form_update.date_naissance_personne_wtf_essai.data,
                "value_numero_avs_personne": form_update.numero_avs_personne_wtf.data,
                "value_sexe_personne": form_update.sexe_personne_wtf.data,
            }
            str_sql_update = (
                """UPDATE t_personne SET Nom = %(value_nom_personne)s,
                    Prenom = %(value_prenom_personne)s, Date_naissance = %(value_date_naissance_personne_essai)s,
                    NumeroAVS = %(value_numero_avs_personne)s, Sexe = %(value_sexe_personne)s
                    WHERE Id_personne = %(value_id_personne)s"""
            )
            with DBconnection() as mconn_bd:
                mconn_bd.execute("ALTER TABLE t_personne AUTO_INCREMENT = 1")
                mconn_bd.execute(str_sql_update, valeurs_update)
            flash("Donnée mise à jour !!", "success")
            return redirect(
                url_for(
                    'personnes_afficher',
                    order_by="DESC",
                    id_personne_sel=id_personne_update,
                    highlighted_id=id_personne_update,
                )
            )
        elif request.method == "GET":
            select_dct = {"value_id_personne": id_personne_update}
            str_sql = (
                """SELECT Id_personne, Nom, Prenom, Date_naissance, NumeroAVS, Sexe
                    FROM t_personne WHERE Id_personne = %(value_id_personne)s"""
            )
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql, select_dct)
                data = mybd_conn.fetchone()
            form_update.nom_personne_update_wtf.data = data["Nom"]
            form_update.prenom_personne_update_wtf.data = data["Prenom"]
            form_update.date_naissance_personne_wtf_essai.data = data["Date_naissance"]
            form_update.numero_avs_personne_wtf.data = data["NumeroAVS"]
            form_update.sexe_personne_wtf.data = data["Sexe"]
    except Exception as e:
        raise ExceptionPersonneUpdateWtf(
            f"fichier : {Path(__file__).name}  ;  {personne_update_wtf.__name__} ; {e}"
        )
    return render_template("personnes/personne_update_wtf.html", form_update=form_update)

"""Route Delete"""
@app.route("/personne_delete", methods=["GET", "POST"])
def personne_delete_wtf():
    data_personne_delete = None
    associations = None
    btn_submit_del = None
    id_personne_delete = request.values['id_personne_btn_delete_html']
    form_delete = FormWTFDeletePersonne()
    try:
        if request.method == "POST":
            if form_delete.submit_btn_annuler.data:
                return redirect(url_for('personnes_afficher', order_by='ASC', id_personne_sel=0))
            if form_delete.submit_btn_conf_del.data:
                data_personne_delete = session['data_personne_delete']
                flash("Effacer la personne de façon définitive de la BD !!!", "danger")
                btn_submit_del = True
            if form_delete.submit_btn_del.data:
                dct = {"value_id_personne": id_personne_delete}
                deletes = [
                    ("DELETE FROM t_avoirfonction WHERE FK_Personne = %(value_id_personne)s"),
                    ("DELETE FROM t_inscrirecours WHERE FK_Personne = %(value_id_personne)s"),
                    ("DELETE FROM t_enseignercours WHERE FK_Personne = %(value_id_personne)s"),
                    ("DELETE FROM t_payement WHERE FK_Inscrirecours IN (SELECT ID_InscrireCours FROM t_inscrirecours WHERE FK_Personne = %(value_id_personne)s)"),
                    ("DELETE FROM t_annulation WHERE FK_Inscrirecours IN (SELECT ID_InscrireCours FROM t_inscrirecours WHERE FK_Personne = %(value_id_personne)s)"),
                    ("DELETE FROM t_personne WHERE Id_personne = %(value_id_personne)s"),
                ]
                with DBconnection() as mconn_bd:
                    for stmt in deletes:
                        mconn_bd.execute(stmt, dct)
                flash("Personne définitivement effacée !!", "success")
                return redirect(url_for('personnes_afficher', order_by="ASC", id_personne_sel=0))
        if request.method == "GET":
            dct = {"value_id_personne": id_personne_delete}
            select_personne = "SELECT * FROM t_personne WHERE Id_personne = %(value_id_personne)s"
            select_associations = (
                """
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
                WHERE t_personne.Id_personne = %(value_id_personne)s
                """
            )
            with DBconnection() as mydb_conn:
                mydb_conn.execute(select_personne, dct)
                data_personne_delete = mydb_conn.fetchall()
                session['data_personne_delete'] = data_personne_delete
                mydb_conn.execute(select_associations, dct)
                associations = mydb_conn.fetchall()
            btn_submit_del = False
    except Exception as e:
        raise ExceptionPersonneDeleteWtf(
            f"fichier : {Path(__file__).name}  ;  {personne_delete_wtf.__name__} ; {e}"
        )
    return render_template(
        "personnes/personne_delete_wtf.html",
        form_delete=form_delete,
        btn_submit_del=btn_submit_del,
        data_personne_del=data_personne_delete,
        associations=associations,
    )
