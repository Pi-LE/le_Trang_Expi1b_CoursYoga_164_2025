# personnes_wtf_forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms import SubmitField,SelectField
from wtforms.validators import Length, InputRequired, DataRequired
from wtforms.validators import Regexp


class FormWTFAjouterPersonne(FlaskForm):
    nom_personne_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_personne_wtf = StringField("Nom de la personne ", validators=[
        Length(min=2, max=20, message="Le nom doit avoir entre 2 et 20 caractères"),
        Regexp(nom_personne_regexp, message="Le nom ne doit pas contenir de chiffres, de caractères spéciaux, "
                                             "d'espaces doubles, de double apostrophes ou de double trait d'union")
    ])
    prenom_personne_wtf = StringField("Prénom de la personne ", validators=[
        Length(min=2, max=20, message="Le prénom doit avoir entre 2 et 20 caractères"),
        Regexp(nom_personne_regexp, message="Le prénom ne doit pas contenir de chiffres, de caractères spéciaux, "
                                             "d'espaces doubles, de double apostrophes ou de double trait d'union")
    ])
    date_naissance_personne_wtf = DateField("Date Naissance", validators=[
        InputRequired("La date de naissance est obligatoire"),
        DataRequired("Date non valide")
    ])
    numero_avs_personne_wtf = StringField("Numéro AVS de la personne", validators=[
        Length(min=13, max=13, message="Le numéro AVS doit avoir exactement 13 caractères."),
        Regexp(r'^\d{13}$', message="Le numéro AVS doit être 13 chiffres sans interruption.")

    ])
    sexe_personne_wtf = SelectField("Sexe de la personne ", choices=[('Masculin', 'Masculin'), ('Féminin', 'Féminin')])
    submit = SubmitField("Enregistrer personne")

class FormWTFUpdatePersonne(FlaskForm):
    nom_personne_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_personne_update_wtf = StringField("Nom de la personne ", validators=[
        Length(min=2, max=20, message="Le nom doit avoir entre 2 et 20 caractères"),
        Regexp(nom_personne_update_regexp, message="Le nom ne doit pas contenir de chiffres, de caractères spéciaux, "
                                                    "d'espaces doubles, de double apostrophes ou de double trait d'union")
    ])
    prenom_personne_update_wtf = StringField("Prénom de la personne ", validators=[
        Length(min=2, max=20, message="Le prénom doit avoir entre 2 et 20 caractères"),
        Regexp(nom_personne_update_regexp, message="Le prénom ne doit pas contenir de chiffres, de caractères spéciaux, "
                                                     "d'espaces doubles, de double apostrophes ou de double trait d'union")
    ])
    date_naissance_personne_wtf_essai = DateField("Essai date", validators=[
        InputRequired("La date de naissance est obligatoire"),
        DataRequired("Date non valide")
    ])
    numero_avs_personne_wtf = StringField("Numéro AVS de la personne", validators=[
        Length(min=13, max=13, message="Le numéro AVS doit avoir exactement 13 caractères."),
        Regexp(r'^\d{13}$', message="Le numéro AVS doit être 13 chiffres sans interruption.")
    ])
    sexe_personne_wtf = SelectField("Sexe de la personne ", choices=[('Masculin', 'Masculin'), ('Féminin', 'Féminin')])
    submit = SubmitField("Modifier personne")


class FormWTFDeletePersonne(FlaskForm):
    nom_personne_delete_wtf = StringField("Effacer cette personne")
    submit_btn_del = SubmitField("Effacer personne")
    submit_btn_conf_del = SubmitField("Êtes-vous sûr d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
