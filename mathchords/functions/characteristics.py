from typing import Callable
import numpy as np
import os
import pickle

import math
from mathchords.io import Experiment

def polar_pitch_classes(chord, chord_id):
    # Inicializar el vector de características con 0s
    feature_vector = [0.0] * 24  # 12 pares de coordenadas (coseno, seno)
    
    pitch_classes = pitch_classes_extractor(chord, chord_id)["feature_vector"]
    
    for pitch_class in pitch_classes:
        angle = pitch_class * (2 * math.pi / 12)  # Convertir a radianes
        x = math.cos(angle)
        y = math.sin(angle)
        feature_vector[pitch_class * 2] = x
        feature_vector[pitch_class * 2 + 1] = y
    
    result = {
        "chord": chord,
        "feature_vector": feature_vector,
        "chord_id": chord_id
    }
    return result



def polar_degree(data):
     # Inicializa variables para llevar un registro del último grado procesado y su ángulo asociado
    last_degree = None
    last_angle = None
    scale_degrees = len(data['experiment_params']['scale']['intervals'])
    
    results = {}
    
    # Itera sobre cada acorde en el conjunto de datos
    for i, chord in enumerate(data['chords']):
        # Verifica si el grado del acorde actual es diferente al último procesado
        if chord['degree'] != last_degree:
            # Actualiza el último grado procesado y calcula un nuevo ángulo
            last_degree = chord['degree']
            # Asume que la escala completa se distribuye uniformemente en 360 grados
            angle_between_degrees = 2 * math.pi / scale_degrees  # 7 es el número total de grados únicos en la escala mayor
            last_angle = (last_degree - 1) * angle_between_degrees
        
        # Usa el ángulo (ya sea recién calculado o el último usado para este grado)
        x = math.cos(last_angle)
        y = math.sin(last_angle)
        
        # Genera un ID único para cada acorde basándose en su índice en la lista
        chord_id = f"chord_{i}"
        
        # Almacena el resultado usando el ángulo calculado o reutilizado
        results[chord_id] = {
            "chord": chord,
            "feature_vector": [x, y],
            "chord_id": chord_id
        }
    
    return results

def intervals_extractor(chord):
    # La función recibe un acorde y extrae los intervalos entre sus notas

    # Calcula el número total de notas en el acorde.
    # Se suma 1 a la longitud de los intervalos para incluir la nota raíz en el conte
    n = len(chord['intervals']) + 1

    # Crea una matriz de ceros con tamaño (n-1) x (n-1).
    # Esta matriz será una matriz triangular superior que representará los intervalos entre las notas.
    chormatrix = np.zeros((n-1, n-1))

    # Calcula las posiciones absolutas de las notas en una escala.
    # Comienza con la nota raíz (posición 0) y luego suma cada intervalo de forma acumulativa.
    note_positions = [0] + list(np.cumsum(chord['intervals']))

    # Llena la matriz con las distancias entre cada par de notas.
    # Recorre solo la parte necesaria de la matriz para mejorar la eficiencia.
    for i in range(n-1):
        for j in range(i+1, n):
            # La distancia entre dos notas se calcula como la diferencia absoluta de sus posiciones.
            dist = abs(note_positions[i] - note_positions[j])

            # Asigna esta distancia a la matriz en la posición correspondiente.
            chormatrix[i, j-1] = dist

    # Devuelve la matriz de intervalos completada.
    return chormatrix

def pitch_classes_extractor(chord: dict,chord_id: int, repeat: bool =False) -> dict:
    """
    Extrae las clases de tono de un acorde.

    Parámetros:
    - chord (dict): Un diccionario con las claves "root" e "intervals", donde "root" es la nota raíz y "intervals" es una lista de intervalos.
    - repeat (bool): Si es True, mantiene las clases de tono repetidas. Si es False, elimina las clases de tono repetidas.

    Retorna:
    - Una lista de clases de tono.

    Nota:
    En la teoría de conjuntos de tono, generalmente se manejan conjuntos sin repeticiones. Sin embargo,
    si se desea conservar las repeticiones para un análisis o aplicación específica, se puede hacerlo con el parámetro `repeat`.
    """
    root = chord["root"]
    chord_pitches = [root]

    for interval in chord["intervals"]:
        root += interval
        root %= 12
        chord_pitches.append(root)

    #if not repeat:
        #chord_pitches = list(set(chord_pitches))
    feature_vector=chord_pitches
    result = {
        "chord": chord,
        "feature_vector": feature_vector,
        "chord_id": chord_id
    }





    return  result



