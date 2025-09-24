# Configuration IA pour Consultator
# Ce fichier contient les instructions pour configurer l'IA Grok

## 🚀 Configuration de Grok AI

### 1. Obtenir une clé API
1. Allez sur [x.ai](https://x.ai)
2. Créez un compte si nécessaire
3. Générez une clé API dans votre dashboard

### 2. Configuration de l'environnement

#### Option A : Variable d'environnement système
```bash
# Windows (PowerShell)
$env:GROK_API_KEY = "votre_clé_api_ici"

# Windows (CMD)
set GROK_API_KEY=votre_clé_api_ici

# Linux/Mac
export GROK_API_KEY="votre_clé_api_ici"
```

#### Option B : Fichier .env (recommandé)
Créez un fichier `.env` à la racine du projet :
```
GROK_API_KEY=votre_clé_api_ici
```

### 3. Installation des dépendances
```bash
pip install requests
```

### 4. Test de la configuration
Lancez l'application et allez dans la section Documents d'un consultant.
Vous devriez voir l'option "🤖 IA avec Grok (recommandé)" disponible.

## 💰 Coûts estimés

- **Analyse d'un CV moyen** : ~$0.001-0.005
- **Volume mensuel typique** : 50-200 analyses = $0.10-1.00/mois
- **Limite gratuite** : Selon les conditions x.ai

## 🔧 Dépannage

### Erreur "Clé API manquante"
- Vérifiez que la variable `GROK_API_KEY` est définie
- Redémarrez l'application après avoir défini la variable

### Erreur "Connexion échouée"
- Vérifiez votre connexion internet
- Vérifiez que votre clé API est valide
- Vérifiez les quotas d'utilisation sur x.ai

### Erreur "JSON invalide"
- Le modèle peut parfois produire un format inattendu
- Essayez de relancer l'analyse
- L'analyse classique reste disponible en fallback

## 🛡️ Sécurité

- **Ne partagez jamais** votre clé API
- **Stockez-la** dans des variables d'environnement, pas dans le code
- **Surveillez** votre utilisation sur le dashboard x.ai
- **Les données** envoyées à Grok sont traitées selon leur politique de confidentialité