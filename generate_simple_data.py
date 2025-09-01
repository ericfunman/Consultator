"""
Script de génération rapide de données de test
Génère uniquement des consultants supplémentaires pour tester les performances
"""

import os
import sys
import random
from datetime import datetime, date, timedelta
from faker import Faker

# Ajouter le dossier app au path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from database.database import get_database_session, init_database
from database.models import Consultant, Practice, BusinessManager, ConsultantBusinessManager
from services.consultant_service import ConsultantService

fake = Faker('fr_FR')

def count_existing_data():
    """Compte les données existantes"""
    print("📊 Comptage des données existantes...")
    
    with get_database_session() as session:
        consultants_count = session.query(Consultant).count()
        practices_count = session.query(Practice).count()
        bm_count = session.query(BusinessManager).count()
        
        print(f"👥 Consultants existants: {consultants_count}")
        print(f"🏢 Practices existantes: {practices_count}")
        print(f"👨‍💼 Business Managers existants: {bm_count}")
        
        return consultants_count, practices_count, bm_count

def generate_unique_email(base_name: str, existing_emails: set) -> str:
    """Génère un email unique"""
    counter = 1
    base_email = f"{base_name}@email.com"
    
    while base_email in existing_emails:
        base_email = f"{base_name}{counter}@email.com"
        counter += 1
    
    existing_emails.add(base_email)
    return base_email

def add_consultants_batch(target_total: int = 1000):
    """Ajoute des consultants par batch pour atteindre l'objectif"""
    
    existing_count, practices_count, bm_count = count_existing_data()
    
    if existing_count >= target_total:
        print(f"✅ Objectif déjà atteint: {existing_count} consultants")
        return
    
    to_create = target_total - existing_count
    print(f"🎯 Création de {to_create} consultants supplémentaires...")
    
    with get_database_session() as session:
        # Récupérer les practices et BM existants
        practices = session.query(Practice).all()
        business_managers = session.query(BusinessManager).all()
        
        # Récupérer les emails existants
        existing_emails = set()
        existing_consultants = session.query(Consultant.email).all()
        for (email,) in existing_consultants:
            existing_emails.add(email)
        
        print(f"📧 {len(existing_emails)} emails existants récupérés")
        
        # Créer les consultants par batch de 100
        batch_size = 100
        created = 0
        
        for batch_start in range(0, to_create, batch_size):
            batch_end = min(batch_start + batch_size, to_create)
            batch_count = batch_end - batch_start
            
            print(f"📝 Création batch {batch_start + 1}-{batch_end} ({batch_count} consultants)...")
            
            batch_consultants = []
            
            for i in range(batch_count):
                prenom = fake.first_name()
                nom = fake.last_name()
                
                # Générer un email unique
                base_name = f"{prenom.lower()}.{nom.lower()}".replace(' ', '').replace('-', '')
                email = generate_unique_email(base_name, existing_emails)
                
                consultant = Consultant(
                    prenom=prenom,
                    nom=nom,
                    email=email,
                    telephone=fake.phone_number(),
                    salaire_actuel=random.randint(35000, 80000),
                    practice_id=random.choice(practices).id if practices else None,
                    disponibilite=random.choice([True, False]),
                    notes=fake.text(max_nb_chars=100) if random.random() < 0.1 else None,
                    date_creation=fake.date_time_between(start_date='-2y', end_date='now'),
                    derniere_maj=fake.date_time_between(start_date='-6m', end_date='now')
                )
                
                batch_consultants.append(consultant)
                session.add(consultant)
            
            # Commit ce batch
            try:
                session.commit()
                created += batch_count
                print(f"✅ Batch committée: {batch_count} consultants ajoutés")
                
                # Assignation BM pour ce batch si disponibles
                if business_managers:
                    for consultant in batch_consultants:
                        if random.random() < 0.8:  # 80% ont un BM
                            bm = random.choice(business_managers)
                            date_debut = fake.date_between(start_date='-1y', end_date='now')
                            
                            cbm = ConsultantBusinessManager(
                                consultant=consultant,
                                business_manager=bm,
                                date_debut=date_debut,
                                date_fin=None if random.random() < 0.9 else fake.date_between(start_date=date_debut, end_date='now')
                            )
                            session.add(cbm)
                    
                    session.commit()
                    print(f"✅ Assignations BM committées pour ce batch")
                
            except Exception as e:
                print(f"❌ Erreur batch {batch_start}-{batch_end}: {e}")
                session.rollback()
                continue
        
        print(f"🎉 Création terminée: {created} nouveaux consultants ajoutés")
        
        # Vérification finale
        final_count = session.query(Consultant).count()
        print(f"📊 Total final: {final_count} consultants")

