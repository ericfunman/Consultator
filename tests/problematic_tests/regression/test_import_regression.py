"""
Tests de non-régression pour l'import VSA

Ce module teste spécifiquement les fonctionnalités d'import VSA
pour éviter les régressions comme le bug d'Eric LAPINA.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import pandas as pd
from datetime import date, datetime
import tempfile
import os

from app.database.models import Consultant, VSA_Mission
from app.database.database import get_session


class TestVSAImportRegression:
    """Tests de non-régression pour l'import VSA"""
    
    def test_mission_uniqueness_logic(self, db_session):
        """
        Test de non-régression : Bug Eric LAPINA
        
        Vérifie que les missions avec le même code mais différentes dates
        ne s'écrasent plus mutuellement.
        """
        # Given - Un consultant
        consultant = Consultant(
            nom='LAPINA', prenom='Eric',
            email='eric.lapina@test.com'
        )
        db_session.add(consultant)
        db_session.flush()
        
        # When - Import de plusieurs missions même code, dates différentes
        missions = [
            VSA_Mission(
                user_id=consultant.id,
                code='AFFAS263',
                orderid='ORD-2023-001',
                client_name='GENERALI VIE',
                date_debut=date(2023, 8, 21),
                date_fin=date(2023, 12, 31)
            ),
            VSA_Mission(
                user_id=consultant.id,
                code='AFFAS263',
                orderid='ORD-2024-001',
                client_name='GENERALI VIE',
                date_debut=date(2024, 1, 1),
                date_fin=date(2024, 12, 31)
            ),
            VSA_Mission(
                user_id=consultant.id,
                code='AFFAS263',
                orderid='ORD-2025-001',
                client_name='GENERALI VIE',
                date_debut=date(2025, 1, 1),
                date_fin=date(2025, 12, 31)
            )
        ]
        
        for mission in missions:
            db_session.add(mission)
        db_session.commit()
        
        # Then - Toutes les missions doivent être présentes
        saved_missions = db_session.query(VSA_Mission)\
            .filter_by(user_id=consultant.id, code='AFFAS263')\
            .order_by(VSA_Mission.date_debut)\
            .all()
        
        assert len(saved_missions) == 3, "Les 3 missions doivent être sauvées"
        
        # Vérification des dates spécifiques
        assert saved_missions[0].date_debut == date(2023, 8, 21)
        assert saved_missions[0].date_fin == date(2023, 12, 31)
        
        assert saved_missions[1].date_debut == date(2024, 1, 1)
        assert saved_missions[1].date_fin == date(2024, 12, 31)
        
        assert saved_missions[2].date_debut == date(2025, 1, 1)
        assert saved_missions[2].date_fin == date(2025, 12, 31)
    
    def test_duplicate_mission_detection(self, db_session):
        """Test que les missions avec des codes identiques peuvent être créées
        (pas de contrainte d'unicité sur le code)"""
        # Given - Un consultant
        consultant = Consultant(
            nom='DUPLICATE', prenom='Test',
            email='duplicate.test@test.com'
        )
        db_session.add(consultant)
        db_session.flush()
        
        # When - Ajout de missions avec le même code
        mission1 = VSA_Mission(
            user_id=consultant.id,
            code='DUPLICATE001',
            orderid="ORD-3329-359",
            client_name='CLIENT TEST',
            date_debut=date(2024, 1, 1),
            date_fin=date(2024, 12, 31)
        )
        
        mission2 = VSA_Mission(
            user_id=consultant.id,
            code='DUPLICATE001',
            orderid="ORD-9893-475",
            client_name='CLIENT TEST',
            date_debut=date(2024, 1, 1),
            date_fin=date(2024, 12, 31)
        )
        
        db_session.add(mission1)
        db_session.commit()
        
        # Then - Les deux missions sont créées sans erreur
        db_session.add(mission2)
        db_session.commit()
        
        # Vérifier que les deux missions existent
        missions = db_session.query(VSA_Mission).filter(
            VSA_Mission.code == 'DUPLICATE001'
        ).all()
        assert len(missions) == 2
    
    def test_mission_import_with_invalid_dates(self, db_session):
        """Test de gestion des dates invalides lors de l'import"""
        # Given - Un consultant
        consultant = Consultant(
            nom='DATETEST', prenom='Invalid',
            email='datetest.invalid@test.com'
        )
        db_session.add(consultant)
        db_session.flush()
        
        # When - Import avec date de fin avant date de début
        mission = VSA_Mission(
            user_id=consultant.id,
            code='INVALID_DATE',
                orderid="ORD-6105-310",
            client_name='CLIENT TEST',
            date_debut=date(2024, 12, 31),
            date_fin=date(2024, 1, 1)  # Date de fin avant début
        )
        
        # Then - La mission doit quand même être sauvée
        # (la validation métier se fait ailleurs)
        db_session.add(mission)
        db_session.commit()
        
        saved_mission = db_session.query(VSA_Mission)\
            .filter_by(user_id=consultant.id, code='INVALID_DATE')\
            .first()
        
        assert saved_mission is not None
    
    def test_bulk_mission_import_performance(self, db_session):
        """Test de performance pour l'import en masse"""
        import time
        
        # Given - Plusieurs consultants
        consultants = []
        for i in range(10):
            consultant = Consultant(
                nom=f'BULK{i:02d}',
                prenom=f'Import{i}',
                email=f'bulk.import{i}@test.com'
            )
            consultants.append(consultant)
        
        db_session.add_all(consultants)
        db_session.flush()
        
        # When - Import de nombreuses missions
        missions = []
        start_time = time.time()
        
        for consultant in consultants:
            for j in range(20):  # 20 missions par consultant
                mission = VSA_Mission(
                    user_id=consultant.id,
                    code=f'BULK{j:03d}',
                orderid="ORD-2211-237",
                    client_name=f'CLIENT {j}',
                    date_debut=date(2024, 1, 1),
                    date_fin=date(2024, 12, 31)
                )
                missions.append(mission)
        
        db_session.add_all(missions)
        db_session.commit()
        end_time = time.time()
        
        # Then - Vérification du temps et du nombre
        import_time = end_time - start_time
        assert import_time < 10.0, f"Import trop lent: {import_time:.2f}s"
        
        total_missions = db_session.query(VSA_Mission)\
            .filter(VSA_Mission.code.like('BULK%'))\
            .count()
        assert total_missions == 200  # 10 consultants × 20 missions
    
    def test_consultant_mission_relationship_integrity(self, db_session):
        """Test d'intégrité des relations consultant-mission"""
        # Given - Consultant avec missions VSA et normales
        consultant = Consultant(
            nom='RELATION', prenom='Test',
            email='relation.test@test.com'
        )
        db_session.add(consultant)
        db_session.flush()
        
        # Mission VSA
        vsa_mission = VSA_Mission(
            user_id=consultant.id,
            code='RELATION001',
                orderid="ORD-5147-542",
            client_name='CLIENT VSA',
            date_debut=date(2024, 1, 1),
            date_fin=date(2024, 6, 30)
        )
        
        # When - Suppression du consultant
        db_session.add(vsa_mission)
        db_session.commit()
        
        missions_before = db_session.query(VSA_Mission)\
            .filter_by(user_id=consultant.id)\
            .count()
        assert missions_before == 1
        
        db_session.delete(consultant)
        db_session.commit()
        
        # Then - Les missions VSA doivent être supprimées en cascade
        missions_after = db_session.query(VSA_Mission)\
            .filter_by(user_id=consultant.id)\
            .count()
        assert missions_after == 0
    
    def test_mission_data_completeness(self, db_session):
        """Test de complétude des données de mission"""
        # Given - Un consultant
        consultant = Consultant(
            nom='COMPLETE', prenom='Data',
            email='complete.data@test.com'
        )
        db_session.add(consultant)
        db_session.flush()
        
        # When - Mission avec données complètes
        mission = VSA_Mission(
            user_id=consultant.id,
            code='COMPLETE001',
                orderid="ORD-5546-649",
            client_name='CLIENT COMPLET',
            date_debut=date(2024, 1, 1),
            date_fin=date(2024, 12, 31),
            tjm=600.0,
            description='Mission complète avec toutes les données'
        )
        
        db_session.add(mission)
        db_session.commit()
        
        # Then - Toutes les données doivent être présentes
        saved_mission = db_session.query(VSA_Mission)\
            .filter_by(user_id=consultant.id, code='COMPLETE001')\
            .first()
        
        assert saved_mission.client_name == 'CLIENT COMPLET'
        assert saved_mission.tjm == 600.0
        assert saved_mission.description == 'Mission complète avec toutes les données'
        assert saved_mission.date_debut is not None
        assert saved_mission.date_fin is not None
    
    def test_mission_search_and_filtering(self, db_session):
        """Test de recherche et filtrage des missions"""
        # Given - Consultant avec plusieurs missions
        consultant = Consultant(
            nom='SEARCH', prenom='Filter',
            email='search.filter@test.com'
        )
        db_session.add(consultant)
        db_session.flush()
        
        missions_data = [
            ('SEARCH001', 'BANQUE POPULAIRE', date(2023, 1, 1), date(2023, 12, 31)),
            ('SEARCH002', 'SOCIETE GENERALE', date(2024, 1, 1), date(2024, 12, 31)),
            ('SEARCH003', 'BNP PARIBAS', date(2024, 6, 1), date(2024, 12, 31)),
        ]
        
        for code, client, debut, fin in missions_data:
            mission = VSA_Mission(
                user_id=consultant.id,
                code=code,
                orderid="ORD-6263-377",
                client_name=client,
                date_debut=debut,
                date_fin=fin
            )
            db_session.add(mission)
        
        db_session.commit()
        
        # When/Then - Tests de recherche
        # Recherche par client
        banque_missions = db_session.query(VSA_Mission)\
            .filter(VSA_Mission.client_name.like('%BANQUE%'))\
            .all()
        assert len(banque_missions) == 1
        assert banque_missions[0].code == 'SEARCH001'
        
        # Recherche par année
        missions_2024 = db_session.query(VSA_Mission)\
            .filter(VSA_Mission.date_debut >= date(2024, 1, 1))\
            .filter(VSA_Mission.date_debut < date(2025, 1, 1))\
            .all()
        assert len(missions_2024) == 2
        
        # Recherche par code
        search002 = db_session.query(VSA_Mission)\
            .filter_by(code='SEARCH002')\
            .first()
        assert search002 is not None
        assert search002.client_name == 'SOCIETE GENERALE'


