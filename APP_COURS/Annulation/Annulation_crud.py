"""

    Gestions des "routes" FLASK et des données pour l'annulationle cours
    OM

"""


from pathlib import Path

from flask import redirect, jsonify
from flask import request
from flask import session
from flask import url_for
from decimal import Decimal

from APP_COURS.database.database_tools import DBconnection
from APP_COURS.erreurs.exceptions import *
from APP_COURS.Annulation.Annulation_wtf import AnnulationAjouterWTF,AnnulationUpdateWTF,AnnulationDeleteWTF


""" ROUTE Afficher table Annulation inclue personne avec cours
"""

@app.route("/annulation_afficher/<string:order_by>/<int:id_personne_sel>", methods=['GET', 'POST'])
def annulation_afficher(order_by, id_personne_sel):
    #ID hight light pour brillant l'élément lorsqu'on ajouter ou modifier
    highlighted_id = request.args.get('highlighted_id', None)
    try:
        with DBconnection() as mc_afficher:
            if order_by == "ASC" and id_personne_sel == 0:
                strsql_afficher = """SELECT a.ID_AnnulerCours, a.Raison,
                                      p.Nom, p.Prenom, p.NumeroAVS, 
                                      c.Titre, pm.Montant_paye
                                      FROM t_annulation a
                                      JOIN t_inscrirecours ic ON a.FK_Inscrirecours = ic.ID_InscrireCours
                                      JOIN t_cours c ON ic.FK_Cours = c.Id_cours
                                      JOIN t_personne p ON ic.FK_Personne = p.Id_personne
                                      LEFT JOIN t_payement pm ON ic.ID_InscrireCours = pm.FK_Inscrirecours
                                      ORDER BY a.ID_AnnulerCours """
                mc_afficher.execute(strsql_afficher)
            elif order_by == "ASC":
                valeur_Id_personne_selected_dictionnaire = {"value_Id_personne_selected": id_personne_sel}
                strsql_afficher = """SELECT a.ID_AnnulerCours, a.Raison,
                                      p.Nom, p.Prenom, p.NumeroAVS, 
                                      c.Titre, pm.Montant_paye
                                      FROM t_annulation a
                                      JOIN t_inscrirecours ic ON a.FK_Inscrirecours = ic.ID_InscrireCours
                                      JOIN t_cours c ON ic.FK_Cours = c.Id_cours
                                      JOIN t_personne p ON ic.FK_Personne = p.Id_personne
                                      LEFT JOIN t_payement pm ON ic.ID_InscrireCours = pm.FK_Inscrirecours
                                      WHERE p.Id_personne = %(value_Id_personne_selected)s
                                      ORDER BY a.ID_AnnulerCours"""
                mc_afficher.execute(strsql_afficher, valeur_Id_personne_selected_dictionnaire)
            else:
                strsql_afficher = """SELECT a.ID_AnnulerCours, a.Raison,
                                      p.Nom, p.Prenom, p.NumeroAVS, 
                                      c.Titre, pm.Montant_paye
                                      FROM t_annulation a
                                      JOIN t_inscrirecours ic ON a.FK_Inscrirecours = ic.ID_InscrireCours
                                      JOIN t_cours c ON ic.FK_Cours = c.Id_cours
                                      JOIN t_personne p ON ic.FK_Personne = p.Id_personne
                                      LEFT JOIN t_payement pm ON ic.ID_InscrireCours = pm.FK_Inscrirecours
                                      ORDER BY a.ID_AnnulerCours DESC"""
                mc_afficher.execute(strsql_afficher)

            data_inscriptions = mc_afficher.fetchall()
            print("Données récupérées:", data_inscriptions)

            if not data_inscriptions and id_personne_sel == 0:
                flash("La table 't_annulation' est vide. !!", "warning")
            elif not data_inscriptions and id_personne_sel > 0:
                flash("t_annulation demandée n'existe pas !!", "warning")
            else:
                flash("Données des annulations affichées !!", "success")

    except Exception as Exception_annulation_afficher:
        raise ExceptionAnnulationAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{annulation_afficher.__name__} ; "
                                          f"{Exception_annulation_afficher}")

    return render_template("Annulation/annulation_afficher.html", data=data_inscriptions, highlighted_id=highlighted_id)




""" Route charger et update les cours lié à la personne"""
"""1. charger cours route"""
@app.route('/charger_cours_annulation')
def charger_cours_annulation():
    personne_id = request.args.get('personne_id')
    with DBconnection() as db:
        db.execute("""
            SELECT ic.ID_InscrireCours, 
                   c.Titre
            FROM t_inscrirecours ic
            JOIN t_cours c ON ic.FK_Cours = c.Id_cours
            WHERE ic.FK_Personne = %s AND NOT EXISTS (
                SELECT 1 FROM t_annulation a WHERE a.FK_Inscrirecours = ic.ID_InscrireCours)
        """, (personne_id,))
        cours = db.fetchall()
        return jsonify([{'id': c['ID_InscrireCours'], 'titre': c['Titre']} for c in cours])


