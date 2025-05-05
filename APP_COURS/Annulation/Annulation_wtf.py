from flask_wtf import FlaskForm
from wtforms import DecimalField, SelectField, StringField, SubmitField
from wtforms.fields.simple import HiddenField
from wtforms.validators import DataRequired, Optional

class AnnulationAjouterWTF(FlaskForm):
    personne_wtf = SelectField('Personne', coerce=int, validators=[DataRequired()])
    fk_inscrirecours = SelectField('Cours Inscription', coerce=int, validators=[DataRequired()])
    raison_wtf = SelectField('Raison Annulation', choices=[
        ('Absent', 'Absent'), ('Santé', 'Santé'),
        ('Voyage', 'Voyage'), ('Raisons familiales', 'Raisons familiales'),
        ('Problème technique', 'Problème technique'), ('Examen', 'Examen'),
        ('Météo', 'Météo'), ('Grève', 'Grève'),
        ('Congé', 'Congé'), ('Cours remplacé', 'Cours remplacé'),
        ('Autre', 'Autre')
    ], validators=[DataRequired()])
    submit = SubmitField('Enregistrer')



class AnnulationUpdateWTF(FlaskForm):
    personne_wtf = StringField('Personne', validators=[Optional()], render_kw={"readonly": "readonly"})
    fk_inscrirecours_hidden = HiddenField('Cours Inscription ID')
    fk_inscrirecours_display = StringField('Cours Inscription', render_kw={"readonly": "readonly"})
    raison_updatewtf = SelectField('Raison Annulation', choices=[
        ('Absent', 'Absent'), ('Santé', 'Santé'),
        ('Voyage', 'Voyage'), ('Raisons familiales', 'Raisons familiales'),
        ('Problème technique', 'Problème technique'), ('Examen', 'Examen'),
        ('Météo', 'Météo'), ('Grève', 'Grève'),
        ('Congé', 'Congé'), ('Cours remplacé', 'Cours remplacé'),
        ('Autre', 'Autre')
    ], validators=[DataRequired()])
    submit = SubmitField('Mettre à jour')


class AnnulationDeleteWTF(FlaskForm):
    """

        AnnulationDelete_wtf : Champ qui reçoit la valeur du film, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "paiement".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_paiement".
    """
    AnnulationDelete_wtf = StringField("Effacer cet Annulation?")
    submit_btn_del = SubmitField("Effacer l'Annulation'")
    submit_btn_confirmation = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
