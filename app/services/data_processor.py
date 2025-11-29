import pandas as pd
import numpy as np
import logging
from sklearn.model_selection import train_test_split

class DataProcessor:
    def __init__(self):
        pass

    def load_training_data(self, file_path: str):
        """Cargar datos de entrenamiento desde CSV"""
        try:
            df = pd.read_csv(file_path)
            logging.info(f"✅ Datos de entrenamiento cargados: {len(df)} muestras")
            return df
        except Exception as e:
            logging.error(f"Error cargando datos de entrenamiento: {e}")
            return None

    def prepare_data(self, df):
        """Preparar datos para entrenamiento"""
        # Asumimos que el CSV tiene columnas 'text' y 'label'
        # donde label es 0 para correctivo y 1 para evolutivo
        
        # Para este ejemplo, generaremos datos sintéticos si no hay archivo
        if df is None or len(df) == 0:
            return self.generate_synthetic_data()
        
        X = df['text'].values
        y = df['label'].values
        
        # Vectorización simple (en un caso real, usaríamos el mismo vectorizador que en MS-Text-Analysis)
        # Por ahora, generamos vectores aleatorios para demostración
        X_vectors = np.random.rand(len(X), 1000)
        
        return X_vectors, y

    def generate_synthetic_data(self, n_samples=1000):
        """Generar datos sintéticos para demostración"""
        logging.info("Generando datos sintéticos para entrenamiento")
        
        # Vectores de características aleatorias
        X = np.random.rand(n_samples, 1000)
        
        # Etiquetas aleatorias (0: correctivo, 1: evolutivo)
        y = np.random.randint(0, 2, n_samples)
        
        return X, y