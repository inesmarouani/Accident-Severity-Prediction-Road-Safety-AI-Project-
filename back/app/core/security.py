"""
Fonctions de sécurité pour l'application.

Ce fichier contient des utilitaires de sécurité qui seraient utilisés pour:
- Hashing de mots de passe (bcrypt, argon2)
- Génération et validation de tokens JWT
- Vérification d'API keys
- Rate limiting

Pour l'instant, ces fonctionnalités ne sont pas nécessaires car:
- Pas d'authentification utilisateur
- API publique pour les prédictions
- Pas de gestion de sessions

À implémenter quand ajout:
- Un système de login/signup
- Des utilisateurs avec différents rôles (admin, user)
- Une limitation du nombre de prédictions par utilisateur
"""

import secrets
from datetime import timedelta
from typing import Optional

from passlib.context import CryptContext

# Context pour le hashing de mots de passe
# Utilise bcrypt, un algorithme sécurisé et lent (protection contre brute force)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Vérifie qu'un mot de passe en clair correspond à son hash.

    Exemple d'usage futur:
        user = get_user_by_email(email)
        if verify_password(password, user.hashed_password):
            # Login réussi
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash un mot de passe pour le stocker en base de données.

    Exemple d'usage futur:
        hashed = get_password_hash("mon_mot_de_passe")
        user = User(email=email, hashed_password=hashed)
    """
    return pwd_context.hash(password)


def generate_token(length: int = 32) -> str:
    """
    Génère un token aléatoire sécurisé (pour reset password, API keys, etc.)

    Exemple d'usage futur:
        reset_token = generate_token()
        # Envoyer par email pour reset password
    """
    return secrets.token_urlsafe(length)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crée un token JWT pour l'authentification.

    TODO: Implémenter avec python-jose quand nécessaire

    Exemple d'usage futur:
        token = create_access_token({"sub": user.email})
        return {"access_token": token, "token_type": "bearer"}
    """
    # Pour l'instant, retourne juste un token simple
    return generate_token()


# Note: Pour implémenter JWT complet, installer:
# pip install python-jose[cryptography]
# Et voir: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
