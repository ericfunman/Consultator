"""
Tests pour les modèles de base de données
"""

from datetime import date
from datetime import datetime
from datetime import timedelta
from unittest.mock import Mock
from unittest.mock import patch

import pytest

from app.database.models import CV
from app.database.models import BusinessManager
from app.database.models import Competence
from app.database.models import Consultant
from app.database.models import ConsultantBusinessManager
from app.database.models import ConsultantCompetence
from app.database.models import ConsultantLangue
from app.database.models import ConsultantSalaire
from app.database.models import CustomTechnology
from app.database.models import Langue
from app.database.models import Mission
from app.database.models import Practice


class TestPracticeModel:
    """Tests pour le modèle Practice"""

    def test_practice_creation(self):
        """Test de création d'une practice"""
        practice = Practice(
            nom="Data Science",
            description="Practice spécialisée en data science",
            responsable="Jean Dupont",
            actif=True,
        )

        assert practice.nom == "Data Science"
        assert practice.description == "Practice spécialisée en data science"
        assert practice.responsable == "Jean Dupont"
        assert practice.actif is True

    def test_practice_repr(self):
        """Test de la représentation string"""
        practice = Practice(id=1, nom="Data Science")
        assert repr(practice) == "<Practice(id=1, nom='Data Science')>"

    def test_practice_nombre_consultants(self):
        """Test de la propriété nombre_consultants"""
        practice = Practice()

        # Créer des objets Consultant réels pour le test
        consultant1 = Consultant(
            nom="Dupont", prenom="Jean", email="jean@test.com", disponibilite=True
        )
        consultant2 = Consultant(
            nom="Martin", prenom="Marie", email="marie@test.com", disponibilite=False
        )
        consultant3 = Consultant(
            nom="Bernard", prenom="Pierre", email="pierre@test.com", disponibilite=True
        )

        # Simuler la relation
        practice.consultants = [consultant1, consultant2, consultant3]

        assert practice.nombre_consultants == 2


class TestConsultantModel:
    """Tests pour le modèle Consultant"""

    def test_consultant_creation(self):
        """Test de création d'un consultant"""
        consultant = Consultant(
            nom="Dupont",
            prenom="Jean",
            email="jean.dupont@email.com",
            telephone="0123456789",
            salaire_actuel=45000.0,
            disponibilite=True,
            societe="Quanteam",
            grade="Senior",
            type_contrat="CDI",
        )

        assert consultant.nom == "Dupont"
        assert consultant.prenom == "Jean"
        assert consultant.email == "jean.dupont@email.com"
        assert consultant.nom_complet == "Jean Dupont"
        assert consultant.salaire_actuel == 45000.0
        assert consultant.disponibilite is True

    def test_consultant_repr(self):
        """Test de la représentation string"""
        consultant = Consultant(id=1, nom="Dupont", prenom="Jean")
        assert repr(consultant) == "<Consultant(id=1, nom='Dupont', prenom='Jean')>"

    def test_consultant_nom_complet(self):
        """Test de la propriété nom_complet"""
        consultant = Consultant(prenom="Jean", nom="Dupont")
        assert consultant.nom_complet == "Jean Dupont"

    def test_consultant_experience_annees_no_date(self):
        """Test de experience_annees sans date de première mission"""
        consultant = Consultant()
        assert consultant.experience_annees == 0

    def test_consultant_experience_annees_with_date(self):
        """Test de experience_annees avec date de première mission"""
        consultant = Consultant()
        # Simuler une date 2 ans dans le passé
        past_date = date.today().replace(year=date.today().year - 2)
        consultant.date_premiere_mission = past_date

        experience = consultant.experience_annees
        assert 1.9 <= experience <= 2.1  # Tolérance pour les années bissextiles

    def test_consultant_statut_societe_en_poste(self):
        """Test de statut_societe pour un consultant en poste"""
        consultant = Consultant()
        assert consultant.statut_societe == "En poste"

    def test_consultant_statut_societe_depart_prevu(self):
        """Test de statut_societe pour un départ prévu"""
        consultant = Consultant()
        future_date = date.today().replace(year=date.today().year + 1)
        consultant.date_sortie_societe = future_date
        assert consultant.statut_societe == "Départ prévu"

    def test_consultant_statut_societe_parti(self):
        """Test de statut_societe pour un consultant parti"""
        consultant = Consultant()
        past_date = date.today().replace(year=date.today().year - 1)
        consultant.date_sortie_societe = past_date
        assert consultant.statut_societe == "Parti"

    def test_consultant_date_disponibilite_asap(self):
        """Test de date_disponibilite quand disponible"""
        consultant = Consultant(disponibilite=True)
        assert consultant.date_disponibilite == "ASAP"

    def test_consultant_date_disponibilite_with_missions(self):
        """Test de date_disponibilite avec missions futures"""
        consultant = Consultant(disponibilite=False)

        # Mock des missions avec des dates valides
        mission1 = Mock()
        mission1.date_fin = date.today() + timedelta(days=30)
        mission1._sa_instance_state = Mock()
        mission1._sa_instance_state.manager = {"consultant": Mock(impl=Mock())}
        mission1._sa_instance_state.parents = {}

        mission2 = Mock()
        mission2.date_fin = date.today() + timedelta(days=60)
        mission2._sa_instance_state = Mock()
        mission2._sa_instance_state.manager = {"consultant": Mock(impl=Mock())}
        mission2._sa_instance_state.parents = {}

        # Patcher directement la propriété missions
        with patch.object(consultant, "missions", [mission1, mission2]):
            # Devrait retourner la date la plus tardive
            expected_date = mission2.date_fin.strftime("%d/%m/%Y")
            assert consultant.date_disponibilite == expected_date

    def test_consultant_business_manager_actuel(self):
        """Test de business_manager_actuel"""
        consultant = Consultant()

        # Mock des gestions BM
        gestion1 = Mock()
        gestion1.date_fin = None
        gestion1.business_manager = "BM Actuel"
        gestion1._sa_instance_state = Mock()
        gestion1._sa_instance_state.manager = {"consultant": Mock(impl=Mock())}
        gestion1._sa_instance_state.parents = {}

        gestion2 = Mock()
        gestion2.date_fin = date.today()
        gestion2.business_manager = "Ancien BM"
        gestion2._sa_instance_state = Mock()
        gestion2._sa_instance_state.manager = {"consultant": Mock(impl=Mock())}
        gestion2._sa_instance_state.parents = {}

        # Patcher directement la propriété business_manager_gestions
        with patch.object(
            consultant, "business_manager_gestions", [gestion1, gestion2]
        ):
            assert consultant.business_manager_actuel == "BM Actuel"


