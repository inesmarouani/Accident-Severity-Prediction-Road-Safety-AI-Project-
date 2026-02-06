# ============================================
# ÉTAPE 1: Image de base
# ============================================

FROM python:3.12-slim

#Métadonnées de l'image
LABEL maintainer="ines.marouani69@gmail.com"
LABEL version="1.0"
LABEL description="Image Docker pour une application Python 3.14 avec Flask et requests"

# ============================================
# ÉTAPE 2: Configuration de l'environnement
# ============================================

# Variables d'environnement

# Définir le répertoire de travail
WORKDIR /app

# ============================================
# ÉTAPE 3: Installation des dépendances
# ============================================

#installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copier requirements.txt d'abord (cache Docker)
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# ============================================
# ÉTAPE 4: Copie du code source
# ============================================
# Copier le code source de l'application dans le conteneur
COPY . /app


# ============================================
# ÉTAPE 5: Configuration finale
# ============================================
RUN useradd -m -u 1000 appuser

# Donner les permissions sur /app à appuser
RUN chown -R appuser:appuser /app


#changer l'utilisateur 
USER appuser

# Exposer le port sur lequel l'application va s'exécuter
EXPOSE 8000 

#Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s \
    CMD python -c "import sys; sys.exit(0)"

# Commande pour démarrer l'application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]