"""
Modèles de base de données pour Consultator
Définit la structure des tables avec SQLAlchemy
"""

from sqlalchemy import Column, Integer, String, Float, Date, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()
class Practice(Base):
    """Modèle pour les practices (Data, Quant, etc.)"""
    __tablename__ = 'practices'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    responsable = Column(String(200))  # Nom du responsable de practice
    date_creation = Column(DateTime, default=datetime.now)
    actif = Column(Boolean, default=True)

    # Relations
    consultants = relationship("Consultant", back_populates="practice")

    def __repr__(self):
        return f"<Practice(id={self.id}, nom='{self.nom}')>"

    @property
    def nombre_consultants(self):
        """Retourne le nombre de consultants dans cette practice"""
        return len([c for c in self.consultants if c.disponibilite])

class Consultant(Base):
    """Modèle pour les consultants"""
    __tablename__ = 'consultants'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    telephone = Column(String(20))
    salaire_actuel = Column(Float)
    date_creation = Column(DateTime, default=datetime.now)
    derniere_maj = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    disponibilite = Column(Boolean, default=True)
    notes = Column(Text)
    
    # Relations
    practice_id = Column(Integer, ForeignKey('practices.id'))
    practice = relationship("Practice", back_populates="consultants")
    competences = relationship("ConsultantCompetence", back_populates="consultant", cascade="all, delete-orphan")
    missions = relationship("Mission", back_populates="consultant", cascade="all, delete-orphan")
    cvs = relationship("CV", back_populates="consultant", cascade="all, delete-orphan")
    salaires = relationship("ConsultantSalaire", back_populates="consultant", cascade="all, delete-orphan")
    langues = relationship("ConsultantLangue", back_populates="consultant", cascade="all, delete-orphan")
    business_manager_gestions = relationship("ConsultantBusinessManager", back_populates="consultant", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Consultant(id={self.id}, nom='{self.nom}', prenom='{self.prenom}')>"
    
    @property
    def nom_complet(self):
        return f"{self.prenom} {self.nom}"
    
    @property
    def business_manager_actuel(self):
        """Retourne le Business Manager actuel du consultant"""
        for cbm in self.business_manager_gestions:
            if cbm.date_fin is None:
                return cbm.business_manager
        return None

class Competence(Base):
    """Modèle pour les compétences techniques et fonctionnelles"""
    __tablename__ = 'competences'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(100), unique=True, nullable=False)
    categorie = Column(String(50), nullable=False)  # Frontend, Backend, Data, Cloud, etc.
    type_competence = Column(String(20), default='technique')  # technique ou fonctionnelle
    description = Column(Text)
    niveau_requis = Column(String(20), default='junior')  # junior, medior, senior
    
    # Relations
    consultant_competences = relationship("ConsultantCompetence", back_populates="competence")
    
    def __repr__(self):
        return f"<Competence(id={self.id}, nom='{self.nom}', categorie='{self.categorie}')>"

class ConsultantCompetence(Base):
    """Table de liaison entre consultants et compétences"""
    __tablename__ = 'consultant_competences'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    consultant_id = Column(Integer, ForeignKey('consultants.id'), nullable=False)
    competence_id = Column(Integer, ForeignKey('competences.id'), nullable=False)
    annees_experience = Column(Float, default=0.0)
    niveau_maitrise = Column(String(20), default='debutant')  # debutant, intermediaire, expert
    certifications = Column(Text)  # JSON ou texte simple
    projets_realises = Column(Text)
    date_ajout = Column(DateTime, default=datetime.now)
    
    # Relations
    consultant = relationship("Consultant", back_populates="competences")
    competence = relationship("Competence", back_populates="consultant_competences")
    
    def __repr__(self):
        return f"<ConsultantCompetence(consultant_id={self.consultant_id}, competence_id={self.competence_id}, experience={self.annees_experience})>"

class Mission(Base):
    """Modèle pour les missions des consultants"""
    __tablename__ = 'missions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    consultant_id = Column(Integer, ForeignKey('consultants.id'), nullable=False)
    nom_mission = Column(String(200), nullable=False)
    client = Column(String(200), nullable=False)
    role = Column(String(300))  # Nouveau champ pour le rôle/poste
    date_debut = Column(Date, nullable=False)
    date_fin = Column(Date)
    statut = Column(String(20), default='en_cours')  # en_cours, terminee, suspendue
    taux_journalier = Column(Float)
    revenus_generes = Column(Float)
    technologies_utilisees = Column(Text)  # JSON ou texte séparé par virgules
    description = Column(Text)
    
    # Relations
    consultant = relationship("Consultant", back_populates="missions")
    
    def __repr__(self):
        return f"<Mission(id={self.id}, nom='{self.nom_mission}', client='{self.client}')>"
    
    @property
    def duree_jours(self):
        """Calcule la durée de la mission en jours"""
        if self.date_fin and self.date_debut:
            return (self.date_fin - self.date_debut).days
        return None

class CV(Base):
    """Modèle pour les CVs uploadés"""
    __tablename__ = 'cvs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    consultant_id = Column(Integer, ForeignKey('consultants.id'), nullable=False)
    fichier_nom = Column(String(255), nullable=False)
    fichier_path = Column(String(500), nullable=False)
    contenu_extrait = Column(Text)  # Contenu parsé du CV
    date_upload = Column(DateTime, default=datetime.now)
    taille_fichier = Column(Integer)  # en bytes
    
    # Relations
    consultant = relationship("Consultant", back_populates="cvs")
    
    def __repr__(self):
        return f"<CV(id={self.id}, consultant_id={self.consultant_id}, fichier='{self.fichier_nom}')>"