class TestImportDataValidation:
    """Tests de validation des données d'import"""
    
    def test_consultant_mapping_validation(self, db_session):
        """Test de validation du mapping consultant"""
        # Given - Données de mapping incohérentes
        consultant = Consultant(
            nom='MAPPING', prenom='Test',
            email='mapping.test@test.com'
        )
        db_session.add(consultant)
        db_session.flush()
        
        # When - Mission avec user_id incorrect
        mission = VSA_Mission(
            user_id=99999,  # ID inexistant
            code='MAPPING001',
            orderid='ORD-MAPPING-001',
            client_name='CLIENT TEST',
            date_debut=date(2024, 1, 1)
        )
        
        # Then - Doit échouer avec contrainte FK
        db_session.add(mission)
        with pytest.raises(Exception):
            db_session.commit()
    
    def test_date_format_consistency(self, db_session):
        """Test de cohérence des formats de date"""
        # Given - Un consultant
        consultant = Consultant(
            nom='DATEFORMAT', prenom='Test',
            email='dateformat.test@test.com'
        )
        db_session.add(consultant)
        db_session.flush()
        
        # When - Mission avec différents formats de date
        mission = VSA_Mission(
            user_id=consultant.id,
            code='DATE001',
                orderid="ORD-5272-144",
            client_name='CLIENT DATE',
            date_debut=date(2024, 1, 15),
            date_fin=date(2024, 12, 31)
        )
        
        db_session.add(mission)
        db_session.commit()
        
        # Then - Les dates doivent être cohérentes
        saved_mission = db_session.query(VSA_Mission)\
            .filter_by(code='DATE001')\
            .first()
        
        assert isinstance(saved_mission.date_debut, date)
        assert isinstance(saved_mission.date_fin, date)
        assert saved_mission.date_debut <= saved_mission.date_fin