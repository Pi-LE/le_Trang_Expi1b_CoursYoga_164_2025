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
from wtforms.fields.simple import SubmitField

from APP_COURS.database.database_tools import DBconnection
from APP_COURS.erreurs.exceptions import *
from flask_wtf import FlaskForm
from wtforms import DateField
from wtforms.validators import InputRequired, Optional

"""
    Nom : films_genres_afficher
    Auteur : OM 2021.05.01
    Définition d'une "route" /personne_fonction_afficher
    
                 
"""
@app.route("/personnes_fonctions_afficher/<int:id_personne_sel>", methods=['GET', 'POST'])
def personnes_fonctions_afficher(id_personne_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                strsql_personnes_fonctions_afficher_data = """
                        SELECT
                            t_personne.Id_personne,t_personne.Nom,
                            t_personne.Prenom,t_personne.Date_naissance,
                            t_personne.NumeroAVS,t_personne.Sexe,
                            t_avoirfonction.Date_debut,t_avoirfonction.Date_fin,
                            t_fonction.Type_fonction
                        FROM
                            t_personne
                        LEFT JOIN t_avoirfonction ON t_personne.Id_personne = t_avoirfonction.FK_Personne
                        LEFT JOIN t_fonction ON t_fonction.ID_Fonction = t_avoirfonction.FK_Fonction
                        """

                if id_personne_sel != 0:
                    strsql_personnes_fonctions_afficher_data += " WHERE t_personne.Id_personne = %(value_id_personne_selected)s"
                    params = {'value_id_personne_selected': id_personne_sel}
                else:
                    params = {}

                mc_afficher.execute(strsql_personnes_fonctions_afficher_data, params)
                raw_data = mc_afficher.fetchall()

                # Regrouper les fonctions par personne
                data_personnes_fonctions_afficher = {}
                for row in raw_data:
                    if row['Id_personne'] not in data_personnes_fonctions_afficher:
                        data_personnes_fonctions_afficher[row['Id_personne']] = row
                        data_personnes_fonctions_afficher[row['Id_personne']]['fonctions'] = []
                    data_personnes_fonctions_afficher[row['Id_personne']]['fonctions'].append({
                        'Type_fonction': row['Type_fonction'],
                        'Date_debut': row['Date_debut'],
                        'Date_fin': row['Date_fin']
                    })

                # Convertir en liste pour le template
                data_list = list(data_personnes_fonctions_afficher.values())

                flash("Données personnes et fonctions affichées !!", "success")

        except Exception as Exception_personnes_fonctions_afficher:
            raise ExceptionPersonnesFonctionsAfficher(
                f"fichier : {Path(__file__).name}  ;  {personnes_fonctions_afficher.__name__} ;"
                f"{Exception_personnes_fonctions_afficher}")
            data_list = []
    return render_template("personne_fonction/personnes_fonctions_afficher.html", data=data_list)

"""
    nom: edit_personne_fonction_selected
    
"""

@app.route("/edit_personne_fonction_selected", methods=['GET', 'POST'])
def edit_personne_fonction_selected():
    form = UpdateFonctionForm()
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                # Sélectionner toutes les fonctions disponibles
                strsql_fonctions_afficher = """SELECT ID_Fonction, Type_fonction FROM t_fonction ORDER BY ID_Fonction ASC"""
                mc_afficher.execute(strsql_fonctions_afficher)
            data_fonctions_all = mc_afficher.fetchall()
            print("dans edit_personne_fonction_selected ---> data_fonctions_all", data_fonctions_all)

            # Récupère l'ID de la personne sélectionnée
            id_personne_fonctions_edit = request.values['id_personne_fonctions_edit_html']

            # Mémorise l'ID de la personne dans une variable de session
            session['session_id_personne_fonctions_edit'] = id_personne_fonctions_edit

            # Préparation du dictionnaire pour les requêtes
            valeur_id_personne_selected_dictionnaire = {"value_id_personne_selected": id_personne_fonctions_edit}

            # Exécuter les requêtes pour obtenir les fonctions associées et non associées à la personne
            # Exécution des requêtes et récupération des données
            data_personne_selected, data_fonctions_personne_non_attribues, data_fonctions_personne_attribues =\
                personnes_fonctions_afficher_data(valeur_id_personne_selected_dictionnaire)
            print("data_fonction_personne_selected", data_personne_selected)

            #  cette partie remplit le formulaire avec les données récupérées
            if data_personne_selected:
                form.date_debut.data = data_personne_selected[0].get('Date_debut')
                form.date_fin.data = data_personne_selected[0].get('Date_fin')

            # Préparation des listes pour l'interface utilisateur
            lst_data_personne_selected = [item['Id_personne'] for item in data_personne_selected]
            print("lst_data_personne_selected  ", lst_data_personne_selected, type(lst_data_personne_selected))

            # Identification des fonctions non attribuées pour le composant "tags-selector-tagselect"
            lst_data_fonctions_personne_non_attribues = [item['ID_Fonction'] for item in
                                                         data_fonctions_personne_non_attribues]
            session['session_lst_data_fonctions_personne_non_attribues'] = lst_data_fonctions_personne_non_attribues
            print("lst_data_fonctions_personne_non_attribues  ", lst_data_fonctions_personne_non_attribues,
                  type(lst_data_fonctions_personne_non_attribues))

            # Identification des fonctions déjà attribuées pour le composant "tags-selector-tagselect"
            lst_data_fonctions_personne_old_attribues = [item['ID_Fonction'] for item in
                                                         data_fonctions_personne_attribues]
            session['session_lst_data_fonctions_personne_old_attribues'] = lst_data_fonctions_personne_old_attribues
            print("lst_data_fonctions_personne_old_attribues  ", lst_data_fonctions_personne_old_attribues,
                  type(lst_data_fonctions_personne_old_attribues))

            # Affichage détaillé des données pour le débogage
            print("Data data_fonction_personne_selected", data_personne_selected, "type ",
                  type(data_personne_selected))
            print("Data data_fonctions_personne_non_attribues ", data_fonctions_personne_non_attribues, "type ",
                  type(data_fonctions_personne_non_attribues))
            print("Data_fonctions_personne_attribues ", data_fonctions_personne_attribues, "type ",
                  type(data_fonctions_personne_attribues))

            # Extraction des valeurs nécessaires pour le composant Javascript "tagify"
            lst_intitule_fonctions_personne_non_attribues = [item['Type_fonction'] for item in
                                                             data_fonctions_personne_non_attribues]
            print("lst_all_fonctions gf_edit_personne_fonction_selected ",
                  lst_intitule_fonctions_personne_non_attribues,
                  type(lst_intitule_fonctions_personne_non_attribues))



        except Exception as Exception_edit_personne_fonction_selected:
            raise ExceptionEditPersonneFonctionSelected(f"fichier : {Path(__file__).name} ; "
                                                        f"{edit_personne_fonction_selected.__name__} ; "
                                                        f"{Exception_edit_personne_fonction_selected}")

    # Retourner les données à la template pour affichage et modifications
    return render_template("personne_fonction/personnes_fonctions_modifier_tags_dropbox.html",
                           data_fonctions_all=data_fonctions_all,
                           data_personne_selected=data_personne_selected,
                           data_fonctions_attribues=data_fonctions_personne_attribues,
                           data_fonctions_non_attribues=data_fonctions_personne_non_attribues,
                           form = form)





"""
    nom: update_genre_film_selected

    Récupère la liste de tous les genres du film sélectionné par le bouton "MODIFIER" de "films_genres_afficher.html"
    
    Dans une liste déroulante particulière (tags-selector-tagselect), on voit :
    1) Tous les genres contenus dans la "t_genre".
    2) Les genres attribués au film selectionné.
    3) Les genres non-attribués au film sélectionné.

    On signale les erreurs importantes
"""


@app.route("/update_personne_fonction_selected", methods=['GET', 'POST'])
def update_personne_fonction_selected():
    form = UpdateFonctionForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:

            # Récupération des dates depuis le formulaire
            date_debut = form.date_debut.data.strftime('%Y-%m-%d') if form.date_debut.data else None
            date_fin = form.date_fin.data.strftime('%Y-%m-%d') if form.date_fin.data else None

            print("Dates récupérées : ", date_debut, date_fin)

            # Récupère l'id de la personne sélectionnée
            id_personne_selected = session['session_id_personne_fonctions_edit']
            print("session['session_id_personne_fonctions_edit'] ", session['session_id_personne_fonctions_edit'])


            # Récupère la liste des fonctions qui ne sont pas associées à la personne sélectionnée.
            old_lst_data_fonctions_personne_non_attribues = session['session_lst_data_fonctions_personne_non_attribues']
            print("old_lst_data_fonctions_personne_non_attribues ", old_lst_data_fonctions_personne_non_attribues)

            # Récupère la liste des fonctions qui sont associées à la personne sélectionnée.
            old_lst_data_fonctions_personne_attribues = session['session_lst_data_fonctions_personne_old_attribues']
            print("old_lst_data_fonctions_personne_old_attribues ", old_lst_data_fonctions_personne_attribues)

            # Effacer toutes les variables de session.
            session.clear()

            # Récupère ce que l'utilisateur veut modifier comme fonctions dans le composant "tags-selector-tagselect"
            new_lst_str_fonctions_personne = request.form.getlist('name_select_tags')
            print("new_lst_str_fonctions_personne ", new_lst_str_fonctions_personne)

            # Transformation de la liste de string en liste d'int
            new_lst_int_fonction_personne = list(map(int, new_lst_str_fonctions_personne))
            print("new_lst_int_fonction_personne ", new_lst_int_fonction_personne, "type new_lst_int_fonction_personne ",
                  type(new_lst_int_fonction_personne))

            # Calcul des différences pour savoir ce qui doit être ajouté ou supprimé
            lst_diff_fonctions_delete_b = list(set(old_lst_data_fonctions_personne_attribues) -
                                               set(new_lst_int_fonction_personne))
            print("lst_diff_fonctions_delete_b ", lst_diff_fonctions_delete_b)

            lst_diff_fonctions_insert_a = list(set(new_lst_int_fonction_personne) -
                                               set(old_lst_data_fonctions_personne_attribues))
            print("lst_diff_fonctions_insert_a ", lst_diff_fonctions_insert_a)

            # Insertion des nouvelles associations dans la table intermédiaire
            # SQL pour insérer une nouvelle association entre la personne et la fonction dans "t_avoirfonction"
            strsql_insert_fonction_personne = """INSERT INTO t_avoirfonction (FK_Personne, FK_Fonction, Date_debut, Date_fin)
                                     VALUES (%(value_fk_personne)s, %(value_fk_fonction)s, %(value_date_debut)s, %(value_date_fin)s)"""

            # SQL pour supprimer une association existante entre la personne et la fonction dans "t_avoirfonction"
            strsql_delete_fonction_personne = """DELETE FROM t_avoirfonction WHERE FK_Personne = %(value_fk_personne)s 
                                                                                AND FK_Fonction = %(value_fk_fonction)s"""

            # SQL pour mettre à jour une association existante entre la personne et la fonction
            strsql_update_fonction_personne = """
                                        UPDATE t_avoirfonction
                                        SET Date_debut = %(value_date_debut)s, Date_fin = %(value_date_fin)s
                                        WHERE FK_Personne = %(value_fk_personne)s AND FK_Fonction = %(value_fk_fonction)s
                                    """

            with DBconnection() as mconn_bd:

                # Pour chaque fonction déjà attribuée, vérifiez si elle doit être mise à jour
                for id_fonction_attrib in old_lst_data_fonctions_personne_attribues:
                    if id_fonction_attrib in new_lst_int_fonction_personne:
                        # Préparer les données pour la mise à jour
                        valeurs_personne_fonction_dictionnaire = {
                            "value_fk_personne": id_personne_selected,
                            "value_fk_fonction": id_fonction_attrib,
                            "value_date_debut": date_debut,
                            "value_date_fin": date_fin if date_fin else None,
                        }
                        # Exécuter la mise à jour
                        mconn_bd.execute(strsql_update_fonction_personne,
                                         valeurs_personne_fonction_dictionnaire)
                # Pour la personne sélectionnée, parcourir la liste des fonctions à INSÉRER dans "t_avoirfonction"
                for id_fonction_ins in lst_diff_fonctions_insert_a :
                    valeurs_personne_fonction_dictionnaire = {"value_fk_personne": id_personne_selected,
                                                               "value_fk_fonction": id_fonction_ins,
                                                              "value_date_debut": date_debut,
                                                              "value_date_fin": date_fin }

                    mconn_bd.execute(strsql_insert_fonction_personne, valeurs_personne_fonction_dictionnaire)

                # Pour la personne sélectionnée, parcourir la liste des fonctions à SUPPRIMER de "t_avoirfonction"
                for id_fonction_del in lst_diff_fonctions_delete_b:
                    valeurs_personne_fonction_dictionnaire = {"value_fk_personne": id_personne_selected,
                                                               "value_fk_fonction": id_fonction_del}

                    mconn_bd.execute(strsql_delete_fonction_personne, valeurs_personne_fonction_dictionnaire)

                    # Rediriger vers la page d'affichage des personnes et de leurs fonctions associées

        except Exception as Exception_update_personne_fonction_selected:
            raise ExceptionUpdatePersonneFonctionSelected(f"fichier : {Path(__file__).name}  ;  "
                                                          f"{update_personne_fonction_selected.__name__} ; "
                                                          f"{Exception_update_personne_fonction_selected}")

    return redirect(url_for('personnes_fonctions_afficher', id_personne_sel=id_personne_selected, form = form))








"""

    nom: personne_fonction_afficher_data

    Récupère la liste de tous les fonctions de la personne sélectionné par le bouton "MODIFIER" de "personne_fonction_afficher.html"

"""


def personnes_fonctions_afficher_data(valeur_id_personne_selected_dict):
    print("valeur_id_personne_selected_dict...", valeur_id_personne_selected_dict)
    try:
        # Requête pour obtenir la personne sélectionnée et ses fonctions associées
        strsql_personne_selected = """
                                    SELECT
                                        t_personne.Id_personne,
                                        t_personne.Nom,
                                        t_personne.Prenom,
                                        t_personne.Date_naissance,
                                        t_personne.NumeroAVS,
                                        t_personne.Sexe,
                                        t_avoirfonction.Date_debut,
                                        t_avoirfonction.Date_fin,
                                        t_fonction.Type_fonction
                                    FROM
                                        t_personne
                                    INNER JOIN t_avoirfonction ON t_personne.Id_personne = t_avoirfonction.FK_Personne
                                    INNER JOIN t_fonction ON t_fonction.ID_Fonction = t_avoirfonction.FK_Fonction
                                    WHERE
                                        t_personne.Id_personne = %(value_id_personne_selected)s
                                    """

        # Requête pour obtenir les fonctions non attribuées à la personne
        strsql_fonctions_personne_non_attribues = """SELECT ID_Fonction, Type_fonction FROM t_fonction 
                                                     WHERE ID_Fonction NOT IN (SELECT ID_Fonction FROM t_avoirfonction
                                                        INNER JOIN t_personne ON t_personne.Id_personne = t_avoirfonction.FK_Personne
                                                        INNER JOIN t_fonction ON t_fonction.ID_Fonction = t_avoirfonction.FK_Fonction
                                                         WHERE FK_Personne = %(value_id_personne_selected)s)"""

        # Requête pour obtenir les fonctions déjà attribuées à la personne
        strsql_fonctions_personne_attribues = """
                                            SELECT
                                                t_avoirfonction.FK_Personne AS Id_personne,
                                                t_avoirfonction.FK_Fonction AS ID_Fonction,
                                                t_fonction.Type_fonction,
                                                t_avoirfonction.Date_debut,
                                                t_avoirfonction.Date_fin
                                            FROM
                                                t_avoirfonction
                                            INNER JOIN t_personne ON t_personne.Id_personne = t_avoirfonction.FK_Personne
                                            INNER JOIN t_fonction ON t_fonction.ID_Fonction = t_avoirfonction.FK_Fonction
                                            WHERE
                                                t_avoirfonction.FK_Personne = %(value_id_personne_selected)s
                                            """

        # Exécution des requêtes
        with DBconnection() as mc_afficher:
            # Récupère les fonctions non attribuées
            mc_afficher.execute(strsql_fonctions_personne_non_attribues, valeur_id_personne_selected_dict)
            data_fonctions_personne_non_attribues = mc_afficher.fetchall()
            print("Fonctions non attribuées à la personne :", data_fonctions_personne_non_attribues)

            # Récupère la personne sélectionnée et ses fonctions associées
            mc_afficher.execute(strsql_personne_selected, valeur_id_personne_selected_dict)
            data_personne_selected = mc_afficher.fetchall()

            # Récupère les fonctions attribuées à la personne
            mc_afficher.execute(strsql_fonctions_personne_attribues, valeur_id_personne_selected_dict)
            data_fonctions_personne_attribues = mc_afficher.fetchall()

            # Retourne les données des requêtes
            return data_personne_selected, data_fonctions_personne_non_attribues, data_fonctions_personne_attribues

    except Exception as Exception_personnes_fonctions_afficher_data:
        raise ExceptionPersonnesFonctionsAfficherData(f"Erreur dans {Path(__file__).name} ; "
                                                      f"{personnes_fonctions_afficher_data.__name__} ; {Exception_personnes_fonctions_afficher_data}")


class UpdateFonctionForm(FlaskForm):
    # Ajoutez ici des champs dynamiques ou des champs statiques, selon votre besoin
    date_debut = DateField("Date de début", validators=[InputRequired("Date de début obligatoire")])
    date_fin = DateField("Date de fin", validators=[Optional()])
    submit = SubmitField("EditDate")
