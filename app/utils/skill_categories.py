"""
Référentiel des compétences prédéfinies pour Consultator
Catégories et technologies organisées par domaine
"""

# Référentiel des compétences techniques par catégorie
COMPETENCES_TECHNIQUES = {
    "Backend": [
        "Java",
        "Python",
        "C#/.NET",
        "Node.js",
        "PHP",
        "Go",
        "Rust",
        "Ruby",
        "Spring Boot",
        "Django",
        "Flask",
        "FastAPI",
        "ASP.NET",
        "Express.js",
        "API REST",
        "GraphQL",
        "gRPC",
    ],
    "Frontend": [
        "React",
        "Angular",
        "Vue.js",
        "HTML/CSS",
        "JavaScript",
        "TypeScript",
        "Next.js",
        "Nuxt.js",
        "Svelte",
        "jQuery",
        "Bootstrap",
        "Tailwind CSS",
        "Sass/SCSS",
        "Webpack",
        "Vite",
        "Material-UI",
        "Ant Design",
    ],
    "Mobile": [
        "React Native",
        "Flutter",
        "iOS (Swift)",
        "Android (Kotlin/Java)",
        "Xamarin",
        "Ionic",
        "Cordova",
        "PWA",
        "Unity Mobile",
    ],
    "Data & Analytics": [
        "Python Data",
        "R",
        "SQL",
        "Apache Spark",
        "Kafka",
        "Elasticsearch",
        "Power BI",
        "Tableau",
        "Qlik",
        "SAS",
        "SPSS",
        "Pandas",
        "NumPy",
        "Scikit-learn",
        "TensorFlow",
        "PyTorch",
        "Jupyter",
        "Apache Airflow",
        "dbt",
        "Snowflake",
        "BigQuery",
    ],
    "Cloud & DevOps": [
        "AWS",
        "Azure",
        "Google Cloud Platform",
        "Docker",
        "Kubernetes",
        "Terraform",
        "Ansible",
        "Jenkins",
        "GitLab CI/CD",
        "GitHub Actions",
        "Helm",
        "ArgoCD",
        "Prometheus",
        "Grafana",
        "ELK Stack",
        "Datadog",
    ],
    "Base de données": [
        "PostgreSQL",
        "MySQL",
        "Oracle",
        "SQL Server",
        "MongoDB",
        "Redis",
        "Cassandra",
        "DynamoDB",
        "Neo4j",
        "InfluxDB",
        "CouchDB",
        "SQLite",
    ],
    "Architecture & Design": [
        "Microservices",
        "SOA",
        "Event Driven Architecture",
        "CQRS",
        "Domain Driven Design",
        "Clean Architecture",
        "Hexagonal Architecture",
        "Design Patterns",
        "UML",
        "Architecture Cloud",
    ],
    "Sécurité": [
        "Cybersécurité",
        "OAuth",
        "JWT",
        "LDAP",
        "SSL/TLS",
        "Pen Testing",
        "OWASP",
        "Cryptographie",
        "IAM",
        "RBAC",
        "SIEM",
        "SOC",
    ],
    "Outils & Méthodologies": [
        "Git",
        "Jira",
        "Confluence",
        "Agile/Scrum",
        "Kanban",
        "DevOps",
        "TDD",
        "BDD",
        "CI/CD",
        "Code Review",
        "Pair Programming",
        "VS Code",
        "IntelliJ",
        "Eclipse",
    ],
    "IA & Machine Learning": [
        "Machine Learning",
        "Deep Learning",
        "NLP",
        "Computer Vision",
        "MLOps",
        "AutoML",
        "GPT/LLM",
        "OpenAI",
        "Hugging Face",
        "Azure AI",
        "AWS SageMaker",
        "Google AI",
    ],
}

