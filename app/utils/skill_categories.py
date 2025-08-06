"""
Référentiel des compétences prédéfinies pour Consultator
Catégories et technologies organisées par domaine
"""

# Référentiel des compétences techniques par catégorie
COMPETENCES_TECHNIQUES = {
    "Backend": [
        "Java", "Python", "C#/.NET", "Node.js", "PHP", "Go", "Rust", "Ruby",
        "Spring Boot", "Django", "Flask", "FastAPI", "ASP.NET", "Express.js",
        "Microservices", "API REST", "GraphQL", "gRPC"
    ],
    
    "Frontend": [
        "React", "Angular", "Vue.js", "HTML/CSS", "JavaScript", "TypeScript",
        "Next.js", "Nuxt.js", "Svelte", "jQuery", "Bootstrap", "Tailwind CSS",
        "Sass/SCSS", "Webpack", "Vite", "Material-UI", "Ant Design"
    ],
    
    "Mobile": [
        "React Native", "Flutter", "iOS (Swift)", "Android (Kotlin/Java)",
        "Xamarin", "Ionic", "Cordova", "PWA", "Unity Mobile"
    ],
    
    "Data & Analytics": [
        "Python Data", "R", "SQL", "Apache Spark", "Kafka", "Elasticsearch",
        "Power BI", "Tableau", "Qlik", "SAS", "SPSS", "Pandas", "NumPy",
        "Scikit-learn", "TensorFlow", "PyTorch", "Jupyter", "Apache Airflow",
        "dbt", "Snowflake", "BigQuery"
    ],
    
    "Cloud & DevOps": [
        "AWS", "Azure", "Google Cloud Platform", "Docker", "Kubernetes",
        "Terraform", "Ansible", "Jenkins", "GitLab CI/CD", "GitHub Actions",
        "Helm", "ArgoCD", "Prometheus", "Grafana", "ELK Stack", "Datadog"
    ],
    
    "Base de données": [
        "PostgreSQL", "MySQL", "Oracle", "SQL Server", "MongoDB", "Redis",
        "Cassandra", "DynamoDB", "Neo4j", "InfluxDB", "CouchDB", "SQLite"
    ],
    
    "Architecture & Design": [
        "Microservices", "SOA", "Event Driven Architecture", "CQRS",
        "Domain Driven Design", "Clean Architecture", "Hexagonal Architecture",
        "Design Patterns", "UML", "Architecture Cloud"
    ],
    
    "Sécurité": [
        "Cybersécurité", "OAuth", "JWT", "LDAP", "SSL/TLS", "Pen Testing",
        "OWASP", "Cryptographie", "IAM", "RBAC", "SIEM", "SOC"
    ],
    
    "Outils & Méthodologies": [
        "Git", "Jira", "Confluence", "Agile/Scrum", "Kanban", "DevOps",
        "TDD", "BDD", "CI/CD", "Code Review", "Pair Programming",
        "VS Code", "IntelliJ", "Eclipse"
    ],
    
    "IA & Machine Learning": [
        "Machine Learning", "Deep Learning", "NLP", "Computer Vision",
        "MLOps", "AutoML", "GPT/LLM", "OpenAI", "Hugging Face",
        "Azure AI", "AWS SageMaker", "Google AI"
    ]
}

# Compétences fonctionnelles par secteur
COMPETENCES_FONCTIONNELLES = {
    "Finance & Banking": [
        "Banque d'investissement", "Trading", "Risk Management", "Compliance",
        "Réglementation bancaire", "Basel III", "IFRS", "Solvency II",
        "Anti-Money Laundering", "KYC", "Payment Systems", "Blockchain Finance"
    ],
    
    "Assurance": [
        "Actuariat", "Souscription", "Gestion des sinistres", "Réassurance",
        "Solvency II", "Tarification", "Modélisation des risques",
        "Distribution d'assurance", "InsurTech"
    ],
    
    "Retail & E-commerce": [
        "Customer Experience", "Supply Chain", "Inventory Management",
        "Pricing Strategy", "Merchandising", "Omnichannel", "CRM",
        "Marketing Digital", "SEO/SEM", "Analytics E-commerce"
    ],
    
    "Santé & Pharma": [
        "Réglementation FDA", "Clinical Trials", "Pharmacovigilance",
        "Medical Devices", "Healthcare IT", "HIPAA", "HL7", "FHIR",
        "Télémédecine", "Biotechnologies"
    ],
    
    "Industrie & Manufacturing": [
        "Lean Manufacturing", "Six Sigma", "Supply Chain", "PLM",
        "ERP Manufacturing", "IoT Industriel", "Industrie 4.0", "MES",
        "Quality Management", "Maintenance prédictive"
    ],
    
    "Energie & Utilities": [
        "Smart Grid", "Renewable Energy", "Energy Trading", "Grid Management",
        "SCADA", "Asset Management", "Regulatory Compliance",
        "Carbon Management", "Energy Analytics"
    ],
    
    "Télécom & Media": [
        "Network Management", "5G", "OSS/BSS", "Broadcasting", "Streaming",
        "Content Management", "Digital Rights", "Subscriber Management",
        "Network Optimization"
    ],
    
    "Transport & Logistique": [
        "Supply Chain Optimization", "Fleet Management", "Route Optimization",
        "Warehouse Management", "TMS", "WMS", "Last Mile Delivery",
        "Autonomous Vehicles", "Smart Mobility"
    ],
    
    "Secteur Public": [
        "E-Government", "Digital Identity", "Citizen Services", "Smart Cities",
        "Public Safety", "Tax Systems", "Social Services", "Regulatory Compliance",
        "Open Data", "Digital Transformation"
    ]
}

# Niveaux de maîtrise
NIVEAUX_MAITRISE = [
    "Débutant",
    "Intermédiaire", 
    "Avancé",
    "Expert"
]

# Niveaux requis pour les postes
NIVEAUX_REQUIS = [
    "Junior",
    "Médior", 
    "Senior",
    "Lead",
    "Architect"
]

def get_all_competences():
    """Retourne toutes les compétences organisées par catégorie"""
    return {
        "techniques": COMPETENCES_TECHNIQUES,
        "fonctionnelles": COMPETENCES_FONCTIONNELLES
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
        "fonctionnelles": list(COMPETENCES_FONCTIONNELLES.keys())
    }

def search_competences(query, category_type=None):
    """Recherche des compétences par nom"""
    results = []
    competences_dict = COMPETENCES_TECHNIQUES if category_type == "techniques" else COMPETENCES_FONCTIONNELLES
    
    if category_type is None:
        competences_dict = {**COMPETENCES_TECHNIQUES, **COMPETENCES_FONCTIONNELLES}
    
    query_lower = query.lower()
    
    for category, competences in competences_dict.items():
        for competence in competences:
            if query_lower in competence.lower():
                results.append({
                    "nom": competence,
                    "categorie": category,
                    "type": category_type or ("techniques" if category in COMPETENCES_TECHNIQUES else "fonctionnelles")
                })
    
    return results