def add_missions_to_existing_consultants():
    """Ajoute des missions aux consultants existants"""
    print("🎯 Ajout de missions aux consultants existants...")
    
    from database.models import Mission
    
    CLIENTS = [
        "BNP Paribas", "Société Générale", "Crédit Agricole", "BPCE", "Orange", "SFR",
        "EDF", "Engie", "Airbus", "Thales", "Capgemini", "Atos", "SNCF", "Air France",
        "L'Oréal", "Danone", "Michelin", "La Poste", "RATP", "Veolia"
    ]
    
    with get_database_session() as session:
        consultants = session.query(Consultant).all()
        
        missions_created = 0
        
        for i, consultant in enumerate(consultants):
            if i % 100 == 0:
                print(f"  🎯 Missions pour consultant {i+1}/{len(consultants)}")
            
            # Chaque consultant a entre 8 et 15 missions
            nb_missions = random.randint(8, 15)
            
            for _ in range(nb_missions):
                # Dates de mission cohérentes
                date_debut = fake.date_between(start_date='-3y', end_date='now')
                
                # 70% de missions terminées, 30% en cours
                if random.random() < 0.7:
                    date_fin = fake.date_between(start_date=date_debut, end_date='now')
                    statut = 'terminee'
                else:
                    date_fin = None
                    statut = 'en_cours'
                
                client = random.choice(CLIENTS)
                
                mission = Mission(
                    consultant_id=consultant.id,
                    nom_mission=f"Mission {fake.word().title()} chez {client}",
                    client=client,
                    role=fake.job(),
                    date_debut=date_debut,
                    date_fin=date_fin,
                    statut=statut,
                    taux_journalier=random.randint(400, 1200),
                    revenus_generes=random.randint(5000, 50000) if date_fin else 0,
                    technologies_utilisees=', '.join([
                        random.choice(['Python', 'Java', 'JavaScript', 'React', 'Angular', 'SQL', 'Docker'])
                        for _ in range(random.randint(2, 5))
                    ]),
                    description=fake.text(max_nb_chars=200)
                )
                
                session.add(mission)
                missions_created += 1
            
            # Commit tous les 50 consultants
            if (i + 1) % 50 == 0:
                session.commit()
                print(f"✅ Missions committées pour les consultants 1-{i+1}")
        
        # Commit final
        session.commit()
        print(f"✅ {missions_created} missions créées au total")

if __name__ == "__main__":
    print("🚀 Génération rapide de données de test")
    print("=" * 50)
    
    try:
        # Initialisation
        init_database()
        
        # Ajouter des consultants
        add_consultants_batch(1000)
        
        # Ajouter des missions
        add_missions_to_existing_consultants()
        
        # Test final
        with get_database_session() as session:
            final_consultants = session.query(Consultant).count()
            from database.models import Mission
            final_missions = session.query(Mission).count()
            
            print("=" * 50)
            print("✅ GÉNÉRATION TERMINÉE")
            print(f"👥 Total consultants: {final_consultants}")
            print(f"🎯 Total missions: {final_missions}")
            print("=" * 50)
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
