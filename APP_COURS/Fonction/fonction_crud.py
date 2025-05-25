
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_COURS import app
from APP_COURS.Fonction.fonction_wtf_forms import FormWTFAjouterFonction, FormWTFUpdateFonction, FormWTFDeleteFonction
from APP_COURS.database.database_tools import DBconnection
from APP_COURS.erreurs.exceptions import *

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /fonction_afficher
    avec :
    ExceptionFonctionAfficher
    return render_template("fonction/fonction_afficher.html", data=data_fonction)

"""


@app.route("/fonction_afficher/<string:order_by>/<int:id_fonction_sel>", methods=['GET', 'POST'])
def fonction_afficher(order_by, id_fonction_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_fonction_sel == 0:
                    strsql_fonctions_afficher = """SELECT ID_Fonction, Type_fonction FROM t_fonction ORDER BY ID_Fonction ASC"""
                    mc_afficher.execute(strsql_fonctions_afficher)
                elif order_by == "ASC":
                    valeur_id_fonction_selected_dictionnaire = {"value_id_fonction_selected": id_fonction_sel}
                    strsql_fonctions_afficher = """SELECT ID_Fonction, Type_fonction FROM t_fonction WHERE ID_Fonction = %(value_id_fonction_selected)s"""
                    mc_afficher.execute(strsql_fonctions_afficher, valeur_id_fonction_selected_dictionnaire)
                else:
                    strsql_fonctions_afficher = """SELECT ID_Fonction, Type_fonction FROM t_fonction ORDER BY ID_Fonction DESC"""
                    mc_afficher.execute(strsql_fonctions_afficher)

                data_fonction = mc_afficher.fetchall()

                print("data_fonction ", data_fonction, " Type : ", type(data_fonction))

                if not data_fonction and id_fonction_sel == 0:
                    flash("""La table "t_fonction" est vide. !!""", "warning")
                elif not data_fonction and id_fonction_sel > 0:
                    flash(f"La fonction demandée n'existe pas !!", "warning")
                else:
                    flash(f"Données des fonctions affichées !!", "success")

        except Exception as Exception_fonctions_afficher:
            raise ExceptionFonctionAfficherWTF(f"fichier : {Path(__file__).name}  ;  "
                                          f"{fonction_afficher.__name__} ; "
                                          f"{Exception_fonctions_afficher}")
    return render_template("fonction/fonction_afficher.html", data=data_fonction)


"""
    Auteur : OM 2021.03.22
    Définition d'une "route" /fonction_ajouter
    
    Test : ex : http://127.0.0.1:5575/fonction_ajouter
    
    Paramètres : sans
    
    But : Ajouter un fonction pour la personne
"""



@app.route("/fonction_ajouter", methods=['GET', 'POST'])
def fonction_ajouter():
    form = FormWTFAjouterFonction()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                nom_fonction_wtf = form.nom_fonction_wtf.data
                valeurs_insertion_dictionnaire = {"value_nom_fonction": nom_fonction_wtf}
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_fonction = """INSERT INTO t_fonction (ID_Fonction, Type_fonction) VALUES (NULL, %(value_nom_fonction)s) """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute("ALTER TABLE t_fonction AUTO_INCREMENT = 1")
                    mconn_bd.execute(strsql_insert_fonction, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('fonction_afficher', order_by='DESC', id_fonction_sel=0))

        except Exception as Exception_fonctions_ajouter_wtf:
            raise ExceptionFonctionsAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                                f"{fonction_ajouter.__name__} ; "
                                                f"{Exception_fonctions_ajouter_wtf}")

    return render_template("fonction/fonction_ajouter.html", form=form)




"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /fonction_update
    
    faire:
    def fonction_update
    form_update = FormWTFUpdateFonction
    nom_fonction_update_wtf
    
"""