class CustomTechnology(Base):
    """Modèle pour les technologies personnalisées"""
    __tablename__ = 'custom_technologies'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(100), nullable=False, unique=True)
    categorie = Column(String(100), nullable=False, default="Personnalisées")
    description = Column(Text)
    date_creation = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<CustomTechnology(id={self.id}, nom='{self.nom}', categorie='{self.categorie}')>"

class ConsultantSalaire(Base):
    """Historique des salaires d'un consultant"""
    __tablename__ = 'consultant_salaires'
    id = Column(Integer, primary_key=True, autoincrement=True)
    consultant_id = Column(Integer, ForeignKey('consultants.id'), nullable=False)
    salaire = Column(Float, nullable=False)
    date_debut = Column(Date, nullable=False, default=datetime.now)
    date_fin = Column(Date)
    commentaire = Column(Text)
    consultant = relationship("Consultant", back_populates="salaires")
    def __repr__(self):
        return f"<ConsultantSalaire(id={self.id}, consultant_id={self.consultant_id}, salaire={self.salaire}, date_debut={self.date_debut})>"

class Langue(Base):
    """Modèle pour les langues"""
    __tablename__ = 'langues'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(100), nullable=False, unique=True)
    code_iso = Column(String(5))  # ex: FR, EN, ES, DE, IT
    description = Column(Text)
    
    # Relations
    consultant_langues = relationship("ConsultantLangue", back_populates="langue")
    
    def __repr__(self):
        return f"<Langue(id={self.id}, nom='{self.nom}', code_iso='{self.code_iso}')>"

class ConsultantLangue(Base):
    """Table de liaison entre consultants et langues avec niveau"""
    __tablename__ = 'consultant_langues'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    consultant_id = Column(Integer, ForeignKey('consultants.id'), nullable=False)
    langue_id = Column(Integer, ForeignKey('langues.id'), nullable=False)
    niveau = Column(Integer, nullable=False)  # 1=Débutant, 2=Élémentaire, 3=Intermédiaire, 4=Avancé, 5=Natif
    commentaire = Column(Text)  # ex: "Lu, écrit, parlé", "Certification TOEIC 850", etc.
    date_ajout = Column(DateTime, default=datetime.now)
    
    # Relations
    consultant = relationship("Consultant", back_populates="langues")
    langue = relationship("Langue", back_populates="consultant_langues")
    
    def __repr__(self):
        return f"<ConsultantLangue(consultant_id={self.consultant_id}, langue_id={self.langue_id}, niveau={self.niveau})>"
    
    @property
    def niveau_label(self):
        """Retourne le label du niveau"""
        labels = {
            1: "Débutant (A1)",
            2: "Élémentaire (A2)", 
            3: "Intermédiaire (B1-B2)",
            4: "Avancé (C1)",
            5: "Natif (C2)"
        }
        return labels.get(self.niveau, "Inconnu")

class BusinessManager(Base):
    """Modèle pour les Business Managers"""
    __tablename__ = 'business_managers'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    telephone = Column(String(20))
    date_creation = Column(DateTime, default=datetime.now)
    derniere_maj = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    actif = Column(Boolean, default=True)
    notes = Column(Text)
    
    # Relations
    consultant_gestions = relationship("ConsultantBusinessManager", back_populates="business_manager", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<BusinessManager(id={self.id}, nom='{self.nom}', prenom='{self.prenom}')>"
    
    @property
    def nom_complet(self):
        """Retourne le nom complet du BM"""
        return f"{self.prenom} {self.nom}"
    
    @property
    def consultants_actuels(self):
        """Retourne les consultants actuellement gérés par ce BM"""
        return [cbm.consultant for cbm in self.consultant_gestions if cbm.date_fin is None]
    
    @property
    def nombre_consultants_actuels(self):
        """Retourne le nombre de consultants actuellement gérés"""
        return len(self.consultants_actuels)

class ConsultantBusinessManager(Base):
    """Table de liaison entre consultants et business managers avec historique"""
    __tablename__ = 'consultant_business_managers'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    consultant_id = Column(Integer, ForeignKey('consultants.id'), nullable=False)
    business_manager_id = Column(Integer, ForeignKey('business_managers.id'), nullable=False)
    date_debut = Column(Date, nullable=False, default=datetime.now)
    date_fin = Column(Date)  # NULL si la gestion est active
    commentaire = Column(Text)  # ex: "Changement d'équipe", "Promotion", etc.
    date_creation = Column(DateTime, default=datetime.now)
    
    # Relations
    consultant = relationship("Consultant", back_populates="business_manager_gestions")
    business_manager = relationship("BusinessManager", back_populates="consultant_gestions")
    
    def __repr__(self):
        return f"<ConsultantBusinessManager(consultant_id={self.consultant_id}, bm_id={self.business_manager_id}, debut={self.date_debut})>"
    
    @property
    def est_actuel(self):
        """Retourne True si cette gestion est actuellement active"""
        return self.date_fin is None
    
    @property
    def duree_jours(self):
        """Calcule la durée de la gestion en jours"""
        date_fin_effective = self.date_fin or datetime.now().date()
        return (date_fin_effective - self.date_debut).days
