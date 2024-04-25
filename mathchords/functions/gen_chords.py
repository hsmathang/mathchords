from itertools import product
import pickle
import os
from datetime import datetime

def generate_chords(scale, octaves, sizes, intervals, max_population=-1):
    """
    Genera una lista de acordes musicales.

    Parámetros:
    - scale: un diccionario que representa la escala musical. Debe contener 'intervals' y 'root'.
    - octaves: una lista de octavas en las que se generarán los acordes.
    - sizes: una lista de tamaños de acorde (número de notas en el acorde) cardinal.
    - intervals: una lista de intervalos musicales posibles para los acordes. Son saltos por entre la escala
    - max_population: número máximo de acordes a generar. Si es -1, no hay límite.

    Retorna:
    - Una lista de diccionarios, donde cada diccionario representa un acorde.
    """

    chords = []  # Lista para almacenar los acordes generados

    # Itera sobre cada octava proporcionada
    for octave in octaves:
        # Itera sobre cada nota de la escala
        for index, note in enumerate(scale["intervals"]):
            # Itera sobre los tamaños de acorde dados
            for size in sizes:
                # Crea todas las combinaciones posibles de intervalos para el tamaño actual
                for interval_permutation in product(intervals, repeat=size):
                    # Construye el acorde inicial con su octava, nota raíz e intervalos
                    chord = {"octave": octave, "bass":scale["root"] + note, "root": scale["root"] + note, "degree": index+1,  "intervals": list(interval_permutation)}

                    pos = index  # Posición actual en la escala
                    # Actualiza los intervalos del acorde basándose en la escala
                    for i, interval in enumerate(chord["intervals"]):
                        val = (pos + chord["intervals"][i]) % len(scale["intervals"])
                        chord["intervals"][i] = (scale["intervals"][val] - scale["intervals"][pos]) % 12
                        pos = val

                    # Añade el acorde a la lista de acordes
                    chords.append(chord)

                    # Si se alcanza la población máxima de acordes, termina el bucle
                    if max_population > 0 and len(chords) == max_population:
                        break

    return chords  # Devuelve la lista de acordes generados

def Simula_inversiones(chords):
    """
    Simula las inversiones de una lista de acordes.
    
    Cada acorde se puede invertir moviendo la nota más baja una octava más arriba, 
    lo que cambia el bajo del acorde pero mantiene las mismas notas. Esta función
    genera todas las inversiones posibles para cada acorde proporcionado.
    
    Parámetros:
    - chords: Lista de diccionarios, donde cada diccionario representa un acorde. 
              Cada acorde debe tener una clave "intervals" que es una lista de 
              intervalos en semitonos desde la nota más baja, y una clave "bass" 
              que indica la nota más baja del acorde en semitonos desde C0.
    
    Retorna:
    - Una lista de diccionarios, donde cada diccionario representa un acorde 
      original o una de sus inversiones. La clave "bass" de cada acorde se actualiza 
      para reflejar la nota más baja después de la inversión.
    """
    output = []  # Lista para almacenar los acordes originales e invertidos
    
    for chord in chords:
        # Añade el acorde original a la lista de salida
        output.append(chord.copy())
        
        # Itera sobre los intervalos del acorde para generar las inversiones
        for index in chord["intervals"]:
            # Copia la última versión del acorde (ya sea el original o una inversión previa)
            output.append(output[-1].copy())
            
            # Actualiza el bajo del acorde añadiendo el intervalo actual y asegurando
            # que el valor se mantenga dentro de una octava (0-11 semitonos)
            output[-1]["bass"] += index
            output[-1]["bass"] %= 12  # Asegura que 'bass' esté dentro del rango 0-11

    return output  # Devuelve la lista de acordes originales e invertidos