def transpose_to_zero(chord, chord_id):
    """Transpone un conjunto de clases de tono para que el primer elemento sea 0."""
    pc_set = pitch_classes_extractor(chord, chord_id)["feature_vector"]
    transposition = pc_set[0]
    feature_vector=[(pitch - transposition) % 12 for pitch in pc_set]
    result = {
        "chord": chord,
        "feature_vector": feature_vector,  # Reemplazar por la forma normal calculada
        "chord_id": chord_id
    }
    return result
     

def prime_form(chord, chord_id):
    """
    Calculates the prime form of a pitch class set.

    Parameters:
    - pcs (list): A list containing the pitch classes of the set.

    Returns:
    - A list representing the prime form of the set.

    Context:
    Following Allen Forte's theory of pitch-class set, the prime form is the most compact representation of a set.
    It's obtained by comparing the normal form of the original set and its inversion, and then selecting the most "left-ward" form.


   



    pcs = pitch_classes_extractor(chord, chord_id)["feature_vector"]
    def inverted_pcs(pcs):
        feature_vector= [(12 - pitch) % 12 for pitch in pcs]
        
        result = {
        "chord": chord,
        "feature_vector": feature_vector,  
        "chord_id": chord_id
                }
        return result

   
    inverted_normal_form = normal_form(inverted_pcs(pcs)["chord"],inverted_pcs(pcs)["chord_id"])["feature_vector"]

    if tuple(inverted_normal_form) < tuple(pcs):
        return inverted_normal_form
    feature_vector=pcs

    """
    pcs = pitch_classes_extractor(chord, chord_id)["feature_vector"]
    normal_result = normal_form(chord, chord_id)
    normal = normal_result["feature_vector"]
    
    inverted = [(12 - p) % 12 for p in pcs]
    inverted.sort()  # Asegurarse de que la lista esté ordenada para la forma normal
    inverted_normal = [((n - inverted[0]) % 12) for n in inverted]  # Ajustar para comenzar en 0

    transposed_normal = [(note - normal[0]) % 12 for note in normal]
    transposed_inverted = inverted_normal  # Ya ajustado para comenzar en 0

    # Escoger la forma más compacta a la izquierda como forma prima
    prime = min(transposed_normal, transposed_inverted, key=lambda x: (x, len(set(x)), -x[1]))
    result = {
        "chord": chord,
        "feature_vector": prime,  
        "chord_id": chord_id
    }
    return result


def interval_vector(chord,chord_id):
    """
    Calcula el vector de intervalos para un conjunto de clases de tono.

    El vector de intervalos es un histograma que cuenta la ocurrencia de cada intervalo posible (del 1 al 6) en un conjunto.
    Es una herramienta útil para clasificar y comparar conjuntos en la teoría de Allen Forte.

    Parámetros:
    pcs (list): Lista de clases de tono (enteros del 0 al 11).

    Retorna:
    list: Vector de intervalos del conjunto de clases de tono.
    """
    pcs = pitch_classes_extractor(chord, chord_id)["feature_vector"]
    intervals = [0] * 6

    # Cuenta cada intervalo en el conjunto
    for i in range(len(pcs)):
        for j in range(i + 1, len(pcs)):
            interval = abs(pcs[j] - pcs[i]) % 12
            if interval > 6:
                interval = 12 - interval
            intervals[interval - 1] += 1
    feature_vector=intervals
    result = {
        "chord": chord,
        "feature_vector": feature_vector,  # Reemplazar por la forma normal calculada
        "chord_id": chord_id
    }
    return result


