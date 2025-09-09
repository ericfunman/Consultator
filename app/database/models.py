"""
Modèles de base de données pour Consultator
Définit la structure des tables avec SQLAlchemy
Optimisé pour gérer 1000+ consultants avec index de performance
"""

from datetime import date
from datetime import datetime
from typing import TYPE_CHECKING
from typing import List
from typing import Optional

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Index
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    from typing import Any

Base = declarative_base()


class Practice(Base):
    """Modèle pour les practices (Data, Quant, etc.)"""

    __tablename__ = "practices"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    nom: Mapped[str] = Column(String(100), unique=True, nullable=False)
    description: Mapped[Optional[str]] = Column(Text)
    responsable: Mapped[Optional[str]] = Column(
        String(200)
    )  # Nom du responsable de practice
    date_creation: Mapped[datetime] = Column(DateTime, default=datetime.now)
    actif: Mapped[bool] = Column(Boolean, default=True)

    # Relations
    consultants: Mapped[List["Consultant"]] = relationship(
        "Consultant", back_populates="practice"
    )

    def __repr__(self) -> str:
        return f"<Practice(id={self.id}, nom='{self.nom}')>"

    @property
    def nombre_consultants(self) -> int:
        """Retourne le nombre de consultants dans cette practice"""
        return len([c for c in self.consultants if c.disponibilite])


class Consultant(Base):
    """Modèle pour les consultants avec optimisations de performance"""

    __tablename__ = "consultants"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    nom: Mapped[str] = Column(String(100), nullable=False)
    prenom: Mapped[str] = Column(String(100), nullable=False)
    email: Mapped[str] = Column(String(255), unique=True, nullable=False)
    telephone: Mapped[Optional[str]] = Column(String(20))
    salaire_actuel: Mapped[Optional[float]] = Column(Float)
    date_creation: Mapped[datetime] = Column(DateTime, default=datetime.now)
    derniere_maj: Mapped[datetime] = Column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )
    disponibilite: Mapped[bool] = Column(Boolean, default=True)
    notes: Mapped[Optional[str]] = Column(Text)

    # Nouveaux champs pour l'historique société V1.2
    date_entree_societe: Mapped[Optional[datetime.date]] = Column(
        Date
    )  # Date d'entrée dans la société
    date_sortie_societe: Mapped[Optional[datetime.date]] = Column(Date)
    societe: Mapped[str] = Column(String(50), default="Quanteam")  # Quanteam ou Asigma
    date_premiere_mission: Mapped[Optional[datetime.date]] = Column(
        Date
    )  # Date de la première mission

    # Nouveaux champs pour grade et contrat V1.2.1
    # Junior, Confirmé, Consultant Manager, Directeur de Practice
    grade: Mapped[str] = Column(String(50), default="Junior")
    # CDI, CDD, Stagiaire, Alternant, Indépendant
    type_contrat: Mapped[str] = Column(String(20), default="CDI")

    # Relations
    practice_id: Mapped[Optional[int]] = Column(Integer, ForeignKey("practices.id"))
    practice: Mapped[Optional["Practice"]] = relationship(
        "Practice", back_populates="consultants"
    )
    competences: Mapped[List["ConsultantCompetence"]] = relationship(
        "ConsultantCompetence",
        back_populates="consultant",
        cascade="all, delete-orphan",
    )
    missions: Mapped[List["Mission"]] = relationship(
        "Mission", back_populates="consultant", cascade="all, delete-orphan"
    )
    cvs: Mapped[List["CV"]] = relationship(
        "CV", back_populates="consultant", cascade="all, delete-orphan"
    )
    salaires: Mapped[List["ConsultantSalaire"]] = relationship(
        "ConsultantSalaire", back_populates="consultant", cascade="all, delete-orphan"
    )
    langues: Mapped[List["ConsultantLangue"]] = relationship(
        "ConsultantLangue", back_populates="consultant", cascade="all, delete-orphan"
    )
    business_manager_gestions: Mapped[List["ConsultantBusinessManager"]] = relationship(
        "ConsultantBusinessManager",
        back_populates="consultant",
        cascade="all, delete-orphan",
    )

    # Index de performance pour recherches rapides
    __table_args__ = (
        Index("idx_consultant_nom_prenom", "nom", "prenom"),
        Index("idx_consultant_email", "email"),
        Index("idx_consultant_disponibilite", "disponibilite"),
        Index("idx_consultant_practice", "practice_id"),
        Index("idx_consultant_date_maj", "derniere_maj"),
    )

    def __repr__(self) -> str:
        return f"<Consultant(id={self.id}, nom='{self.nom}', prenom='{self.prenom}')>"

    @property
    def nom_complet(self) -> str:
        return f"{self.prenom} {self.nom}"

    @property
    def business_manager_actuel(self) -> Optional["BusinessManager"]:
        """Retourne le Business Manager actuel du consultant"""
        for cbm in self.business_manager_gestions:
            if cbm.date_fin is None:
                return cbm.business_manager
        return None

    @property
    def experience_annees(self) -> float:
        """Calcule l'expérience en années depuis la première mission"""
        if not self.date_premiere_mission:
            return 0

        today = date.today()
        delta = today - self.date_premiere_mission
        return round(delta.days / 365.25, 1)  # Prise en compte des années bissextiles

    @property
    def statut_societe(self) -> str:
        """Retourne le statut actuel dans la société"""
        if not self.date_sortie_societe:
            return "En poste"

        if self.date_sortie_societe > date.today():
            return "Départ prévu"
        else:
            return "Parti"

    @property
    def date_disponibilite(self) -> str:
        """
        Calcule la date de disponibilité du consultant
        - Si disponible immédiatement: 'ASAP'
        - Sinon: date de fin de la mission la plus tardive (si > aujourd'hui)
        """

        # Si marqué comme disponible, retour ASAP
        if self.disponibilite:
            return "ASAP"

        # Chercher la date de fin de mission la plus tardive
        today = date.today()
        max_date_fin: Optional[datetime.date] = None

        for mission in self.missions:
            if mission.date_fin and mission.date_fin > today:
                if max_date_fin is None or mission.date_fin > max_date_fin:
                    max_date_fin = mission.date_fin

        if max_date_fin:
            return max_date_fin.strftime("%d/%m/%Y")
        else:
            # Aucune mission avec date de fin future, donc ASAP
            return "ASAP"