class TestCompetenceModel:
    """Tests pour le modèle Competence"""

    def test_competence_creation(self):
        """Test de création d'une compétence"""
        competence = Competence(
            nom="Python",
            categorie="Langages de programmation",
            type_competence="technique",
            description="Langage de programmation Python",
            niveau_requis="senior",
        )

        assert competence.nom == "Python"
        assert competence.categorie == "Langages de programmation"
        assert competence.type_competence == "technique"
        assert competence.niveau_requis == "senior"

    def test_competence_repr(self):
        """Test de la représentation string"""
        competence = Competence(id=1, nom="Python", categorie="Backend")
        assert (
            repr(competence) == "<Competence(id=1, nom='Python', categorie='Backend')>"
        )


class TestMissionModel:
    """Tests pour le modèle Mission"""

    def test_mission_creation(self):
        """Test de création d'une mission"""
        mission = Mission(
            consultant_id=1,
            nom_mission="Projet Data Science",
            client="Client ABC",
            role="Data Scientist",
            date_debut=date(2024, 1, 1),
            date_fin=date(2024, 6, 30),
            statut="terminee",
            tjm=650.0,
            technologies_utilisees="Python, TensorFlow, AWS",
        )

        assert mission.nom_mission == "Projet Data Science"
        assert mission.client == "Client ABC"
        assert mission.tjm == 650.0
        assert mission.statut == "terminee"

    def test_mission_repr(self):
        """Test de la représentation string"""
        mission = Mission(id=1, nom_mission="Projet ABC", client="Client XYZ")
        expected = "<Mission(id=1, nom='Projet ABC', client='Client XYZ')>"
        assert repr(mission) == expected

    def test_mission_duree_jours(self):
        """Test de la propriété duree_jours"""
        mission = Mission()
        mission.date_debut = date(2024, 1, 1)
        mission.date_fin = date(2024, 1, 31)

        assert mission.duree_jours == 30

    def test_mission_duree_jours_no_dates(self):
        """Test de duree_jours sans dates"""
        mission = Mission()
        assert mission.duree_jours is None