# Compétences fonctionnelles spécialisées Bancaire & Assurance
COMPETENCES_FONCTIONNELLES = {
    "Banque de Détail": [
        "Conseil clientèle particuliers",
        "Conseil clientèle professionnels",
        "Conseil patrimoine",
        "Crédit immobilier",
        "Crédit à la consommation",
        "Comptes et dépôts",
        "Épargne et placement",
        "Assurance-vie bancaire",
        "Moyens de paiement",
        "Services bancaires digitaux",
        "Monétique",
    ],
    "Banque d'Affaires & Corporate": [
        "Crédit corporate",
        "Financement structuré",
        "Financement de projets",
        "Syndication bancaire",
        "Trade finance",
        "Cash management",
        "Introduction en bourse (IPO)",
        "Émissions obligataires",
        "Fusions & acquisitions (M&A)",
        "Leveraged buy-out (LBO)",
        "Restructuration financière",
        "Capital markets",
    ],
    "Marchés Financiers": [
        "Trading actions (equity)",
        "Trading obligataire (fixed income)",
        "Trading dérivés",
        "Market making",
        "Sales trading",
        "Structuration de produits",
        "Analyse fondamentale",
        "Analyse technique",
        "Recherche actions (equity research)",
        "Valorisation d'entreprises",
        "Gestion de portefeuille",
        "Asset management",
        "Gestion quantitative",
    ],
    "Crédit & Risques": [
        "Scoring crédit",
        "Notation interne",
        "Analyse sectorielle",
        "Due diligence crédit",
        "Restructuration de créances",
        "Recouvrement",
        "Risque de crédit",
        "Risque de marché",
        "Risque opérationnel",
        "Risque de liquidité",
        "Stress testing",
        "Modélisation des risques",
        "Modèles VaR",
        "Backtesting",
        "Monte Carlo",
    ],
    "Assurance Vie": [
        "Épargne retraite",
        "Assurance décès",
        "Contrats en unités de compte",
        "Gestion sous mandat",
        "Prévoyance collective",
        "Actuariat vie",
        "Modélisation ALM",
        "Réserves techniques vie",
        "Distribution assurance vie",
    ],
    "Assurance Non-Vie": [
        "Assurance automobile",
        "Assurance habitation",
        "Assurance santé",
        "Assurance responsabilité civile",
        "Assurance entreprise",
        "Actuariat non-vie",
        "Gestion des sinistres",
        "Expertise sinistres",
        "Tarification IARD",
        "Modélisation catastrophes",
    ],
    "Réassurance": [
        "Souscription réassurance",
        "Traités de réassurance",
        "Réassurance facultative",
        "Réassurance obligatoire",
        "Gestion des sinistres réassurance",
        "Modélisation cat bonds",
        "Cession en réassurance",
        "Rétrocession",
    ],
    "Produits Financiers": [
        "Actions",
        "Obligations",
        "Dérivés (options, futures)",
        "Swaps",
        "Produits structurés",
        "OPCVM/SICAV",
        "ETF",
        "Private equity",
        "Hedge funds",
        "Commodities",
        "Devises (FX)",
        "Cryptomonnaies",
        "Green bonds",
        "Sukuk (finance islamique)",
        "Warrants",
        "Certificats",
    ],
    "Réglementation Bancaire": [
        "Bâle III",
        "CRD IV/CRR",
        "IFRS 9",
        "MiFID II",
        "PSD2",
        "EMIR",
        "SFTR",
        "Benchmark Regulation",
        "CSDR",
        "AIFMD",
        "UCITS",
        "MAR (Market Abuse)",
        "BRRD",
        "SRM",
        "EBA Guidelines",
    ],
    "Réglementation Assurance": [
        "Solvabilité II",
        "IFRS 17",
        "Code des assurances",
        "ACPR",
        "EIOPA Guidelines",
        "IDD",
        "PRIIPS",
        "Loi Sapin II",
        "ORSA",
        "Pilier 1-2-3 Solvency",
        "QRT",
        "SFCR",
        "RSR",
    ],
    "Compliance & AML": [
        "Anti-blanchiment (AML)",
        "KYC (Know Your Customer)",
        "LCB-FT",
        "FATCA",
        "CRS",
        "Sanctions internationales",
        "PEP screening",
        "Transaction monitoring",
        "SAR/STR",
        "TRACFIN",
        "Embargos",
        "Lutte contre financement terrorisme",
        "Due diligence renforcée",
    ],
}

# Niveaux de maîtrise
NIVEAUX_MAITRISE = ["Débutant", "Intermédiaire", "Avancé", "Expert"]

