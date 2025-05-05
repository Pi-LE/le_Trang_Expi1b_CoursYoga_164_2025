from flask_wtf import FlaskForm
from wtforms import DecimalField, SelectField, StringField, SubmitField
from wtforms.fields.simple import HiddenField
from wtforms.validators import DataRequired, Optional

class PaiementAjouter(FlaskForm):
    personne_wtf = SelectField('Personne', coerce=int, validators=[DataRequired()])
    fk_inscrirecours = SelectField('Cours Inscription', coerce=int, validators=[DataRequired()])
    montant_principal_wtf = DecimalField('Montant principal', validators=[Optional()], render_kw={"readonly": "readonly"})
    montant_wtf = DecimalField('Montant payé', validators=[DataRequired()])
    montant_restant_wtf = DecimalField('Montant Restant', render_kw={"readonly": "readonly"})
    mode_paiement_wtf = SelectField('Mode de Paiement', choices=[
        ('Carte de crédit', 'Carte de crédit'),
        ('PayPal', 'PayPal'),
        ('Virement bancaire', 'Virement bancaire'),
        ('TWINT', 'TWINT'),
        ('Espèces', 'Espèces')
    ], validators=[DataRequired()])
    statut_wtf = SelectField('Statut Paiement', choices=[
        ('en attente', 'en attente'),
        ('réussi', 'réussi'),
        ('payé partiel', 'payé partiel'),
        ('échoué', 'échoué')
    ], validators=[DataRequired()])
    rabais_wtf = DecimalField('Rabais (%)', validators=[Optional()], default=0.0)
    description_rabais_wtf = SelectField('Description Rabais', choices=[
        ('rabais famille', 'rabais famille'),
        ('welcome20%', 'welcome20%'),
        ('special 50%', 'special 50%'),
        ('Aucune Rabais', 'Aucune Rabais')
    ])
    submit = SubmitField('Enregistrer')


class PaiementUpdate(FlaskForm):
    personne_wtf = StringField('Personne', validators=[Optional()], render_kw={"readonly": "readonly"})
    fk_inscrirecours_hidden = HiddenField('Cours Inscription ID')
    fk_inscrirecours_display = StringField('Cours Inscription', render_kw={"readonly": "readonly"})
    montant_principal = DecimalField('Montant principal', validators=[Optional()], render_kw={"readonly": "readonly"})
    montant_paye_updatewtf = DecimalField('Montant payé', validators=[DataRequired()])
    montant_restant_updatewtf = DecimalField('Montant Restant', render_kw={"readonly": "readonly"})
    mode_paiement_updatewtf = SelectField('Mode de Paiement', choices=[
        ('Carte de crédit', 'Carte de crédit'),
        ('PayPal', 'PayPal'),
        ('Virement bancaire', 'Virement bancaire'),
        ('TWINT', 'TWINT'),
        ('Espèces', 'Espèces')
    ], validators=[DataRequired()])
    statut_updatewtf = SelectField('Statut Paiement', choices=[
        ('en attente', 'en attente'),
        ('réussi', 'réussi'),
        ('payé partiel', 'payé partiel'),
        ('échoué', 'échoué')
    ], validators=[DataRequired()])
    rabais_updatewtf = DecimalField('Rabais (%)', validators=[Optional()], default=0.0)
    description_rabais_updatewtf = SelectField('Description Rabais', choices=[
        ('rabais famille', 'rabais famille'),
        ('welcome20%', 'welcome20%'),
        ('special 50%', 'special 50%'),
        ('Aucune Rabais', 'Aucune Rabais')
    ])
    submit = SubmitField('Mettre à jour')


class PaiementDelete(FlaskForm):
    """

        PaiementDelete_wtf : Champ qui reçoit la valeur du film, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "paiement".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_paiement".
    """
    PaiementDelete_wtf = StringField("Effacer ce Paiement?")
    submit_btn_del = SubmitField("Effacer le Paiement")
    submit_btn_confirmation = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