class TestCVModel:
    """Tests pour le modèle CV"""

    def test_cv_creation(self):
        """Test de création d'un CV"""
        cv = CV(
            consultant_id=1,
            fichier_nom="cv_jean_dupont.pdf",
            fichier_path="/uploads/cv_jean_dupont.pdf",
            contenu_extrait="Contenu du CV...",
            taille_fichier=1024000,
        )

        assert cv.fichier_nom == "cv_jean_dupont.pdf"
        assert cv.taille_fichier == 1024000

    def test_cv_repr(self):
        """Test de la représentation string"""
        cv = CV(id=1, consultant_id=1, fichier_nom="cv.pdf")
        assert repr(cv) == "<CV(id=1, consultant_id=1, fichier='cv.pdf')>"


class TestCustomTechnologyModel:
    """Tests pour le modèle CustomTechnology"""

    def test_custom_technology_creation(self):
        """Test de création d'une technologie personnalisée"""
        tech = CustomTechnology(
            nom="FrameworkXYZ",
            categorie="Frameworks Web",
            description="Framework personnalisé",
        )

        assert tech.nom == "FrameworkXYZ"
        assert tech.categorie == "Frameworks Web"

    def test_custom_technology_repr(self):
        """Test de la représentation string"""
        tech = CustomTechnology(id=1, nom="TechX", categorie="Custom")
        assert repr(tech) == "<CustomTechnology(id=1, nom='TechX', categorie='Custom')>"


class TestConsultantSalaireModel:
    """Tests pour le modèle ConsultantSalaire"""

    def test_consultant_salaire_creation(self):
        """Test de création d'un salaire"""
        salaire = ConsultantSalaire(
            consultant_id=1,
            salaire=50000.0,
            date_debut=date(2024, 1, 1),
            commentaire="Augmentation annuelle",
        )

        assert salaire.salaire == 50000.0
        assert salaire.commentaire == "Augmentation annuelle"

    def test_consultant_salaire_repr(self):
        """Test de la représentation string"""
        salaire = ConsultantSalaire(
            id=1, consultant_id=1, salaire=45000.0, date_debut=date(2024, 1, 1)
        )
        expected = "<ConsultantSalaire(id=1, consultant_id=1, salaire=45000.0, date_debut=2024-01-01)>"
        assert repr(salaire) == expected


class TestLangueModel:
    """Tests pour le modèle Langue"""

    def test_langue_creation(self):
        """Test de création d'une langue"""
        langue = Langue(nom="Français", code_iso="FR", description="Langue française")

        assert langue.nom == "Français"
        assert langue.code_iso == "FR"

    def test_langue_repr(self):
        """Test de la représentation string"""
        langue = Langue(id=1, nom="Français", code_iso="FR")
        assert repr(langue) == "<Langue(id=1, nom='Français', code_iso='FR')>"


class TestConsultantLangueModel:
    """Tests pour le modèle ConsultantLangue"""

    def test_consultant_langue_creation(self):
        """Test de création d'une langue consultant"""
        consultant_langue = ConsultantLangue(
            consultant_id=1, langue_id=1, niveau=4, commentaire="Certification TOEIC"
        )

        assert consultant_langue.niveau == 4
        assert consultant_langue.commentaire == "Certification TOEIC"

    def test_consultant_langue_repr(self):
        """Test de la représentation string"""
        consultant_langue = ConsultantLangue(consultant_id=1, langue_id=1, niveau=3)
        assert (
            repr(consultant_langue)
            == "<ConsultantLangue(consultant_id=1, langue_id=1, niveau=3)>"
        )

    def test_consultant_langue_niveau_label(self):
        """Test de la propriété niveau_label"""
        consultant_langue = ConsultantLangue(niveau=3)
        assert consultant_langue.niveau_label == "Intermédiaire (B1-B2)"

        consultant_langue.niveau = 5
        assert consultant_langue.niveau_label == "Natif (C2)"

        consultant_langue.niveau = 99
        assert consultant_langue.niveau_label == "Inconnu"