def normal_form(chord, chord_id):
    """
    Devuelve la forma normal de un conjunto de clases de tono.

    La idea detrás de la forma normal es tomar un conjunto de clases de tono y transformarlo en una forma estándar,
    es decir, una forma que representa todas las transposiciones e inversiones posibles del conjunto.
    Esta es una técnica introducida por Allen Forte en su teoría de conjuntos de clases de tono.

    Parámetros:
    pcs (list): Lista de clases de tono (enteros del 0 al 11).

    Retorna:
    list: Forma normal del conjunto de clases de tono.



    

    
    """
    pcs = pitch_classes_extractor(chord, chord_id)["feature_vector"]
    pcs = sorted(set(pcs))  # Eliminar duplicados y ordenar

    # Función para calcular la distancia de abarque de una rotación
    def span(rotation):
        return (rotation[-1] - rotation[0]) % 12

    # Generar todas las rotaciones posibles
    rotations = [[pcs[(i + j) % len(pcs)] for j in range(len(pcs))] for i in range(len(pcs))]

    # Seleccionar la rotación con la distancia de abarque mínima
    min_span_rotation = min(rotations, key=lambda x: (span(x), x))

    feature_vector = min_span_rotation

    result = {
        "chord": chord,
        "feature_vector": feature_vector,  # Reemplazar por la forma normal calculada
        "chord_id": chord_id
    }
    return result



def rahn_normal_order(chord, chord_id):
    # Obtenemos las clases de tono desde el diccionario devuelto por pitch_classes_extractor
    pitch_class_set = pitch_classes_extractor(chord, chord_id)["feature_vector"]

    # Convertir el conjunto a un conjunto único para eliminar duplicados y luego a una lista para poder ordenarlo
    pitch_class_set = sorted(list(set(pitch_class_set)))

    # Enumerar todos los posibles ciclos del conjunto de clases de tono
    cycles = [pitch_class_set[i:] + pitch_class_set[:i] for i in range(len(pitch_class_set))]

    # Función para calcular la compactness de un ciclo
    def compactness(cycle):
        # Diferencia entre el último y el primer elemento, módulo 12
        return (cycle[-1] - cycle[0]) % 12

    # Función para aplicar criterios secundarios en caso de empates en compactness
    def secondary_criteria(cycle):
        # Itera desde el segundo hasta el último elemento para desempatar
        for i in range(2, len(cycle) + 1):
            yield (cycle[-i] - cycle[0]) % 12

    # Seleccionar el ciclo más compacto, utilizando primero compactness y luego criterios secundarios
    most_compact_cycle = min(cycles, key=lambda cycle: (compactness(cycle), *secondary_criteria(cycle)))

    # Preparar y devolver el resultado
    result = {
        "chord": chord,
        "feature_vector": most_compact_cycle,
        "chord_id": chord_id
    }
    return result




def binary_pitch_class_set(chord, chord_id):
    # Obtenemos las clases de tono desde el diccionario devuelto por pitch_classes_extractor
    pitch_class_set = pitch_classes_extractor(chord, chord_id)["feature_vector"]

    # Representar como vector binario: 1 si la clase de tono está presente, 0 si no
    binary_vector = [1 if i in pitch_class_set else 0 for i in range(12)]

    # Preparar y devolver el resultado
    result = {
        "chord": chord,
        "feature_vector": binary_vector,
        "chord_id": chord_id
    }
    return result

def generate_interval_histogram(chord):
    # Extraemos la matriz de intervalos
    intervals_matrix = intervals_extractor(chord)

    # Aplanamos la matriz de intervalos y la convertimos a una lista
    intervals_list = intervals_matrix.flatten().tolist()

    # Creamos un histograma con 11dims para los intervalos
    interval_histogram = [0] * 11
    for interval in intervals_list:
        if interval != 0:  # Excluimos la nota raíz
            interval_histogram[int(interval) - 1] += 1

    return interval_histogram








