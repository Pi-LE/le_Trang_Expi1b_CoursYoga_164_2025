"""Gestion des formulaires avec WTF pour les films
Fichier : gestion_films_wtf_forms.py
Auteur : OM 2022.04.11

"""
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField,SelectField, FloatField,TextAreaField
from wtforms import SubmitField
from wtforms.validators import Length, InputRequired, NumberRange, DataRequired
from wtforms.validators import Regexp
from wtforms.widgets import TextArea


class FormWTFAddCours(FlaskForm):
    """
        Dans le formulaire "genres_ajouter_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    titre_session_regexp = r"^[A-Za-zÀ-ÖØ-öø-ÿ' \-,!]+$"

    titre_cours_wtf = StringField("Titre du cours", validators=[
        InputRequired(message="Le titre du cours est obligatoire."),
        Length(min=1, max=255, message="Le titre doit avoir entre 1 et 255 caractères."),
        Regexp(titre_session_regexp,
               message="Le titre ne doit contenir que des lettres, des espaces, des apostrophes, des tirets, des virgules ou des points d'exclamation.")
    ])

    niveau_cours_wtf = SelectField("Niveau du cours", choices=[
        ('Débutant', 'Débutant'),
        ('Intermédiaire', 'Intermédiaire'),
        ('Avancé', 'Avancé')
    ], validators=[DataRequired(message="Le choix du niveau est obligatoire.")])
    session_cours_wtf = StringField("Session du cours", validators=[
        InputRequired(message="La session du cours est obligatoire."),
        Length(min=1, max=255, message="La session doit avoir entre 1 et 255 caractères."),

    ])
    prix_par_session_cours_wtf = FloatField("Prix par session", validators=[
        InputRequired(message="Le prix par session est obligatoire."),
        NumberRange(min=0, message="Le prix doit être un nombre positif.")
    ])
    description_cours_wtf = TextAreaField("Description du cours", validators=[
        Length(max=65535, message="La description ne peut pas dépasser 65535 caractères.")
        # Limite technique due à `TEXT` dans MySQL
    ])
    affiche_cours_wtf = TextAreaField("Affiche du cours", validators=[
        Length(max=65535, message="L'affiche ne peut pas dépasser 65535 caractères.")

    ])
    submit = SubmitField("Enregistrer le cours")

class FormWTFUpdateCours(FlaskForm):
    """
        Dans le formulaire "genres_ajouter_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    titre_session_regexp = r"^[A-Za-zÀ-ÖØ-öø-ÿ' \-,!]+$"

    titre_cours_Uwtf = StringField("Titre du cours", validators=[
        InputRequired(message="Le titre du cours est obligatoire."),
        Length(min=1, max=255, message="Le titre doit avoir entre 1 et 255 caractères."),
        Regexp(titre_session_regexp,
               message="Le titre ne doit contenir que des lettres, des espaces, des apostrophes, des tirets, des virgules ou des points d'exclamation.")
    ])

    niveau_cours_Uwtf = SelectField("Niveau du cours", choices=[
        ('Débutant', 'Débutant'),
        ('Intermédiaire', 'Intermédiaire'),
        ('Avancé', 'Avancé')
    ], validators=[DataRequired(message="Le choix du niveau est obligatoire.")])
    session_cours_Uwtf = StringField("Session du cours", validators=[
        InputRequired(message="La session du cours est obligatoire."),
        Length(min=1, max=255, message="La session doit avoir entre 1 et 255 caractères."),

    ])
    prix_par_session_cours_Uwtf = FloatField("Prix par session", validators=[
        InputRequired(message="Le prix par session est obligatoire."),
        NumberRange(min=0, message="Le prix doit être un nombre positif.")
    ])
    description_cours_Uwtf = TextAreaField("Description du cours", validators=[
        Length(max=65535, message="La description ne peut pas dépasser 65535 caractères.")
        # Limite technique due à `TEXT` dans MySQL
    ])
    affiche_cours_Uwtf = TextAreaField("Affiche du cours", validators=[
        Length(max=65535, message="L'affiche ne peut pas dépasser 65535 caractères.")

    ])
    submit = SubmitField("Modifier le cours")


class FormWTFDeleteCours(FlaskForm):
    """

        nom_film_delete_wtf : Champ qui reçoit la valeur du film, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "film".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_film".
    """
    cours_delete_wtf = StringField("Effacer ce Cours?")
    submit_btn_del = SubmitField("Effacer Cour")
    submit_btn_confirmation = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