'''
def create_experiment_data(scale, octaves, sizes, intervals, chords, 
                           experiment_name="Experimento Musical", description="", 
                           experiment_date=None, version="1.0"):
    """
    Crea un diccionario con los datos de un experimento musical, incluyendo metadatos adicionales para una mejor documentación.

    Parámetros:
    - scale: Diccionario que representa la escala musical. Debe contener 'name' y 'intervals'.
    - octaves: Lista de octavas para generar acordes.
    - sizes: Lista de tamaños de los acordes.
    - intervals: Lista de intervalos para los acordes.
    - chords: Lista de acordes generados.
    - experiment_name: Nombre personalizado para el experimento.
    - description: Descripción del propósito o hipótesis del experimento.

    - experiment_date: Fecha en que se realizó el experimento. Si es None, se usará la fecha actual.
    - version: Versión del experimento, útil para el seguimiento de cambios.

    Retorna:
    Diccionario con los datos del experimento, incluyendo metadatos para documentación.
    """
    if experiment_date is None:
        experiment_date = datetime.now().strftime("%Y-%m-%d")

    experiment_metadata = {
        'experiment_name': experiment_name,
        'description': description,
        'experiment_date': experiment_date,
        'version': version,
        'experiment_params': {
            'scale': scale,
            'octaves': octaves,
            'sizes': sizes,
            'intervals': intervals,
        },
        'chords': chords
    }
    
    return experiment_metadata
'''


def create_experiment_data(scale, octaves, sizes, intervals, chords, 
                           experiment_name="Experimento Musical", description="", 
                           experiment_date=None, version="1.0"):
    """
    Crea un diccionario con los datos de un experimento musical, incluyendo metadatos adicionales para una mejor documentación.

    Parámetros:
    - scale: Diccionario que representa la escala musical. Debe contener 'name' y 'intervals'.
    - octaves: Lista de octavas para generar acordes.
    - sizes: Lista de tamaños de los acordes.
    - intervals: Lista de intervalos para los acordes.
    - chords: Lista de acordes generados.
    - experiment_name: Nombre personalizado para el experimento.
    - description: Descripción del propósito o hipótesis del experimento.
    - author: Nombre del investigador o creador del experimento.
    - experiment_date: Fecha en que se realizó el experimento. Si es None, se usará la fecha actual.
    - version: Versión del experimento, útil para el seguimiento de cambios.

    Retorna:
    Diccionario con los datos del experimento, incluyendo metadatos para documentación.
    """
    if experiment_date is None:
        experiment_date = datetime.now().strftime("%Y-%m-%d")

    experiment_metadata = {
        'experiment_name': experiment_name,
        'description': description,
        'experiment_date': experiment_date,
        'version': version,
        'experiment_params': {
            'scale': scale,
            'octaves': octaves,
            'sizes': sizes,
            'intervals': intervals,
        },
        'chords': chords
    }
    
    return experiment_metadata


def save_experiment_data(experiment_data, base_path):
    """
    Guarda los datos del experimento en un archivo dentro de una carpeta específica, sin crear una carpeta por cada versión.

    Parámetros:
    - experiment_data: Los datos del experimento a guardar.
    - base_path: La ruta base donde se guardarán los experimentos.
    """
    # Asegurarse de que el directorio base existe
    if not os.path.exists(base_path):
        os.makedirs(base_path, exist_ok=True)
    
    # Construir el nombre del archivo incluyendo la versión del experimento
    # Formato: 'experiment_name - YYYY-MM-DD - version.pkl'
    file_name = f"{experiment_data['experiment_name']} - {datetime.now().strftime('%Y-%m-%d')} - v{experiment_data['version']}.pkl"
    file_path = os.path.join(base_path, file_name)
    
    # Guardar los datos del experimento en el archivo
    try:
        with open(file_path, 'wb') as file:
            pickle.dump(experiment_data, file)
        print(f"Datos guardados exitosamente en {file_path}")
    except Exception as e:
        print(f"Error al guardar los datos del experimento: {e}")
