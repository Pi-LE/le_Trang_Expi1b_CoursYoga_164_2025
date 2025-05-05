"""Gestion des formulaires avec WTF pour les films
Fichier : gestion_films_wtf_forms.py
Auteur : OM 2022.04.11

"""
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField,SelectField, FloatField,TextAreaField
from wtforms import SubmitField
from wtforms.fields.datetime import TimeField
from wtforms.validators import Length, InputRequired, NumberRange, DataRequired



class FormWTFAjouterHoraire(FlaskForm):
    date_cours_wtf = DateField("Date du cours", format='%Y-%m-%d', validators=[
        DataRequired(message="La date du cours est obligatoire.")
    ])
    jour_semaine_wtf = StringField("Jour de la semaine", validators=[
        DataRequired(message="Le jour de la semaine est obligatoire."),
        Length(min=1, max=50, message="Le jour de la semaine doit avoir entre 1 et 50 caractères.")
    ])
    heure_debut_wtf = TimeField("Heure de début", validators=[
        DataRequired(message="L'heure de début est obligatoire.")
    ])
    heure_fin_wtf = TimeField("Heure de fin", validators=[
        DataRequired(message="L'heure de fin est obligatoire.")
    ])
    submit = SubmitField("Enregistrer l'horaire")


class FormWTFUpdateHoraire(FlaskForm):
    date_cours_Uwtf = DateField("Date du cours", format='%Y-%m-%d', validators=[
        DataRequired(message="La date du cours est obligatoire.")
    ])
    jour_semaine_Uwtf = StringField("Jour de la semaine", validators=[
        DataRequired(message="Le jour de la semaine est obligatoire."),
        Length(min=1, max=50, message="Le jour de la semaine doit avoir entre 1 et 50 caractères.")
    ])
    heure_debut_Uwtf = TimeField("Heure de début", validators=[
        DataRequired(message="L'heure de début est obligatoire.")
    ])
    heure_fin_Uwtf = TimeField("Heure de fin", validators=[
        DataRequired(message="L'heure de fin est obligatoire.")
    ])
    submit = SubmitField("Modifier l'horaire")


class FormWTFDeleteHoraire(FlaskForm):
    horaire_delete_wtf = StringField("Effacer cet Horaire?")
    submit_btn_del = SubmitField("Effacer Horaire")
    submit_btn_confirmation = SubmitField("Êtes-vous sûr d'effacer?")
    submit_btn_annuler = SubmitField("Annuler")