def Experiment_pcset(chord, chord_id):


    # Extraemos el conjunto PC y el histograma de intervalos
    pc_set = pitch_classes_extractor(chord,chord_id)
    interval_histogram = generate_interval_histogram(chord)

    # Combinamos el conjunto PC y el histograma de intervalos en un solo vector de características
    feature_vector = pc_set['feature_vector'] + interval_histogram
    #feature_vector = pc_set

    # Agregamos el chord_id al resultado
    result = {
        "chord": chord,
        "feature_vector": feature_vector,
        "chord_id": chord_id
    }

    return result


def inversion_from_bass(chord):
    """ Experimetno 1
    Calcula la inversión explícita del acorde basada en el bajo, dando como resultado
    una lista que representa la secuencia de notas del acorde empezando desde el bajo.
    """
    # Calcula las posiciones absolutas de las notas en el acorde
    root_note = chord['root']
    intervals = chord['intervals']
    note_sequence = [root_note] + [(root_note + sum(intervals[:i+1])) % 12 for i in range(len(intervals))]

    # Encuentra el índice del bajo en la secuencia de notas
    bass_index = note_sequence.index(chord['bass'])

    # Reorganiza la secuencia de notas para que comience desde el bajo
    reordered_sequence = note_sequence[bass_index:] + note_sequence[:bass_index]

    return reordered_sequence

def interval_histogram(chord, chord_id):
    note_sequence = inversion_from_bass(chord)
    histogram = [0] * 11  # Ajustado a 11 posiciones para intervalos dentro de una octava

    # Calcular intervalos entre la nota actual y todas las posteriores en la secuencia
    for i in range(len(note_sequence) - 1):  # Excluir la última nota para el cálculo
        for j in range(i+1, len(note_sequence)):
            interval = (note_sequence[j] - note_sequence[i]) % 12
            if interval > 0:  # Asegurar que se cuentan solo intervalos positivos
                histogram[interval - 1] += 1

    result = {
        "chord": chord,
        "feature_vector": histogram,
        "chord_id": chord_id
    }

    return result




def only_six_intervals(chord, chord_id):
    """
    Calcula el vector de intervalos de 6 posiciones para un acorde dado y devuelve un diccionario con este vector y el chord_id.

    Parámetros:
    - chord (dict): Un diccionario con las claves "root" e "intervals", donde "root" es la nota raíz y "intervals" es una lista de intervalos.
    - chord_id (any): Identificador del acorde.

    Retorna:
    - dict: Un diccionario con las claves "feature_vector" y "chord_id". "feature_vector" es el vector de intervalos calculado.
    """
    # Extraer las clases de tono del acorde
    chord_pitches=pitch_classes_extractor(chord, chord_id)["feature_vector"]
    inversion_chord=inversion_from_bass(chord)
    # Calcular el vector de intervalos
    intervals = [0] * 6

    for i in range(len(chord_pitches)):
        for j in range(i + 1, len(chord_pitches)):
            interval = abs(chord_pitches[j] - chord_pitches[i]) % 12
            if interval > 6:
                interval = 12 - interval
            intervals[interval - 1] += 1

    # Devolver el diccionario con el vector de características y el chord_id
    result = {
        "chord": chord,
        "feature_vector": intervals,
        "withPCs": inversion_chord + intervals,
        "chord_id": chord_id
    }

    return result


def process(data: dict, func: Callable):
    results = {}
    chords = data["chords"]
    for i, chord in enumerate(chords):
        chord_id = f"chord_{i}"  # Generar un identificador único para el acorde
        result = func(chord, chord_id)  # Llamamos a func en lugar de Experiment_pcset directamente
        #print(result)
        result['chord_id'] = chord_id  # Agregar el identificador único al resultado
        results[chord_id] = result

    # Actualizar el diccionario experiment_data con los resultados
    new_data = data.copy()
    new_data['results'] = results

    return new_data

