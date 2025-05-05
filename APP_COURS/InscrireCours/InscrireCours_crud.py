"""
    Fichier : gestion_films_genres_crud.py
    Auteur : OM 2021.05.01
    Gestions des "routes" FLASK et des données pour l'association entre les films et les genres.
"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_COURS.database.database_tools import DBconnection
from APP_COURS.erreurs.exceptions import *



"""Afficher table inscrire cours . inclue personne et table cours"""


@app.route("/inscriptions_afficher/<int:id_personne_sel>", methods=['GET'])
def inscriptions_afficher(id_personne_sel):
    print("inscriptions_afficher id_personne_sel ", id_personne_sel)
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                sql_afficher_data = """
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
                """
                if id_personne_sel == 0:
                    mc_afficher.execute(sql_afficher_data)
                else:
                    # Constitution d'un dictionnaire pour associer l'id de la personne sélectionnée avec un nom de variable
                    valeur_id_personne_selected_dictionnaire = {"value_id_personne_selected": id_personne_sel}
                    sql_afficher_data += " HAVING p.Id_personne = %(value_id_personne_selected)s"
                    mc_afficher.execute(sql_afficher_data, valeur_id_personne_selected_dictionnaire)

                # Récupère les données de la requête
                data_inscriptions = mc_afficher.fetchall()
                print("data_inscriptions ", data_inscriptions, " Type : ", type(data_inscriptions))

                # Différencier les messages
                if not data_inscriptions and id_personne_sel == 0:
                    flash("Aucune inscription trouvée dans la base de données.", "warning")
                elif not data_inscriptions and id_personne_sel > 0:
                    flash(f"Aucune inscription trouvée pour la personne avec l'ID {id_personne_sel}.", "warning")
                else:
                    flash("Données des inscriptions affichées avec succès.", "success")

        except Exception as Exception_inscription_afficher:
            raise ExceptionInscriptionAfficher(f"fichier : {Path(__file__).name} ; "
                                               f"{inscriptions_afficher.__name__} ; "
                                               f"{Exception_inscription_afficher}")

    return render_template("inscrirecours/inscrirecours_afficher.html",
                           data_inscriptions=data_inscriptions)




"""Affichier des datas"""

def inscriptions_cours_afficher_data(valeur_id_personne_selected_dict):
    print("valeur_id_personne_selected_dict...", valeur_id_personne_selected_dict)
    try:
        # Sélectionner les détails de la personne ainsi que tous les cours auxquels elle est inscrite
        strsql_personne_selected = """
            SELECT Id_personne, Nom, Prenom, Date_naissance, Sexe,
                   GROUP_CONCAT(Id_cours) AS CoursInscrits
            FROM t_inscrirecours
            INNER JOIN t_personne ON t_personne.Id_personne = t_inscrirecours.FK_Personne
            INNER JOIN t_cours ON t_cours.Id_cours = t_inscrirecours.FK_Cours
            WHERE Id_personne = %(value_id_personne_selected)s
            GROUP BY Id_personne 
        """

        strsql_cours_non_attribues = """
            SELECT Id_cours, Titre FROM t_cours
            WHERE Id_cours NOT IN (
                SELECT ic.FK_Cours as idCoursInscrits FROM t_inscrirecours ic
                INNER JOIN t_cours c ON c.Id_cours = ic.FK_Cours
                INNER JOIN t_personne p ON p.Id_personne = ic.FK_Personne
                WHERE p.Id_personne = %(value_id_personne_selected)s )
        """

        strsql_cours_attribues = """
            SELECT ic.FK_Personne, c.Id_cours, c.Titre FROM t_inscrirecours ic
            INNER JOIN t_cours c ON c.Id_cours = ic.FK_Cours
            INNER JOIN t_personne p ON p.Id_personne = ic.FK_Personne
            WHERE p.Id_personne = %(value_id_personne_selected)s
        """

        with DBconnection() as mc_afficher:
            # Envoi de la commande MySQL pour les cours non attribués à la personne sélectionnée
            mc_afficher.execute(strsql_cours_non_attribues, valeur_id_personne_selected_dict)
            # Récupère les données de la requête.
            data_cours_non_attribues = mc_afficher.fetchall()
            print("inscriptions_cours_afficher_data ----> data_cours_non_attribues ", data_cours_non_attribues,
                  " Type : ", type(data_cours_non_attribues))

            # Envoi de la commande MySQL pour obtenir les détails de la personne sélectionnée et ses cours inscrits
            mc_afficher.execute(strsql_personne_selected, valeur_id_personne_selected_dict)
            # Récupère les données de la requête.
            data_personne_selected = mc_afficher.fetchall()
            print("data_personne_selected  ", data_personne_selected, " Type : ", type(data_personne_selected))

            # Envoi de la commande MySQL pour obtenir les cours attribués à la personne
            mc_afficher.execute(strsql_cours_attribues, valeur_id_personne_selected_dict)
            # Récupère les données de la requête.
            data_cours_attribues = mc_afficher.fetchall()
            print("data_cours_attribues ", data_cours_attribues, " Type : ", type(data_cours_attribues))

            # Retourne les données des "SELECT"
            return data_personne_selected, data_cours_non_attribues, data_cours_attribues
    except Exception as Exception_Inscription_afficher_data:
        raise ExceptionInscriptionAfficherData(f"fichier : {Path(__file__).name}  ;  "
                                               f"{inscriptions_cours_afficher_data.__name__} ; "
                                               f"{Exception_Inscription_afficher_data}")



"""Route Edit part1"""

@app.route("/edit_inscription_selected", methods=['GET', 'POST'])
def edit_inscription_selected():
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                # Récupérer tous les cours disponibles pour les lister dans un formulaire de sélection
                strsql_cours_afficher = """SELECT Id_cours, Titre FROM t_cours ORDER BY Id_cours ASC"""
                mc_afficher.execute(strsql_cours_afficher)
                data_cours_all = mc_afficher.fetchall()
                print("dans edit_inscription_selected ---> data_cours_all", data_cours_all)

                id_personne_edit = request.values['id_personne_edit_html']

                session['session_id_personne_edit'] = id_personne_edit

                # Dictionnaire pour passer l'ID de la personne à la fonction de récupération des données
                valeur_id_personne_selected_dict = {"value_id_personne_selected": id_personne_edit}

                # Récupération des données pour la personne sélectionnée et les cours inscrits/non-inscrits
                data_personne_selected, data_cours_non_attribues, data_cours_attribues = \
                    inscriptions_cours_afficher_data(valeur_id_personne_selected_dict)

                print("data_personne_selected", data_personne_selected)

                # Préparation des listes pour l'interface utilisateur
                lst_data_personne_selected = [item['Id_personne'] for item in data_personne_selected]
                print("lst_data_personne_selected  ", lst_data_personne_selected, type(lst_data_personne_selected))

                # Dans le composant "tags-selector-tagselect" on doit connaître les cours qui ne sont pas encore sélectionnés.
                lst_data_cours_non_attribues = [item['Id_cours'] for item in data_cours_non_attribues]
                session['session_lst_data_cours_non_attribues'] = lst_data_cours_non_attribues
                print("lst_data_cours_non_attribues  ", lst_data_cours_non_attribues,
                      type(lst_data_cours_non_attribues))

                # Dans le composant "tags-selector-tagselect" on doit connaître les cours qui sont déjà sélectionnés.
                lst_data_cours_attribues = [item['Id_cours'] for item in data_cours_attribues]
                session['session_lst_data_cours_attribues'] = lst_data_cours_attribues
                print("lst_data_cours_attribues  ", lst_data_cours_attribues,
                      type(lst_data_cours_attribues))

            return render_template("inscrirecours/inscrirecours_update.html",
                                   data_cours_all=data_cours_all,
                                   data_personne=data_personne_selected,
                                   data_cours_non_attribues=data_cours_non_attribues,
                                   data_cours_attribues=data_cours_attribues)

        except Exception as Exception_edit_inscription_selected:
            raise ExceptionEditInscriptionSelected(f"fichier : {Path(__file__).name}  ;  "
                                                   f"{edit_inscription_selected.__name__} ; "
                                                   f"{Exception_edit_inscription_selected}")

"""Edit2"""

@app.route("/update_inscription_selected", methods=['GET', 'POST'])
def update_inscription_selected():
    if request.method == "POST":
        try:
            # Récupère l'ID de la personne sélectionnée
            id_personne_selected = session['session_id_personne_edit']
            print("session['session_id_personne_edit'] ", id_personne_selected)

            # Récupère la liste des ID de cours initialement non inscrits récupérés de la session
            old_lst_data_cours_non_inscrits = session['session_lst_data_cours_non_attribues']
            print("old_lst_data_cours_non_inscrits ", old_lst_data_cours_non_inscrits)

            # Récupère la liste des ID de cours initialement inscrits récupérés de la session
            old_lst_data_cours_inscrits = session['session_lst_data_cours_attribues']
            print("old_lst_data_cours_inscrits ", old_lst_data_cours_inscrits)

            # Efface toutes les variables de session pour éviter des fuites de mémoire
            session.clear()

            # Récupère la liste des cours modifiés par l'utilisateur dans le formulaire
            new_lst_str_cours_inscrits = request.form.getlist('name_select_tags')
            print("new_lst_str_cours_inscrits ", new_lst_str_cours_inscrits)

            # Convertit la liste des ID de cours de string à int
            new_lst_int_cours_inscrits = list(map(int, new_lst_str_cours_inscrits))
            print("new_lst_int_cours_inscrits ", new_lst_int_cours_inscrits, "type new_lst_int_cours_inscrits ",
                  type(new_lst_int_cours_inscrits))

            # Listes des ID de cours à ajouter et à supprimer
            lst_cours_to_add = list(set(new_lst_int_cours_inscrits) - set(old_lst_data_cours_inscrits))
            print("lst_cours_to_add ", lst_cours_to_add)
            lst_cours_to_remove = list(set(old_lst_data_cours_inscrits) - set(new_lst_int_cours_inscrits))
            print("lst_cours_to_remove ", lst_cours_to_remove)

            with DBconnection() as mconn_bd:
                # Insère les nouvelles inscriptions
                if lst_cours_to_add:
                    for id_cours_add in lst_cours_to_add:
                        mconn_bd.execute(
                            "INSERT INTO t_inscrirecours (FK_Personne, FK_Cours) VALUES (%s, %s)",
                            (id_personne_selected, id_cours_add)
                        )

                # Supprime les inscriptions non désirées
                if lst_cours_to_remove:
                    for id_cours_remove in lst_cours_to_remove:
                        mconn_bd.execute(
                            "DELETE FROM t_inscrirecours WHERE FK_Personne = %s AND FK_Cours = %s",
                            (id_personne_selected, id_cours_remove)
                        )

        except Exception as Exception_update_inscription_selected:
            raise ExceptionUpdateInscriptionSelected(f"fichier : {Path(__file__).name} ; {update_inscription_selected.__name__} ; {Exception_update_inscription_selected}")

        return redirect(url_for('inscriptions_afficher', id_personne_sel=id_personne_selected))

