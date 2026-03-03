# VEILLE_OBSERVABILITE.md

## 1. Différence entre monitoring et observabilité

Le monitoring se focalise sur des métriques et seuils prédéfinis pour suivre
l'état de santé d'un système. Il est **réactif** : il identifie les problèmes
après qu'ils ont eu lieu.
Exemple : alerter quand le CPU dépasse 90%.

L'observabilité va au-delà en permettant d'inférer l'état interne d'un système
à partir de ses sorties (métriques, logs, traces). Elle est **proactive** et
permet de comprendre POURQUOI un problème survient.
Exemple : comprendre pourquoi une requête est lente dans un système distribué.

## 2. Les 3 piliers de l'observabilité

- **Métriques** : données quantitatives sur la performance du système
  (CPU, RAM, nombre de requêtes). Elles répondent au "quoi".
- **Logs** : enregistrements immuables des événements discrets qui se produisent
  dans un système. Ils répondent au "pourquoi".
- **Traces** : représentent le parcours complet d'une requête à travers
  les composants d'un système distribué. Elles répondent au "où".

## 3. Architecture pull de Prometheus

Prometheus utilise un modèle **pull** : le serveur récupère régulièrement
les métriques en interrogeant les endpoints `/metrics` des cibles configurées
(toutes les 15s par défaut).

L'alternative est le modèle **push** : les applications envoient elles-mêmes
leurs métriques vers un serveur central (ex: StatsD, Graphite).

Le pull est privilégié pour sa flexibilité et son contrôle centralisé :
c'est Prometheus qui décide quand et quoi scraper.

## 4. Les 4 types de métriques Prometheus

- **Counter** : valeur cumulative qui ne peut qu'augmenter (ou revenir à 0
  au redémarrage).
  Exemple : nombre total de requêtes traitées, d'erreurs.

- **Gauge** : valeur instantanée qui peut monter et descendre.
  Exemple : RAM utilisée, nombre d'utilisateurs connectés, température.

- **Histogram** : échantillonne des observations dans des buckets configurables
  et fournit la somme de toutes les valeurs.
  Exemple : distribution des temps de réponse (combien de requêtes < 100ms,
  < 500ms, < 1s).

- **Summary** : similaire à l'histogram mais calcule des quantiles côté client
  sur une fenêtre glissante.
  Exemple : latence P99 calculée directement par l'application.

## 5. La fonction rate()

`rate()` calcule le taux d'augmentation moyen par seconde d'un Counter
sur une fenêtre de temps.

Un Counter brut de 1 000 000 ne dit pas si c'est 10 req/s ou 10 000 req/s —
il ne fait que monter. `rate()` ramène cette valeur à une unité exploitable
(req/seconde) pour créer des alertes et des graphes lisibles.

Exemple : `rate(http_requests_total[5m])` = nombre moyen de requêtes/sec
sur les 5 dernières minutes.

## 6. La fonction histogram_quantile()

`histogram_quantile(0.95, ...)` calcule le percentile 95 à partir des buckets
d'un histogram.

Exemple concret : P95 = 200ms signifie que 95% des requêtes répondent en
moins de 200ms. Les 5% restants sont les cas lents à investiguer.

Ça résout le problème de la moyenne mensongère : une moyenne de 50ms peut
cacher des pics à 2s qui impactent les utilisateurs.

## 7. Règles de nommage des métriques Prometheus

1. **snake_case** : utiliser des underscores, pas de tirets ni camelCase.
   → `http_requests_total` ✅ et non `httpRequestsTotal` ❌

2. **Suffixe d'unité** : toujours inclure l'unité dans le nom.
   → `db_query_duration_seconds` ✅ et non `db_query_duration` ❌

3. **Suffixe `_total` pour les Counters** : convention officielle Prometheus.
   → `accidents_created_total` ✅ et non `accidents_created` ❌

## 8. Histogram vs Summary — lequel choisir en production ?

| | Histogram | Summary |
|---|---|---|
| Calcul des quantiles | Côté serveur (PromQL) | Côté client (application) |
| Agrégation possible | ✅ Oui | ❌ Non |
| Précision | Dépend des buckets | Exacte |
| Coût CPU | Faible (côté serveur) | Élevé (côté client) |

**En production : préférer l'Histogram** car il permet d'agréger les données
de plusieurs instances avec `histogram_quantile()` en PromQL.
Le Summary calcule les quantiles dans l'application elle-même,
ce qui est impossible à agréger entre plusieurs pods/instances.
