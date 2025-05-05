"""
    Fichier : gestion_genres_wtf_forms.py
    Auteur : OM 2021.03.22
    Gestion des formulaires avec WTF
"""
from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms import SubmitField
from wtforms.validators import Length, InputRequired, DataRequired
from wtforms.validators import Regexp


class FormWTFAjouterFonction(FlaskForm):
    """
        Dans le formulaire "fonction_ajouter_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_fonction_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_fonction_wtf = StringField("Clavioter le type de fonction ", validators=[
        Length(min=2, max=50, message="Le type de fonction doit avoir entre 2 et 50 caractères"),
        Regexp(nom_fonction_regexp,
               message="Pas de chiffres, de caractères spéciaux, d'espace à double, de double apostrophe, de double trait union")
    ])
    submit = SubmitField("Enregistrer fonction")

class FormWTFUpdateFonction(FlaskForm):
    """
        Dans le formulaire "fonction_update_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_fonction_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_fonction_update_wtf = StringField("Clavioter le type de fonction ", validators=[
        Length(min=2, max=50, message="Le type de fonction doit avoir entre 2 et 50 caractères"),
        Regexp(nom_fonction_update_regexp,
               message="Pas de chiffres, de caractères spéciaux, d'espace à double, de double apostrophe, de double trait union")
    ])
    submit = SubmitField("Modifier fonction")

class FormWTFDeleteFonction(FlaskForm):
    """
        Dans le formulaire "fonction_delete_wtf.html"

        nom_fonction_delete_wtf : Champ qui reçoit la valeur du type de fonction, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "type de fonction".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_fonction".
    """
    nom_fonction_delete_wtf = StringField("Effacer ce type de fonction")
    submit_btn_del = SubmitField("Effacer fonction")
    submit_btn_conf_del = SubmitField("Êtes-vous sûr d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")