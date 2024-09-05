# Establishing the working directory
# -----------------------------------

import os

try:
    os.chdir('../../GlobalTerrorismAnalysis_ETL')
except FileNotFoundError:
    print("""
        Posiblemente ya ejecutaste este bloque dos o más veces o tal vez el directorio está incorrecto. 
        ¿Ya ejecutaste este bloque antes y funcionó? Recuerda no ejecutarlo de nuevo. 
        ¿Estás en el directorio incorrecto? Puedes cambiarlo. 
        Recuerda el directorio donde estás:
        """)
print(os.getcwd())

# Importing the necessary modules
# --------------------------------

from src.database.database import creating_engine, create_table
from src.rawLoad.raw import *
from src.transformation.transformation import *