class Competence(Base):
    """Modèle pour les compétences techniques et fonctionnelles"""

    __tablename__ = "competences"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    nom: Mapped[str] = Column(String(100), unique=True, nullable=False)
    # Frontend, Backend, Data, Cloud, etc.
    categorie: Mapped[str] = Column(String(50), nullable=False)
    # technique ou fonctionnelle
    type_competence: Mapped[str] = Column(String(20), default="technique")
    description: Mapped[Optional[str]] = Column(Text)
    niveau_requis: Mapped[str] = Column(
        String(20), default="junior"
    )  # junior, medior, senior

    # Relations
    consultant_competences: Mapped[List["ConsultantCompetence"]] = relationship(
        "ConsultantCompetence", back_populates="competence"
    )

    def __repr__(self) -> str:
        return f"<Competence(id={self.id}, nom='{self.nom}', categorie='{self.categorie}')>"


class ConsultantCompetence(Base):
    """Table de liaison entre consultants et compétences"""

    __tablename__ = "consultant_competences"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    consultant_id: Mapped[int] = Column(
        Integer, ForeignKey("consultants.id"), nullable=False
    )
    competence_id: Mapped[int] = Column(
        Integer, ForeignKey("competences.id"), nullable=False
    )
    annees_experience: Mapped[float] = Column(Float, default=0.0)
    # debutant, intermediaire, expert
    niveau_maitrise: Mapped[str] = Column(String(20), default="debutant")
    certifications: Mapped[Optional[str]] = Column(Text)  # JSON ou texte simple
    projets_realises: Mapped[Optional[str]] = Column(Text)
    date_ajout: Mapped[datetime] = Column(DateTime, default=datetime.now)

    # Relations
    consultant: Mapped["Consultant"] = relationship(
        "Consultant", back_populates="competences"
    )
    competence: Mapped["Competence"] = relationship(
        "Competence", back_populates="consultant_competences"
    )

    def __repr__(self) -> str:
        return f"<ConsultantCompetence(consultant_id={self.consultant_id}, competence_id={self.competence_id}, experience={self.annees_experience})>"