"""2.lorsque l'user choix la personne, il va afficher le cours lié"""
def update_form_choices_annulation(form):
    """Mettre à jour les choix des champs SelectField pour l'annulation de cours à partir de la base de données."""
    with DBconnection() as db:
        db.execute("""
            SELECT DISTINCT p.Id_personne, CONCAT(p.Nom, ' ', p.Prenom, ' [AVS:', p.NumeroAVS, ']') AS Identite
            FROM t_personne p
            JOIN t_inscrirecours ic ON p.Id_personne = ic.FK_Personne
            JOIN t_cours c ON ic.FK_Cours = c.Id_cours
            WHERE NOT EXISTS (
                SELECT 1 FROM t_annulation a WHERE a.FK_Inscrirecours = ic.ID_InscrireCours)
        """)
        personnes = db.fetchall()
        form.personne_wtf.choices = [(p['Id_personne'], p['Identite']) for p in personnes] if personnes else [(-1, 'Aucune personne disponible')]

        selected_person_id = request.form.get('personne_wtf', type=int)
        if selected_person_id:
            db.execute("""
                SELECT ic.ID_InscrireCours, c.Titre 
                FROM t_inscrirecours ic
                JOIN t_cours c ON ic.FK_Cours = c.Id_cours
                WHERE ic.FK_Personne = %s AND NOT EXISTS (
                    SELECT 1 FROM t_annulation a WHERE a.FK_Inscrirecours = ic.ID_InscrireCours)
            """, (selected_person_id,))
            cours = db.fetchall()
            form.fk_inscrirecours.choices = [(c['ID_InscrireCours'], c['Titre']) for c in cours] if cours else [(-1, 'Aucun cours disponible')]


""" Route Ajouter """


@app.route('/annulation_ajouter', methods=['GET', 'POST'])
def annulation_ajouter():
    form = AnnulationAjouterWTF()
    if request.method == 'GET':
        update_form_choices_annulation(form)
    elif request.method == 'POST':
        update_form_choices_annulation(form)
        if form.validate_on_submit():
            fk_inscrirecours = form.fk_inscrirecours.data
            raison = form.raison_wtf.data

            try:
                with DBconnection() as db:
                    db.execute("""
                        INSERT INTO t_annulation (FK_Inscrirecours, Raison)
                        VALUES (%s, %s)
                    """, (fk_inscrirecours, raison))
                    db.execute("ALTER TABLE t_annulation AUTO_INCREMENT = 1")
                    flash('Annulation ajoutée avec succès!', 'success')

                    # Récupérer l'ID de l'annulation ajoutée pour la mettre en surbrillance
                    db.execute("SELECT LAST_INSERT_ID() as last_id")
                    last_id = db.fetchone()['last_id']

                    return redirect(
                        url_for('annulation_afficher', order_by="DESC", id_personne_sel=0, highlighted_id=last_id))
            except Exception as Exception_annulation_ajouter:
                raise ExceptionAnnulationAjouter(f"fichier : {Path(__file__).name}  ;  "
                                                 f"{annulation_ajouter.__name__} ; "
                                                 f"{Exception_annulation_ajouter}")

    return render_template('Annulation/annulation_ajouter_wtf.html', form=form)


"""3. route Update"""

