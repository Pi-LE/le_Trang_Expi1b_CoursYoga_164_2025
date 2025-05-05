"""

    Gestions des "routes" FLASK et des données pour la personne paye le cours
"""


from pathlib import Path

from flask import redirect, jsonify
from flask import request
from flask import session
from flask import url_for
from decimal import Decimal

from APP_COURS.database.database_tools import DBconnection
from APP_COURS.erreurs.exceptions import *
from APP_COURS.Payement.Payement_wtf import PaiementAjouter,PaiementUpdate,PaiementDelete


"""Afficher table payercours inclue personne paie le cours
"""

@app.route("/payercours_afficher/<string:order_by>/<int:id_personne_sel>", methods=['GET', 'POST'])
def payercours_afficher(order_by, id_personne_sel):
    highlighted_id = request.args.get('highlighted_id', None)

    try:
        with DBconnection() as mc_afficher:
            if order_by == "ASC" and id_personne_sel == 0:
                strsql_afficher = """SELECT pm.ID_payement, 
                                       p.Nom, p.Prenom, p.NumeroAVS, 
                                       c.Titre, c.Prix_par_session, pm.Montant_restant,
                                       pm.Mode_paiement, pm.Montant_paye, pm.Montant_principal, pm.Statut, pm.Rabais,
                                       pm.Description_Rabais
                                       FROM t_payement pm
                                       JOIN t_inscrirecours ic ON pm.FK_Inscrirecours = ic.ID_InscrireCours
                                       JOIN t_cours c ON ic.FK_Cours = c.Id_cours
                                       JOIN t_personne p ON ic.FK_Personne = p.Id_personne
                                       ORDER BY pm.ID_payement ASC
                                """
                mc_afficher.execute(strsql_afficher)
            elif order_by == "ASC":
                valeur_Id_personne_selected_dictionnaire = {"value_Id_personne_selected": id_personne_sel}
                strsql_afficher = """SELECT pm.ID_payement, 
                                       p.Nom, p.Prenom, p.NumeroAVS, 
                                       c.Titre, c.Prix_par_session, pm.Montant_principal,
                                       pm.Mode_paiement, pm.Montant_paye, pm.Statut, pm.Rabais, pm.Montant_restant,
                                       pm.Description_Rabais
                                       FROM t_payement pm
                                       JOIN t_inscrirecours ic ON pm.FK_Inscrirecours = ic.ID_InscrireCours
                                       JOIN t_cours c ON ic.FK_Cours = c.Id_cours
                                       JOIN t_personne p ON ic.FK_Personne = p.Id_personne
                                       WHERE p.Id_personne = %(value_Id_personne_selected)s
                                       ORDER BY pm.ID_payement ASC"""
                mc_afficher.execute(strsql_afficher, valeur_Id_personne_selected_dictionnaire)
            else:
                strsql_afficher = """SELECT pm.ID_payement, 
                                       p.Nom, p.Prenom, p.NumeroAVS, 
                                       c.Titre, c.Prix_par_session, pm.Montant_principal,
                                       pm.Mode_paiement, pm.Montant_paye, pm.Statut, pm.Rabais, pm.Montant_restant,
                                       pm.Description_Rabais
                                       FROM t_payement pm
                                       JOIN t_inscrirecours ic ON pm.FK_Inscrirecours = ic.ID_InscrireCours
                                       JOIN t_cours c ON ic.FK_Cours = c.Id_cours
                                       JOIN t_personne p ON ic.FK_Personne = p.Id_personne
                                       ORDER BY pm.ID_payement DESC"""
                mc_afficher.execute(strsql_afficher)

            data_inscriptions = mc_afficher.fetchall()
            print("Données récupérées:", data_inscriptions)

            if not data_inscriptions and id_personne_sel == 0:
                flash("La table 't_payercours' est vide. !!", "warning")
            elif not data_inscriptions and id_personne_sel > 0:
                flash("Le paiement demandé n'existe pas !!", "warning")
            else:
                flash("Données des paiements affichées !!", "success")

    except Exception as Exception_payercours_afficher:
        raise ExceptionPayerCoursAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{payercours_afficher.__name__} ; "
                                          f"{Exception_payercours_afficher}")

    return render_template("Payement/payercours_afficher.html", data=data_inscriptions, highlighted_id=highlighted_id)





""" Route Payement ajouter avec requetes insert"""

