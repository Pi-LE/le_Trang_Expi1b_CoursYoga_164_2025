import pymysql
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

# Connexion à la base de données MySQL
connection = pymysql.connect(
    host='localhost',
    user='root',
    password="",
    db='le_trang_expi1b_coursyoga'
)

# Interroger les informations de schéma pour toutes les tables
query = """
SELECT 
    TABLE_NAME AS 'Table',
    COLUMN_NAME AS 'Column',
    DATA_TYPE AS 'Data Type',
    IS_NULLABLE AS 'Nullable',
    COLUMN_KEY AS 'Key',
    COLUMN_DEFAULT AS 'Default',
    EXTRA AS 'Extra'
FROM
    INFORMATION_SCHEMA.COLUMNS
WHERE
    TABLE_SCHEMA = 'le_trang_expi1b_coursyoga';
"""

# Exécuter la requête et lire les résultats dans un DataFrame Pandas
df = pd.read_sql(query, connection)
connection.close()

# Fonction pour créer le PDF
def create_pdf(dataframe, pdf_filename):
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Obtenir la liste des tables
    tables = dataframe['Table'].unique()

    for table in tables:
        # Ajouter un titre pour chaque table
        elements.append(Paragraph(f"Table: {table}", styles['Heading2']))
        elements.append(Spacer(1, 12))

        # Filtrer le DataFrame pour chaque table
        table_df = dataframe[dataframe['Table'] == table]

        # Convertir le DataFrame en une liste de listes pour le tableau
        data = [table_df.columns.to_list()] + table_df.values.tolist()

        # Créer un tableau pour la table
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        elements.append(table)
        elements.append(Spacer(1, 24))  # Ajouter un espace entre les tables

    doc.build(elements)

# Créer le PDF
create_pdf(df, 'LeTrang_Expi1b_CoursYoga_Dictionnaire_de_Données.pdf')

print("Le dictionnaire de données a été créé avec succès en format PDF.")
