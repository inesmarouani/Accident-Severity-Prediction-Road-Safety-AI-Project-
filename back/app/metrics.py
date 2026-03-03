from prometheus_client import Counter, Gauge, Histogram

accidents_created_total = Counter("accidents_created_total", "Accidents créés")
accidents_read_total = Counter("accidents_read_total", "Accidents lus")
accidents_updated_total = Counter("accidents_updated_total", "Accidents mis à jour")
accidents_deleted_total = Counter("accidents_deleted_total", "Accidents supprimés")
accidents_total = Gauge("accidents_total", "Accidents en base")
http_errors_total = Counter("http_errors_total", "Erreurs HTTP", ["error_type"])
db_query_duration_seconds = Histogram(
    "db_query_duration_seconds",
    "Latence DB",
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5],
)
app_uptime_seconds = Gauge(
    "app_uptime_seconds",
    "Temps depuis le démarrage de l application",
)