class TestBusinessManagerModel:
    """Tests pour le modèle BusinessManager"""

    def test_business_manager_creation(self):
        """Test de création d'un Business Manager"""
        bm = BusinessManager(
            nom="Dubois",
            prenom="Marie",
            email="marie.dubois@email.com",
            telephone="0123456789",
            actif=True,
        )

        assert bm.nom == "Dubois"
        assert bm.prenom == "Marie"
        assert bm.nom_complet == "Marie Dubois"

    def test_business_manager_repr(self):
        """Test de la représentation string"""
        bm = BusinessManager(id=1, nom="Dubois", prenom="Marie")
        expected = "<BusinessManager(id=1, nom='Dubois', prenom='Marie')>"
        assert repr(bm) == expected

    def test_business_manager_nom_complet(self):
        """Test de la propriété nom_complet"""
        bm = BusinessManager(prenom="Marie", nom="Dubois")
        assert bm.nom_complet == "Marie Dubois"

    def test_business_manager_consultants_actuels(self):
        """Test de la propriété consultants_actuels"""
        bm = BusinessManager()

        # Mock des gestions
        gestion1 = Mock()
        gestion1.date_fin = None
        gestion1.consultant = "Consultant Actif"
        gestion1._sa_instance_state = Mock()
        gestion1._sa_instance_state.manager = {"business_manager": Mock(impl=Mock())}
        gestion1._sa_instance_state.parents = {}

        gestion2 = Mock()
        gestion2.date_fin = date.today()
        gestion2.consultant = "Consultant Inactif"
        gestion2._sa_instance_state = Mock()
        gestion2._sa_instance_state.manager = {"business_manager": Mock(impl=Mock())}
        gestion2._sa_instance_state.parents = {}

        # Patcher directement la propriété consultant_gestions
        with patch.object(bm, "consultant_gestions", [gestion1, gestion2]):
            consultants = bm.consultants_actuels
            assert len(consultants) == 1
            assert consultants[0] == "Consultant Actif"

    def test_business_manager_nombre_consultants_actuels(self):
        """Test de la propriété nombre_consultants_actuels"""
        bm = BusinessManager()

        # Mock des gestions
        gestion1 = Mock()
        gestion1.date_fin = None
        gestion1._sa_instance_state = Mock()
        gestion1._sa_instance_state.manager = {"business_manager": Mock(impl=Mock())}
        gestion1._sa_instance_state.parents = {}

        gestion2 = Mock()
        gestion2.date_fin = None
        gestion2._sa_instance_state = Mock()
        gestion2._sa_instance_state.manager = {"business_manager": Mock(impl=Mock())}
        gestion2._sa_instance_state.parents = {}

        gestion3 = Mock()
        gestion3.date_fin = date.today()
        gestion3._sa_instance_state = Mock()
        gestion3._sa_instance_state.manager = {"business_manager": Mock(impl=Mock())}
        gestion3._sa_instance_state.parents = {}

        # Patcher directement la propriété consultant_gestions
        with patch.object(bm, "consultant_gestions", [gestion1, gestion2, gestion3]):
            assert bm.nombre_consultants_actuels == 2


class TestConsultantBusinessManagerModel:
    """Tests pour le modèle ConsultantBusinessManager"""

    def test_consultant_business_manager_creation(self):
        """Test de création d'une gestion consultant-BM"""
        gestion = ConsultantBusinessManager(
            consultant_id=1,
            business_manager_id=1,
            date_debut=date(2024, 1, 1),
            commentaire="Nouvelle affectation",
        )

        assert gestion.consultant_id == 1
        assert gestion.business_manager_id == 1
        assert gestion.commentaire == "Nouvelle affectation"

    def test_consultant_business_manager_repr(self):
        """Test de la représentation string"""
        gestion = ConsultantBusinessManager(
            consultant_id=1, business_manager_id=1, date_debut=date(2024, 1, 1)
        )
        expected = (
            "<ConsultantBusinessManager(consultant_id=1, bm_id=1, debut=2024-01-01)>"
        )
        assert repr(gestion) == expected

    def test_consultant_business_manager_est_actuel(self):
        """Test de la propriété est_actuel"""
        gestion = ConsultantBusinessManager()
        assert gestion.est_actuel is True  # date_fin is None

        gestion.date_fin = date.today()
        assert gestion.est_actuel is False

    def test_consultant_business_manager_duree_jours(self):
        """Test de la propriété duree_jours"""
        gestion = ConsultantBusinessManager()
        gestion.date_debut = date(2024, 1, 1)
        gestion.date_fin = date(2024, 1, 31)

        assert gestion.duree_jours == 30

    def test_consultant_business_manager_duree_jours_active(self):
        """Test de duree_jours pour une gestion active"""
        gestion = ConsultantBusinessManager()
        gestion.date_debut = date.today() - timedelta(
            days=10
        )  # Utiliser timedelta pour éviter les erreurs de date
        gestion.date_fin = None  # Gestion active

        # Devrait utiliser la date actuelle
        duree = gestion.duree_jours
        assert duree >= 10  # Au moins 10 jours
