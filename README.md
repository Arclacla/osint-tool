# OSINT-Tool

Un outil Python simple et puissant pour automatiser la collecte d’informations OSINT  
via plusieurs méthodes :  
- Recherche DNS et WHOIS  
- Recherche d’emails via Hunter.io  
- Recherche par dorks DuckDuckGo  
- Recherche géolocalisée Overpass Turbo (OpenStreetMap)  

---

## Fonctionnalités

### 1. Recherche DNS & WHOIS  
- Résolution des enregistrements A, MX, TXT  
- Extraction d’informations WHOIS  

### 2. Recherche Emails (Hunter.io)  
- Récupère les emails liés à un domaine (clé API requise)  

### 3. Recherche DuckDuckGo Dork (interactive)  
- Recherche avancée avec dorks personnalisés  
- Support multi-domaines, types de fichiers, mots-clés  

### 4. Recherche Overpass Turbo (OpenStreetMap)  
- Recherche d’objets géolocalisés (ex: boulangeries, pharmacies)  
- Plusieurs modes de sélection de la zone :  
  - Zones prédéfinies (ex: Toulouse, Marseille)  
  - Autour d’une adresse via géocodage (Nominatim)  
  - Bounding box manuelle  
  - Filtre par pays (tag addr:country)  

---

## Installation

1. Cloner le dépôt :

```bash
git clone https://github.com/Arclacla/osint-tool.git
cd osint-tool