@app.route("/annulation_update", methods=['GET', 'POST'])
def annulation_update():
    id_annulation_update = request.values['id_annulation_btn_edit_html']
    form_update = AnnulationUpdateWTF()
    try:
        if request.method == "POST":
            update_form_choices_annulation(form_update)
            if form_update.validate_on_submit():
                fk_inscrirecours = form_update.fk_inscrirecours_hidden.data
                raison = form_update.raison_updatewtf.data

                with DBconnection() as db:
                    db.execute("""
                        UPDATE t_annulation SET 
                            FK_Inscrirecours = %(fk_inscrirecours)s,
                            Raison = %(raison)s
                        WHERE ID_AnnulerCours = %(id_annulation)s
                    """, {
                        'fk_inscrirecours': fk_inscrirecours,
                        'raison': raison,
                        'id_annulation': id_annulation_update
                    })

                return redirect(url_for('annulation_afficher', order_by="DESC", id_personne_sel=0, highlighted_id=id_annulation_update))
            else:
                print("Formulaire non valide")
                print(form_update.errors)
        elif request.method == "GET":
            update_form_choices_annulation(form_update)
            str_sql_id_annulation = """
                SELECT 
                    ID_AnnulerCours, 
                    FK_Inscrirecours, 
                    Raison
                FROM t_annulation 
                WHERE ID_AnnulerCours = %(id_annulation)s
            """
            valeur_select_dictionnaire = {"id_annulation": id_annulation_update}

            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_annulation, valeur_select_dictionnaire)
                data_annulation = mybd_conn.fetchone()

                if data_annulation is None:
                    flash('Erreur: Annulation non trouvée.', 'error')
                    return redirect(url_for('annulation_afficher', order_by="DESC", id_personne_sel=0))

            form_update.fk_inscrirecours_hidden.data = data_annulation["FK_Inscrirecours"]
            form_update.raison_updatewtf.data = data_annulation["Raison"]

            str_sql_personne_cours = """
                SELECT 
                    p.Nom, 
                    p.Prenom, 
                    c.Titre 
                FROM t_personne p
                JOIN t_inscrirecours ic ON p.Id_personne = ic.FK_Personne
                JOIN t_cours c ON ic.FK_Cours = c.Id_cours
                WHERE ic.ID_InscrireCours = %(fk_inscrirecours)s
            """
            valeur_personne_cours = {"fk_inscrirecours": data_annulation["FK_Inscrirecours"]}

            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_personne_cours, valeur_personne_cours)
                data_personne_cours = mybd_conn.fetchone()

                if data_personne_cours is None:
                    flash('Erreur: Informations de la personne ou du cours non trouvées.', 'error')
                    return redirect(url_for('annulation_afficher', order_by="DESC", id_personne_sel=0))

            form_update.personne_wtf.data = f"{data_personne_cours['Nom']} {data_personne_cours['Prenom']}"
            form_update.fk_inscrirecours_display.data = data_personne_cours["Titre"]

    except Exception as Exception_annulation_update_wtf:
        raise ExceptionAnnulationUpdateWtf(f"fichier : {Path(__file__).name}  ; "
                                           f"{annulation_update.__name__} ; "
                                           f"{Exception_annulation_update_wtf}")

    return render_template('Annulation/annulation_update_wtf.html', form_update=form_update)


"""4. Route delete"""

@app.route("/annulation_delete", methods=['GET', 'POST'])
def annulation_delete():
    form_delete = AnnulationDeleteWTF()
    id_annulation_delete = request.values.get('id_annulation_btn_delete_html')
    data_annulation_delete = None
    associations = None
    btn_submit_del = False

    try:
        if request.method == "POST":
            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("annulation_afficher", order_by='ASC', id_personne_sel=0))

            if form_delete.submit_btn_confirmation.data:
                data_annulation_delete = session.get('data_annulation_delete')
                flash("Effacer l'annulation de façon définitive de la BD !!!", "danger")
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_annulation": id_annulation_delete}
                delete_annulation = """DELETE FROM t_annulation WHERE ID_AnnulerCours = %(value_id_annulation)s"""

                with DBconnection() as mconn_bd:
                    mconn_bd.execute(delete_annulation, valeur_delete_dictionnaire)

                flash("L'annulation a été définitivement effacée !!", "success")
                return redirect(url_for("annulation_afficher", order_by='ASC', id_personne_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_annulation": id_annulation_delete}

            select_annulation_info = """SELECT * FROM t_annulation WHERE ID_AnnulerCours = %(value_id_annulation)s"""
            str_sql_personne_cours = """
                SELECT p.Nom, p.Prenom, c.Titre 
                FROM t_personne p
                JOIN t_inscrirecours ic ON p.Id_personne = ic.FK_Personne
                JOIN t_cours c ON ic.FK_Cours = c.Id_cours
                WHERE ic.ID_InscrireCours = %(fk_inscrirecours)s
            """

            with DBconnection() as mydb_conn:
                mydb_conn.execute(select_annulation_info, valeur_select_dictionnaire)
                data_annulation_delete = mydb_conn.fetchone()

                if data_annulation_delete:
                    session['data_annulation_delete'] = data_annulation_delete
                    valeur_personne_cours = {"fk_inscrirecours": data_annulation_delete["FK_Inscrirecours"]}
                    mydb_conn.execute(str_sql_personne_cours, valeur_personne_cours)
                    associations = mydb_conn.fetchall()
                else:
                    flash("L'annulation demandée n'existe pas.", "warning")
                    return redirect(url_for("annulation_afficher", order_by='ASC', id_personne_sel=0))

    except Exception as Exception_annulation_delete_wtf:
        raise ExceptionAnnulationDeleteWtf(f"fichier : {Path(__file__).name}; "
                                           f"{annulation_delete.__name__}; "
                                           f"{Exception_annulation_delete_wtf}")

    return render_template("Annulation/annulation_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_annulation_delete=data_annulation_delete,
                           associations=associations)