@app.route("/fonction_update", methods=['GET', 'POST'])
def fonction_update():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "ID_Fonction"
    id_fonction_update = request.values['id_fonction_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdateFonction()
    try:

        if request.method == "POST" and form_update.submit.data:
            # Récupèrer la valeur du champ depuis "fonction_update_wtf.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.
            nom_fonction_update = form_update.nom_fonction_update_wtf.data

            valeur_update_dictionnaire = {"value_id_fonction": id_fonction_update,
                                          "value_nom_fonction": nom_fonction_update
                                          }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_typefonction = """UPDATE t_fonction SET Type_fonction = %(value_nom_fonction)s 
            WHERE ID_Fonction = %(value_id_fonction)s """
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_typefonction, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # Afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_fonction_update"
            return redirect(url_for('fonction_afficher', order_by="ASC", id_fonction_sel=id_fonction_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "ID_Fonction" et "Type_fonction" de la "t_fonction"
            str_sql_id_fonction = "SELECT ID_Fonction, Type_fonction FROM t_fonction WHERE ID_Fonction = %(value_id_fonction)s"
            valeur_select_dictionnaire = {"value_id_fonction": id_fonction_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_fonction, valeur_select_dictionnaire)
                # Récupérer les données
                data_fonction = mybd_conn.fetchone()
                print("data_fonction ", data_fonction, " type ", type(data_fonction))

                # Afficher la valeur sélectionnée dans les champs du formulaire "fonction_update_wtf.html"
                form_update.nom_fonction_update_wtf.data = data_fonction["Type_fonction"]

    except Exception as Exception_fonction_update:
        raise ExceptionFonctionUpdateWTF(f"fichier : {Path(__file__).name}  ;  "
                                      f"{fonction_update.__name__} ; "
                                      f"{Exception_fonction_update}")

    return render_template("fonction/fonction_update.html", form_update=form_update)



"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /fonction_ajouter
    
    Test : ex. cliquer sur le menu "fonction" puis cliquer sur le bouton "DELETE" d'un "fonction"
    
    Paramètres : sans
    
    But : Effacer(delete) un fonction qui a été sélectionné dans le formulaire "fonction_afficher.html"
    
    Remarque :  Dans le champ "nom_genre_delete_wtf" du formulaire "genres/genre_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""

@app.route("/fonction_delete", methods=['GET', 'POST'])
def fonction_delete():
    data_fonction_associees = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "ID_Fonction"
    id_fonction_delete = request.values['id_fonction_btn_delete_html']

    # Objet formulaire pour effacer la fonction sélectionnée.
    form_delete = FormWTFDeleteFonction()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("fonction_afficher", order_by="ASC", id_fonction_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "fonctions/fonction_delete_wtf.html" lorsque le bouton "Etes-vous sûr de vouloir effacer ?" est cliqué.
                data_fonction_associees = session['data_fonction_associees']
                print("data_fonction_associees ", data_fonction_associees)

                flash(f"Effacer la fonction de façon définitive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer fonction" qui va irrémédiablement EFFACER la fonction
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_fonction": id_fonction_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_personnes_fonction = """DELETE FROM t_avoirfonction WHERE fk_fonction = %(value_id_fonction)s"""
                str_sql_delete_idfonction = """DELETE FROM t_fonction WHERE ID_Fonction = %(value_id_fonction)s"""

                # Manière brutale d'effacer d'abord les "personnes" associées à la fonction,
                # même si elles n'existent pas dans la table "t_personne"
                # Ensuite, on peut effacer la fonction vu qu'elle n'est plus "liée" (INNODB) dans la table "t_personne"
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_personnes_fonction, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_idfonction, valeur_delete_dictionnaire)

                flash(f"Fonction définitivement effacée !!", "success")
                print(f"Fonction définitivement effacée !!")

                # afficher les données
                return redirect(url_for('fonction_afficher', order_by="ASC", id_fonction_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_fonction": id_fonction_delete}
            print(id_fonction_delete, type(id_fonction_delete))

            # Requête qui affiche toutes les fonctions associées à la fonction que l'utilisateur veut effacer
            str_sql_fonctions_fonction_delete = """SELECT ID_avoirFonction,f.ID_Fonction, f.Type_fonction, 
                                                    p.Id_personne, p.Nom, p.Prenom, p.Date_naissance, p.NumeroAVS
                                                FROM t_avoirfonction AS AF
                                                INNER JOIN t_personne p ON AF.fk_personne = p.Id_personne
                                                INNER JOIN t_fonction AS f ON AF.fk_fonction = f.ID_Fonction
                                                WHERE fk_fonction = %(value_id_fonction)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_fonctions_fonction_delete, valeur_select_dictionnaire)
                data_fonction_associees = mydb_conn.fetchall()
                print("data_fonction_associees...", data_fonction_associees)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "fonctions/fonction_delete_wtf.html" lorsque le bouton "Etes-vous sûr de vouloir effacer ?" est cliqué.
                session['data_fonction_associees'] = data_fonction_associees

                # Opération sur la BD pour récupérer "ID_Fonction" et "Type_fonction" de la "t_fonction"
                str_sql_id_fonction = "SELECT ID_Fonction, Type_fonction FROM t_fonction WHERE ID_Fonction = %(value_id_fonction)s"

                mydb_conn.execute(str_sql_id_fonction, valeur_select_dictionnaire)
                # Une seule valeur est suffisante "fetchone()",
                # vu qu'il n'y a qu'un seul champ "Type_fonction" pour l'action DELETE
                data_type_fonction = mydb_conn.fetchone()
                print("data_type_fonction ", data_type_fonction, " type ", type(data_type_fonction), " fonction ",
                      data_type_fonction["Type_fonction"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "fonction_delete_wtf.html"
            form_delete.nom_fonction_delete_wtf.data = data_type_fonction["Type_fonction"]

            # Le bouton pour l'action "DELETE" dans le form. "fonction_delete_wtf.html" est caché.
            btn_submit_del = False

    except Exception as Exception_fonction_delete_wtf:
        raise ExceptionFonctionDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                         f"{fonction_delete.__name__} ; "
                                         f"{Exception_fonction_delete_wtf}")

    return render_template("fonction/fonction_delete.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_fonction_associees=data_fonction_associees)