class Mission(Base):
    """Modèle pour les missions des consultants avec optimisations"""

    __tablename__ = "missions"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    consultant_id: Mapped[int] = Column(
        Integer, ForeignKey("consultants.id"), nullable=False
    )
    nom_mission: Mapped[str] = Column(String(200), nullable=False)
    client: Mapped[str] = Column(String(200), nullable=False)
    role: Mapped[Optional[str]] = Column(
        String(300)
    )  # Nouveau champ pour le rôle/poste
    date_debut: Mapped[datetime.date] = Column(Date, nullable=False)
    date_fin: Mapped[Optional[datetime.date]] = Column(Date)
    statut: Mapped[str] = Column(
        String(20), default="en_cours"
    )  # en_cours, terminee, suspendue
    taux_journalier: Mapped[Optional[float]] = Column(
        Float
    )  # Ancien champ, conservé pour compatibilité
    tjm: Mapped[Optional[float]] = Column(
        Float
    )  # Nouveau champ TJM spécifique mission V1.2.2
    revenus_generes: Mapped[Optional[float]] = Column(Float)
    technologies_utilisees: Mapped[Optional[str]] = Column(
        Text
    )  # JSON ou texte séparé par virgules
    description: Mapped[Optional[str]] = Column(Text)

    # Relations
    consultant: Mapped["Consultant"] = relationship(
        "Consultant", back_populates="missions"
    )

    # Index de performance pour requêtes fréquentes
    __table_args__ = (
        Index("idx_mission_consultant", "consultant_id"),
        Index("idx_mission_client", "client"),
        Index("idx_mission_statut", "statut"),
        Index("idx_mission_dates", "date_debut", "date_fin"),
        Index("idx_mission_consultant_dates", "consultant_id", "date_debut"),
    )

    def __repr__(self) -> str:
        return (
            f"<Mission(id={self.id}, nom='{self.nom_mission}', client='{self.client}')>"
        )

    @property
    def duree_jours(self) -> Optional[int]:
        """Calcule la durée de la mission en jours"""
        if self.date_fin and self.date_debut:
            return (self.date_fin - self.date_debut).days
        return None


class CV(Base):
    """Modèle pour les CVs uploadés"""

    __tablename__ = "cvs"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    consultant_id: Mapped[int] = Column(
        Integer, ForeignKey("consultants.id"), nullable=False
    )
    fichier_nom: Mapped[str] = Column(String(255), nullable=False)
    fichier_path: Mapped[str] = Column(String(500), nullable=False)
    contenu_extrait: Mapped[Optional[str]] = Column(Text)  # Contenu parsé du CV
    date_upload: Mapped[datetime] = Column(DateTime, default=datetime.now)
    taille_fichier: Mapped[Optional[int]] = Column(Integer)  # en bytes

    # Relations
    consultant: Mapped["Consultant"] = relationship("Consultant", back_populates="cvs")

    def __repr__(self) -> str:
        return f"<CV(id={self.id}, consultant_id={self.consultant_id}, fichier='{self.fichier_nom}')>"


class CustomTechnology(Base):
    """Modèle pour les technologies personnalisées"""

    __tablename__ = "custom_technologies"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    nom: Mapped[str] = Column(String(100), nullable=False, unique=True)
    categorie: Mapped[str] = Column(
        String(100), nullable=False, default="Personnalisées"
    )
    description: Mapped[Optional[str]] = Column(Text)
    date_creation: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<CustomTechnology(id={self.id}, nom='{self.nom}', categorie='{self.categorie}')>"


class ConsultantSalaire(Base):
    """Historique des salaires d'un consultant"""

    __tablename__ = "consultant_salaires"
    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    consultant_id: Mapped[int] = Column(
        Integer, ForeignKey("consultants.id"), nullable=False
    )
    salaire: Mapped[float] = Column(Float, nullable=False)
    date_debut: Mapped[datetime.date] = Column(
        Date, nullable=False, default=datetime.now
    )
    date_fin: Mapped[Optional[datetime.date]] = Column(Date)
    commentaire: Mapped[Optional[str]] = Column(Text)
    consultant: Mapped["Consultant"] = relationship(
        "Consultant", back_populates="salaires"
    )

    def __repr__(self) -> str:
        return f"<ConsultantSalaire(id={self.id}, consultant_id={self.consultant_id}, salaire={self.salaire}, date_debut={self.date_debut})>"


class Langue(Base):
    """Modèle pour les langues"""

    __tablename__ = "langues"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    nom: Mapped[str] = Column(String(100), nullable=False, unique=True)
    code_iso: Mapped[Optional[str]] = Column(String(5))  # ex: FR, EN, ES, DE, IT
    description: Mapped[Optional[str]] = Column(Text)

    # Relations
    consultant_langues: Mapped[List["ConsultantLangue"]] = relationship(
        "ConsultantLangue", back_populates="langue"
    )

    def __repr__(self) -> str:
        return f"<Langue(id={self.id}, nom='{self.nom}', code_iso='{self.code_iso}')>"