# Niveaux requis pour les postes
NIVEAUX_REQUIS = ["Junior", "Médior", "Senior", "Lead", "Architect"]


def get_all_competences():
    """Retourne toutes les compétences organisées par catégorie"""
    return {
        "techniques": COMPETENCES_TECHNIQUES,
        "fonctionnelles": COMPETENCES_FONCTIONNELLES,
    }


def get_competences_by_category(category_type="techniques"):
    """Retourne les compétences d'une catégorie spécifique"""
    if category_type == "techniques":
        return COMPETENCES_TECHNIQUES
    elif category_type == "fonctionnelles":
        return COMPETENCES_FONCTIONNELLES
    else:
        return {}


def get_all_categories():
    """Retourne toutes les catégories disponibles"""
    return {
        "techniques": list(COMPETENCES_TECHNIQUES.keys()),
        "fonctionnelles": list(COMPETENCES_FONCTIONNELLES.keys()),
    }


def search_competences(query, category_type=None):
    """Recherche des compétences par nom"""
    competences_dict = _get_competences_dict(category_type)
    query_lower = query.lower()
    results = []

    for category, competences in competences_dict.items():
        # Chercher dans le nom de la catégorie
        if query_lower in category.lower():
            results.extend(_add_all_category_competences(category, competences, category_type))
        else:
            # Chercher dans les compétences individuelles
            results.extend(_search_individual_competences(query_lower, category, competences, category_type))

    return results


def _get_competences_dict(category_type):
    """Retourne le dictionnaire de compétences selon le type"""
    if category_type == "techniques":
        return COMPETENCES_TECHNIQUES
    elif category_type == "fonctionnelles":
        return COMPETENCES_FONCTIONNELLES
    else:
        return {**COMPETENCES_TECHNIQUES, **COMPETENCES_FONCTIONNELLES}


def _add_all_category_competences(category, competences, category_type):
    """Ajoute toutes les compétences d'une catégorie"""
    results = []
    for competence in competences:
        results.append(
            {
                "nom": competence,
                "categorie": category,
                "type": _determine_competence_type(category, category_type),
            }
        )
    return results


def _search_individual_competences(query_lower, category, competences, category_type):
    """Cherche dans les compétences individuelles"""
    results = []
    for competence in competences:
        if query_lower in competence.lower():
            results.append(
                {
                    "nom": competence,
                    "categorie": category,
                    "type": _determine_competence_type(category, category_type),
                }
            )
    return results


def _determine_competence_type(category, category_type):
    """Détermine le type de compétence"""
    if category_type:
        return category_type
    return "techniques" if category in COMPETENCES_TECHNIQUES else "fonctionnelles"


# Alias pour compatibilité avec les tests
SKILL_CATEGORIES = {**COMPETENCES_TECHNIQUES, **COMPETENCES_FONCTIONNELLES}


def get_category_for_skill(skill_name: str) -> str:
    """
    Retourne la catégorie d'une compétence donnée

    Args:
        skill_name: Nom de la compétence

    Returns:
        Nom de la catégorie ou "Autre" si non trouvée
    """
    if not skill_name:
        return "Autre"

    skill_lower = skill_name.lower()

    # Chercher dans les compétences techniques
    for category, skills in COMPETENCES_TECHNIQUES.items():
        if any(skill_lower == skill.lower() for skill in skills):
            return category

    # Chercher dans les compétences fonctionnelles
    for category, skills in COMPETENCES_FONCTIONNELLES.items():
        if any(skill_lower == skill.lower() for skill in skills):
            return category

    return "Autre"


def get_all_skills() -> list:
    """
    Retourne une liste plate de toutes les compétences disponibles

    Returns:
        Liste de toutes les compétences (techniques + fonctionnelles)
    """
    all_skills = []

    # Ajouter les compétences techniques
    for skills in COMPETENCES_TECHNIQUES.values():
        all_skills.extend(skills)

    # Ajouter les compétences fonctionnelles
    for skills in COMPETENCES_FONCTIONNELLES.values():
        all_skills.extend(skills)

    return sorted(list(set(all_skills)))  # Éliminer les doublons et trier
