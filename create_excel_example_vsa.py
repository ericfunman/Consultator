"""
Script de création d'un fichier Excel d'exemple pour les missions VSA
Montre la structure attendue pour l'import des missions
"""

import pandas as pd
from datetime import date, timedelta
import random

# Données d'exemple pour les missions VSA
sample_data = {
    'user_id': [1, 1, 2, 2, 3, 4, 5],
    'Code': ['SG-001', 'BNP-002', 'CA-001', 'AXA-002', 'ORA-001', 'SFR-001', 'BOU-001'],
    'Orderid': ['CMD-12345', 'CMD-23456', 'CMD-34567', 'CMD-45678', 'CMD-56789', 'CMD-67890', 'CMD-78901'],
    'name': ['Société Générale', 'BNP Paribas', 'Crédit Agricole', 'AXA', 'Orange', 'SFR', 'Bouygues Telecom'],
    'date_debut': [
        date(2024, 1, 15),
        date(2024, 3, 1),
        date(2024, 2, 10),
        date(2024, 4, 5),
        date(2024, 1, 20),
        date(2024, 5, 1),
        date(2024, 6, 15)
    ],
    'date_fin': [
        date(2024, 7, 15),
        date(2024, 9, 1),
        date(2024, 8, 10),
        date(2024, 10, 5),
        date(2024, 7, 20),
        date(2024, 11, 1),
        date(2024, 12, 15)
    ],
    'TJM': [450.0, 520.0, 380.0, 600.0, 480.0, 420.0, 550.0],
    'CJM': [432.0, 498.0, 364.0, 576.0, 460.0, 403.0, 528.0],
    'description': [
        'Développement application bancaire',
        'Refonte système de paiement',
        'Migration infrastructure cloud',
        'Développement API assurance',
        'Optimisation réseau télécom',
        'Modernisation plateforme mobile',
        'Déploiement solution 5G'
    ]
}

# Créer le DataFrame
df = pd.DataFrame(sample_data)

# Créer le fichier Excel avec l'onglet Mission
with pd.ExcelWriter('missions_vsa_example.xlsx', engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Mission', index=False)

    # Ajuster la largeur des colonnes
    worksheet = writer.sheets['Mission']
    for column in worksheet.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = min(max_length + 2, 50)
        worksheet.column_dimensions[column_letter].width = adjusted_width

print("✅ Fichier 'missions_vsa_example.xlsx' créé avec succès !")
print("\nStructure attendue pour l'onglet 'Mission' :")
print("- user_id: ID du consultant (entier)")
print("- Code: Code unique de la mission (chaîne)")
print("- Orderid: Numéro de commande (chaîne)")
print("- name: Nom du client (chaîne)")
print("- date_debut: Date de début (format YYYY-MM-DD)")
print("- date_fin: Date de fin (format YYYY-MM-DD)")
print("- TJM: Taux Journalier Moyen (nombre décimal)")
print("- CJM: Coût Journalier Moyen (nombre décimal)")
print("- description: Description de la mission (optionnel)")