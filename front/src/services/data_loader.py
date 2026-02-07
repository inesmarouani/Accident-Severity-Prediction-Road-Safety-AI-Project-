"""Chargement et gestion des données CSV"""

import pandas as pd
from src.config import config

class DataLoader:
    """Gestionnaire de données CSV"""
    
    def __init__(self):
        self.df = None
        self.load_data()
    
    def load_data(self):
        """Charge le fichier CSV"""
        self.df = pd.read_csv(config.DATA_PATH)
        # Renommer si nécessaire
        if "grav_accident" in self.df.columns:
            self.df.rename(columns={"grav_accident": "gravite"}, inplace=True)
    
    def get_dataframe(self) -> pd.DataFrame:
        """Retourne le DataFrame"""
        return self.df.copy()
    
    def filter_data(self, dep=None, saison=None, gravite=None) -> pd.DataFrame:
        """
        Filtre les données selon les critères
        
        Args:
            dep: Liste des départements
            saison: Liste des saisons
            gravite: Liste des gravités
            
        Returns:
            DataFrame filtré
        """
        dff = self.df.copy()
        
        if dep:
            dff = dff[dff["dep"].isin(dep)]
        if saison:
            dff = dff[dff["saison"].isin(saison)]
        if gravite:
            dff = dff[dff["gravite"].isin(gravite)]
        
        return dff

# Instance singleton
data_loader = DataLoader()