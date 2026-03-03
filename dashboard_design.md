## Dashboard 1 — HTTP Overview
**Public cible** : SRE / DevOps
**Objectif** : surveiller la santé HTTP de l'API en temps réel

### Panels et justifications
- Requêtes/sec : voir le trafic en temps réel
- Latence P95 : détecter les dégradations de performance
- Taux d'erreur : alerter sur les anomalies
- Total requêtes : volume global
- CPU % : corréler charge applicative et charge système
- RAM % : détecter les fuites mémoire

## Dashboard 2 — Accident Severity Monitoring
**Public cible** : Product / Data
**Objectif** : suivre l'activité métier de l'API de prédiction

### Panels et justifications
- Accidents prédits total : KPI métier principal
- Prédictions/min : débit du modèle ML
- Latence DB : performance des requêtes
- Erreurs par type : segmentation pour debug rapide
- CPU/RAM : corrélation charge ML et ressources
- Requêtes par endpoint : usage de l'API
