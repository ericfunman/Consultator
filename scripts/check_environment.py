#!/usr/bin/env python3
"""
Script de vérification et initialisation de l'environnement Consultator
Vérifie que la base de données est prête et les données de test sont chargées
"""

import os
import sys
from pathlib import Path

# Ajouter le chemin de l'app au Python path
app_path = Path(__file__).parent / 'app'
sys.path.insert(0, str(app_path))

def check_database():
    """Vérifie et initialise la base de données"""
    try:
        from database.database import init_database, DATABASE_PATH
        
        print("🔍 Vérification de la base de données...")
        
        # Vérifier si le fichier existe
        if not os.path.exists(DATABASE_PATH):
            print(f"⚠️  Base de données introuvable: {DATABASE_PATH}")
            print("🔧 Initialisation de la base de données...")
            
            if init_database():
                print("✅ Base de données créée avec succès")
            else:
                print("❌ Échec de la création de la base de données")
                return False
        else:
            print(f"✅ Base de données trouvée: {DATABASE_PATH}")
            
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification de la BD: {e}")
        return False

def check_test_data():
    """Vérifie si les données de test sont présentes"""
    try:
        from database.database import get_database_session
        from database.models import Consultant
        
        print("🔍 Vérification des données de test...")
        
        with get_database_session() as session:
            consultant_count = session.query(Consultant).count()
            
            if consultant_count == 0:
                print("⚠️  Aucun consultant trouvé dans la base")
                print("💡 Conseil: Exécutez 'python scripts/populate_test_data.py' pour charger les données de test")
                return False
            else:
                print(f"✅ {consultant_count} consultant(s) trouvé(s) dans la base")
                return True
                
    except Exception as e:
        print(f"❌ Erreur lors de la vérification des données: {e}")
        return False

def main():
    """Fonction principale de vérification"""
    print("🚀 Vérification de l'environnement Consultator")
    print("=" * 50)
    
    # Vérifier la base de données
    db_ok = check_database()
    
    # Vérifier les données de test
    data_ok = check_test_data()
    
    print("=" * 50)
    
    if db_ok and data_ok:
        print("🎉 Environnement prêt ! Vous pouvez lancer l'application")
        print("   Commande: python run.py")
    elif db_ok:
        print("⚠️  Base de données OK mais données manquantes")
        print("   Commande suggérée: python scripts/populate_test_data.py")
    else:
        print("❌ Problème avec l'environnement, vérifiez les erreurs ci-dessus")
        
    return db_ok and data_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