class ConsultantLangue(Base):
    """Table de liaison entre consultants et langues avec niveau"""

    __tablename__ = "consultant_langues"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    consultant_id: Mapped[int] = Column(
        Integer, ForeignKey("consultants.id"), nullable=False
    )
    langue_id: Mapped[int] = Column(Integer, ForeignKey("langues.id"), nullable=False)
    # 1=Débutant, 2=Élémentaire, 3=Intermédiaire, 4=Avancé, 5=Natif
    niveau: Mapped[int] = Column(Integer, nullable=False)
    # ex: "Lu, écrit, parlé", "Certification TOEIC 850", etc.
    commentaire: Mapped[Optional[str]] = Column(Text)
    date_ajout: Mapped[datetime] = Column(DateTime, default=datetime.now)

    # Relations
    consultant: Mapped["Consultant"] = relationship(
        "Consultant", back_populates="langues"
    )
    langue: Mapped["Langue"] = relationship(
        "Langue", back_populates="consultant_langues"
    )

    def __repr__(self) -> str:
        return f"<ConsultantLangue(consultant_id={self.consultant_id}, langue_id={self.langue_id}, niveau={self.niveau})>"

    @property
    def niveau_label(self) -> str:
        """Retourne le label du niveau"""
        labels = {
            1: "Débutant (A1)",
            2: "Élémentaire (A2)",
            3: "Intermédiaire (B1-B2)",
            4: "Avancé (C1)",
            5: "Natif (C2)",
        }
        return labels.get(self.niveau, "Inconnu")


class BusinessManager(Base):
    """Modèle pour les Business Managers"""

    __tablename__ = "business_managers"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    nom: Mapped[str] = Column(String(100), nullable=False)
    prenom: Mapped[str] = Column(String(100), nullable=False)
    email: Mapped[str] = Column(String(255), unique=True, nullable=False)
    telephone: Mapped[Optional[str]] = Column(String(20))
    date_creation: Mapped[datetime] = Column(DateTime, default=datetime.now)
    derniere_maj: Mapped[datetime] = Column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )
    actif: Mapped[bool] = Column(Boolean, default=True)
    notes: Mapped[Optional[str]] = Column(Text)

    # Relations
    consultant_gestions: Mapped[List["ConsultantBusinessManager"]] = relationship(
        "ConsultantBusinessManager",
        back_populates="business_manager",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"<BusinessManager(id={self.id}, nom='{self.nom}', prenom='{self.prenom}')>"
        )

    @property
    def nom_complet(self) -> str:
        """Retourne le nom complet du BM"""
        return f"{self.prenom} {self.nom}"

    @property
    def consultants_actuels(self) -> List["Consultant"]:
        """Retourne les consultants actuellement gérés par ce BM"""
        return [
            cbm.consultant for cbm in self.consultant_gestions if cbm.date_fin is None
        ]

    @property
    def nombre_consultants_actuels(self) -> int:
        """Retourne le nombre de consultants actuellement gérés"""
        return len(self.consultants_actuels)


class ConsultantBusinessManager(Base):
    """Table de liaison entre consultants et business managers avec historique"""

    __tablename__ = "consultant_business_managers"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    consultant_id: Mapped[int] = Column(
        Integer, ForeignKey("consultants.id"), nullable=False
    )
    business_manager_id: Mapped[int] = Column(
        Integer, ForeignKey("business_managers.id"), nullable=False
    )
    date_debut: Mapped[datetime.date] = Column(
        Date, nullable=False, default=datetime.now
    )
    date_fin: Mapped[Optional[datetime.date]] = Column(
        Date
    )  # NULL si la gestion est active
    commentaire: Mapped[Optional[str]] = Column(
        Text
    )  # ex: "Changement d'équipe", "Promotion", etc.
    date_creation: Mapped[datetime] = Column(DateTime, default=datetime.now)

    # Relations
    consultant: Mapped["Consultant"] = relationship(
        "Consultant", back_populates="business_manager_gestions"
    )
    business_manager: Mapped["BusinessManager"] = relationship(
        "BusinessManager", back_populates="consultant_gestions"
    )

    def __repr__(self) -> str:
        return f"<ConsultantBusinessManager(consultant_id={self.consultant_id}, bm_id={self.business_manager_id}, debut={self.date_debut})>"

    @property
    def est_actuel(self) -> bool:
        """Retourne True si cette gestion est actuellement active"""
        return self.date_fin is None

    @property
    def duree_jours(self) -> int:
        """Calcule la durée de la gestion en jours"""
        date_fin_effective = self.date_fin or datetime.now().date()
        return (date_fin_effective - self.date_debut).days