@app.route('/paiement_ajouter', methods=['GET', 'POST'])
def paiement_ajouter():
    form = PaiementAjouter()
    if request.method == 'GET':
        update_form_choices(form)
    elif request.method == 'POST':
        update_form_choices(form)
        if form.validate_on_submit():
            fk_inscrirecours = form.fk_inscrirecours.data
            rabais = form.rabais_wtf.data
            montant_paye = form.montant_wtf.data
            description_rabais = form.description_rabais_wtf.data
            mode_paiement = form.mode_paiement_wtf.data
            statut = form.statut_wtf.data

            # Récupérer le montant principal à partir de l'ID du cours associé à l'inscription
            try:
                with DBconnection() as db:
                    db.execute("""
                        SELECT c.Prix_par_session FROM t_inscrirecours ic
                        JOIN t_cours c ON ic.FK_Cours = c.Id_cours
                        WHERE ic.ID_InscrireCours = %s
                    """, (fk_inscrirecours,))
                    montant_principal = db.fetchone()['Prix_par_session']

                    # Calcul des montants après application du rabais
                    montant_final_apres_rabais, montant_restant = calculer_paiement(montant_principal, rabais, montant_paye)

                    # Insertion des données calculées et saisies dans la base de données
                    db.execute("""
                        INSERT INTO t_payement (
                            FK_Inscrirecours, Montant_principal, Rabais, Description_Rabais, Montant_paye, Montant_restant, Mode_paiement, Statut
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        fk_inscrirecours,
                        montant_principal,  # Montant principal inchangé
                        rabais,
                        description_rabais,
                        montant_paye,
                        montant_restant,  # Calculé à partir du montant après rabais
                        mode_paiement,
                        statut
                    ))
                    db.execute("ALTER TABLE t_payement AUTO_INCREMENT = 1")
                    flash('Paiement ajouté avec succès!', 'success')

                    # Récupérer l'ID du paiement ajouté pour la mise en surbrillance
                    db.execute("SELECT LAST_INSERT_ID() as last_id")
                    last_id = db.fetchone()['last_id']

                    return redirect(url_for('payercours_afficher', order_by="DESC", id_personne_sel=0, highlighted_id=last_id))
            except Exception as Exception_payercour_ajouter:
                raise ExceptionPaiementAjouter(f"fichier : {Path(__file__).name}  ;  "
                                               f"{paiement_ajouter.__name__} ; "
                                               f"{Exception_payercour_ajouter}")
    return render_template('Payement/payercours_ajouter_wtf.html', form=form)



"""1.Ajouter route charge cours pour interface AJAX"""
@app.route('/charger_cours')
def charger_cours():
    personne_id = request.args.get('personne_id')
    with DBconnection() as db:
        db.execute("""
            SELECT ic.ID_InscrireCours, 
                   c.Titre, 
                   c.Prix_par_session  
            FROM t_inscrirecours ic
            JOIN t_cours c ON ic.FK_Cours = c.Id_cours
            WHERE ic.FK_Personne = %s AND NOT EXISTS (
                SELECT 1 FROM t_payement pm WHERE pm.FK_Inscrirecours = ic.ID_InscrireCours)
        """, (personne_id,))
        cours = db.fetchall()
        return jsonify([{'id': c['ID_InscrireCours'], 'titre': c['Titre'], 'prix': c['Prix_par_session']} for c in cours])





"""2. update des choix pour cours et personne avec select leur données"""
def update_form_choices(form):
    """Mettre à jour les choix des champs SelectField à partir de la base de données."""
    with DBconnection() as db:
        selected_person_id = request.form.get('personne_wtf', type=int)
        selected_course_id = request.form.get('fk_inscrirecours', type=int)
        db.execute("""
            SELECT DISTINCT p.Id_personne, CONCAT(p.Nom, '_ ', p.Prenom, '__ [AVS:', p.NumeroAVS, ']') AS Identite
            FROM t_personne p
            JOIN t_inscrirecours ic ON p.Id_personne = ic.FK_Personne
            JOIN t_cours c ON ic.FK_Cours = c.Id_cours
            LEFT JOIN t_payement pm ON ic.ID_InscrireCours = pm.FK_Inscrirecours
            WHERE pm.ID_payement IS NULL
        """)
        personnes = db.fetchall()
        form.personne_wtf.choices = [(p['Id_personne'], p['Identite']) for p in personnes] if personnes else [(-1, 'Aucune personne disponible')]
        print("Personne sélectionnée ID:", form.personne_wtf.data)
        print("Options de personnes:", form.personne_wtf.choices)

        if selected_person_id and selected_person_id not in [choice[0] for choice in form.personne_wtf.choices]:
            flash('La personne sélectionnée n\'est plus valide, veuillez rafraîchir la page et réessayer.', 'error')

        # Pré-charger les cours pour la première personne disponible si possible
        if personnes:
            selected_person_id = personnes[0]['Id_personne']
            db.execute("""
                SELECT ic.ID_InscrireCours, c.Titre, c.Prix_par_session 
                FROM t_inscrirecours ic
                JOIN t_cours c ON ic.FK_Cours = c.Id_cours
                WHERE ic.FK_Personne = %s AND NOT EXISTS (
                    SELECT 1 FROM t_payement pm WHERE pm.FK_Inscrirecours = ic.ID_InscrireCours)
            """, (selected_person_id,))
            cours = db.fetchall()
            form.fk_inscrirecours.choices = [(c['ID_InscrireCours'], c['Titre']) for c in cours] if cours else [(-1, 'Aucun cours disponible')]
            # Mettre à jour le montant principal si un cours est déjà sélectionné
            if selected_course_id:
                selected_course = next((c for c in cours if c['ID_InscrireCours'] == selected_course_id), None)
                if selected_course:
                    form.montant_principal_wtf.data = selected_course['Prix_par_session']
                    print("Prix du cours sélectionné:", selected_course['Prix_par_session'])
                else:
                    flash('Le cours sélectionné n\'est plus valide, veuillez choisir un autre cours.', 'error')

            print("montant_principa_Cours_select:", form.fk_inscrirecours.data)
            print("Cours sélectionné ID:", form.montant_principal_wtf.data)
            print("Options de cours:", form.fk_inscrirecours.choices)
            if selected_course_id and selected_course_id not in [choice[0] for choice in form.fk_inscrirecours.choices]:
                flash('Le cours sélectionné n\'est plus valide, veuillez rafraîchir la page et réessayer.', 'error')


"""3. la fonction calculer_paiement"""

def calculer_paiement(prix_par_session, rabais, montant_paye):
    # Convertir tous les arguments en Decimal pour éviter les problèmes de type
    prix_par_session = Decimal(prix_par_session)
    rabais = Decimal(rabais)
    montant_paye = Decimal(montant_paye)

    # Assumant que rabais est toujours en pourcentage et passé comme tel (ex: 20 pour 20%)
    rabais_decimal = rabais / Decimal(100)
    montant_final_apres_rabais = prix_par_session * (Decimal(1) - rabais_decimal)
    montant_restant = montant_final_apres_rabais - montant_paye
    return montant_final_apres_rabais, montant_restant


"""Route Modifier le Paiement un cours """
@app.route("/paiement_update", methods=['GET', 'POST'])
def paiement_update():
    id_paiement_update = request.values['id_paiement_btn_edit_html']
    form_update = PaiementUpdate()
    try:
        if request.method == "POST":
            update_form_choices(form_update)
            if form_update.validate_on_submit():
                fk_inscrirecours = form_update.fk_inscrirecours_hidden.data
                rabais = form_update.rabais_updatewtf.data
                montant_paye = form_update.montant_paye_updatewtf.data
                description_rabais = form_update.description_rabais_updatewtf.data
                mode_paiement = form_update.mode_paiement_updatewtf.data
                statut = form_update.statut_updatewtf.data

                with DBconnection() as db:
                    db.execute("""
                        SELECT c.Prix_par_session 
                        FROM t_inscrirecours ic
                        JOIN t_cours c ON ic.FK_Cours = c.Id_cours
                        WHERE ic.ID_InscrireCours = %s
                    """, (fk_inscrirecours,))
                    montant_principal = db.fetchone()

                    if montant_principal is None:
                        flash('Erreur: Cours non trouvé.', 'error')
                        return redirect(url_for('paiement_update', id_paiement_btn_edit_html=id_paiement_update))

                    montant_principal = montant_principal['Prix_par_session']
                    montant_final_apres_rabais, montant_restant = calculer_paiement(montant_principal, rabais, montant_paye)

                    db.execute("""
                        UPDATE t_payement SET 
                            FK_Inscrirecours = %(fk_inscrirecours)s,
                            Montant_principal = %(montant_principal)s,
                            Rabais = %(rabais)s,
                            Description_Rabais = %(description_rabais)s,
                            Montant_paye = %(montant_paye)s,
                            Montant_restant = %(montant_restant)s,
                            Mode_paiement = %(mode_paiement)s,
                            Statut = %(statut)s
                        WHERE ID_payement = %(id_paiement)s
                    """, {
                        'fk_inscrirecours': fk_inscrirecours,
                        'montant_principal': montant_principal,
                        'rabais': rabais,
                        'description_rabais': description_rabais,
                        'montant_paye': montant_paye,
                        'montant_restant': montant_restant,
                        'mode_paiement': mode_paiement,
                        'statut': statut,
                        'id_paiement': id_paiement_update
                    })

                return redirect(url_for('payercours_afficher', order_by="DESC", id_personne_sel=id_paiement_update, highlighted_id=id_paiement_update))
            else:
                print("Formulaire non valide")
                print(form_update.errors)
            # MéTHODE GET
        elif request.method == "GET":
            update_form_choices(form_update)
            str_sql_id_paiement = """
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
                WHERE ID_payement = %(id_paiement)s
            """
            valeur_select_dictionnaire = {"id_paiement": id_paiement_update}

            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_paiement, valeur_select_dictionnaire)
                data_paiement = mybd_conn.fetchone()

                if data_paiement is None:
                    flash('Erreur: Paiement non trouvé.', 'error')
                    return redirect(url_for('payercours_afficher', order_by="DESC", id_personne_sel=0))

            form_update.fk_inscrirecours_hidden.data = data_paiement["FK_Inscrirecours"]
            form_update.montant_principal.data = data_paiement["Montant_principal"]
            form_update.rabais_updatewtf.data = data_paiement["Rabais"]
            form_update.montant_paye_updatewtf.data = data_paiement["Montant_paye"]
            form_update.mode_paiement_updatewtf.data = data_paiement["Mode_paiement"]
            form_update.statut_updatewtf.data = data_paiement["Statut"]
            form_update.description_rabais_updatewtf.data = data_paiement["Description_Rabais"]

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
            valeur_personne_cours = {"fk_inscrirecours": data_paiement["FK_Inscrirecours"]}

            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_personne_cours, valeur_personne_cours)
                data_personne_cours = mybd_conn.fetchone()

                if data_personne_cours is None:
                    flash('Erreur: Informations de la personne ou du cours non trouvées.', 'error')
                    return redirect(url_for('payercours_afficher', order_by="DESC", id_personne_sel=0))

            form_update.personne_wtf.data = f"{data_personne_cours['Nom']} {data_personne_cours['Prenom']}"
            form_update.fk_inscrirecours_display.data = data_personne_cours["Titre"]

    except Exception as Exception_paiement_update_wtf:
        raise ExceptionPaiementUpdateWtf(f"fichier : {Path(__file__).name}  ; "
                                         f"{paiement_update.__name__} ; "
                                         f"{Exception_paiement_update_wtf}")

    return render_template('Payement/payercours_update_wtf.html', form_update=form_update)



"""#Route Delete"""


@app.route("/paiement_delete", methods=['GET', 'POST'])
def paiement_delete():
    form_delete = PaiementDelete()
    id_paiement_delete = request.values.get('id_paiement_btn_delete_html')
    data_paiement_delete = None
    associations = None
    btn_submit_del = False

    try:
        if request.method == "POST":
            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("payercours_afficher", order_by='ASC', id_personne_sel=0))

            if form_delete.submit_btn_confirmation.data:
                data_paiement_delete = session.get('data_paiement_delete')
                flash("Effacer le Paiement de façon définitive de la BD !!!", "danger")
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_paiement": id_paiement_delete}
                delete_paiement = """DELETE FROM t_payement WHERE ID_payement = %(value_id_paiement)s"""

                with DBconnection() as mconn_bd:
                    mconn_bd.execute(delete_paiement, valeur_delete_dictionnaire)

                flash("Le Paiement a été définitivement effacé !!", "success")
                return redirect(url_for("payercours_afficher", order_by='ASC', id_personne_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_paiement": id_paiement_delete}

            select_paiement_info = """SELECT * FROM t_payement WHERE ID_payement = %(value_id_paiement)s"""
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

            with DBconnection() as mydb_conn:
                mydb_conn.execute(select_paiement_info, valeur_select_dictionnaire)
                data_paiement_delete = mydb_conn.fetchone()

                if data_paiement_delete:
                    session['data_paiement_delete'] = data_paiement_delete
                    valeur_personne_cours = {"fk_inscrirecours": data_paiement_delete["FK_Inscrirecours"]}
                    mydb_conn.execute(str_sql_personne_cours, valeur_personne_cours)
                    associations = mydb_conn.fetchall()

    except Exception as Exception_paiement_delete_wtf:
        raise ExceptionPaiementDeleteWtf(f"fichier : {Path(__file__).name}; "
                                         f"{paiement_delete.__name__}; "
                                         f"{Exception_paiement_delete_wtf}")

    return render_template("Payement/payercours_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_paiement_delete=data_paiement_delete,
                           associations=associations)