def characteristics_1(chord: dict, chord_id: int, repeat: bool = False) -> None:
    """
    Extrae las clases de tono de un acorde.

    Parámetros:
    - chord (dict): Un diccionario con las claves "root" e "intervals", donde "root" es la nota raíz y "intervals" es una lista de intervalos.
    - repeat (bool): Si es True, mantiene las clases de tono repetidas. Si es False, elimina las clases de tono repetidas.

    Retorna:
    - Una lista de clases de tono.

    Nota:
    En la teoría de conjuntos de tono, generalmente se manejan conjuntos sin repeticiones. Sin embargo,
    si se desea conservar las repeticiones para un análisis o aplicación específica, se puede hacerlo con el parámetro `repeat`.
    """
    root = chord["root"]
    degree=chord["degree"]
    chord_pitches = [degree]
    val=0
    for interval in chord["intervals"]:
        val += interval
        val %= 12
        chord_pitches.append(val)

    #if not repeat:
        #chord_pitches = list(set(chord_pitches))
    feature_vector=chord_pitches
    result = {
        "chord": chord,
        "feature_vector": feature_vector,
        "chord_id": chord_id
    }
    return 


def inversion_to_frequencies(chord):
    """Calcula la inversión del acorde y convierte a frecuencias considerando octavas correctas."""
    A4_FREQ = 440  # Frecuencia de A4
    A4_NOTE = 9    # Valor numérico de A en el sistema de 12 semitonos
    A4_OCTAVE = 4  # Octava de A4

    reordered_sequence=inversion_from_bass(chord)

    # Inicia la octava para la primera nota basada en el bajo y ajusta según la secuencia
    octave = chord['octave']
    previous_note = chord['bass']  # Comienza con el bajo como referencia
    frequencies = []

    for note in reordered_sequence:
        if note < previous_note:  # Si la nota actual es menor que la anterior, aumenta la octava
            octave += 1
        frequency = A4_FREQ * 2 ** (((note + (octave - A4_OCTAVE) * 12) - A4_NOTE) / 12)
        frequencies.append(frequency)
        previous_note = note  # Actualiza la nota anterior para la siguiente iteración

    return frequencies

def dissmeasure_fixed_amp(fvec, fixed_amp=1, model='min'):
    sort_idx = np.argsort(fvec)
    fr_sorted = np.asarray(fvec)[sort_idx]

    Dstar = 0.24
    S1 = 0.0207
    S2 = 18.96

    C1 = 5
    C2 = -5

    A1 = -3.51
    A2 = -5.75

    idx = np.transpose(np.triu_indices(len(fr_sorted), 1))
    fr_pairs = fr_sorted[idx]

    Fmin = fr_pairs[:, 0]
    S = Dstar / (S1 * Fmin + S2)
    Fdif = fr_pairs[:, 1] - fr_pairs[:, 0]

    # Usando una amplitud fija en lugar de variables basadas en el modelo
    a = fixed_amp  # Amplitud constante para todos los pares
    SFdif = S * Fdif
    D = np.sum(a * (C1 * np.exp(A1 * SFdif) + C2 * np.exp(A2 * SFdif)))

    return D



def interval_histogram_with_dissmeasure(chord, chord_id):
    fixed_amp = 1
    # Genera la secuencia de notas con inversión basada en el bajo
    note_sequence = inversion_from_bass(chord)
    frequencies = inversion_to_frequencies(chord)  # Asume que esta es la función correcta para obtener frecuencias

    histogram = [0] * 11  # Histograma para intervalos
    dissmeasures = [0] * 11  # Vector para almacenar las disonancias por intervalo
    vector_test1 = [0] * 11  # Vector para la suma de histograma y disonancias

    # Calcular intervalos y disonancias para pares de notas
    for i in range(len(note_sequence) - 1):
        for j in range(i + 1, len(note_sequence)):
            interval = (note_sequence[j] - note_sequence[i]) % 12
            if interval > 0:  # Solo intervalos positivos
                histogram[interval - 1] += 1

                # Calcula la disonancia para el par de notas
                dissonance = dissmeasure_fixed_amp([frequencies[i], frequencies[j]], fixed_amp)
                dissmeasures[interval - 1] += dissonance

    # Calcula el vector_test1 como la suma de histogram y dissmeasures
    for i in range(len(histogram)):
        vector_test1[i] = histogram[i] * dissmeasures[i]

    result = {
        "chord": chord,
        "feature_vector": vector_test1,
        "chord_id": chord_id
    }

    return result

