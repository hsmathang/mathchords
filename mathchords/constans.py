"""
Definiciones de Escalas Musicales

Este archivo contiene una lista de diccionarios, cada uno representando una escala musical
diferente. Las escalas se utilizan en la generación de acordes y la experimentación musical.

Estructura de cada diccionario de escala:
- name: Nombre de la escala musical.
- root: La nota raíz de la escala, donde 0 representa C y se incrementa cromáticamente.
- intervals: Lista de intervalos en semitonos que componen la escala desde la nota raíz.


"""

SCALES = [
    # Escala Mayor: Tradicionalmente asociada con música alegre y brillante.
    {"name": "Escala Mayor", "root": 0, "intervals": [0, 2, 4, 5, 7, 9, 11]},
    
    # Escala Menor Natural: Produce un sonido más melancólico, común en la música triste.
    {"name": "Escala Menor", "root": 0, "intervals": [0, 2, 3, 5, 7, 8, 10]},
    
    # Escala Pentatónica Mayor: Muy utilizada en géneros como el blues y el rock.
    {"name": "Escala Pentatónica Mayor", "root": 0, "intervals": [0, 2, 4, 7, 9]},
    
    # Escala Pentatónica Menor: Similar a la mayor pero con un carácter más melancólico.
    {"name": "Escala Pentatónica Menor", "root": 0, "intervals": [0, 3, 5, 7, 10]},
    
    # Escala Armónica Menor: Característica por su intervalo aumentado, útil para música clásica y jazz.
    {"name": "Escala Armónica Menor", "root": 0, "intervals": [0, 2, 3, 5, 7, 8, 11]},
    
    # Escala Melódica Menor: Utilizada en jazz para improvisación sobre acordes menores.
    {"name": "Escala Melódica Menor", "root": 0, "intervals": [0, 2, 3, 5, 7, 9, 11]},
    
    # Escala Dórica: Una variante menor con un sexto grado mayor, común en el jazz y la música funk.
    {"name": "Escala Dórica", "root": 0, "intervals": [0, 2, 3, 5, 7, 9, 10]},
    
    # Escala Frigia: Se destaca por su segundo grado menor, dándole un sonido distintivo, usado en flamenco.
    {"name": "Escala Frigia", "root": 0, "intervals": [0, 1, 3, 5, 7, 8, 10]},
    
    # Escala Lidia: Con un cuarto grado aumentado, proporciona un sonido "flotante" o "etéreo".
    {"name": "Escala Lidia", "root": 0, "intervals": [0, 2, 4, 6, 7, 9, 11]},
    
    # Escala Mixolidia: Un sonido mayor con un séptimo grado menor, común en la música rock y folk.
    {"name": "Escala Mixolidia", "root": 0, "intervals": [0, 2, 4, 5, 7, 9, 10]},
    
    # Escala Locria: El modo más oscuro debido a su quinta disminuida, raramente utilizado en su totalidad.
    {"name": "Escala Locria", "root": 0, "intervals": [0, 1, 3, 5, 6, 8, 10]},
    
    # Escala Alterada: Derivada del modo locrio, se utiliza para improvisación sobre acordes dominantes alterados.
    {"name": "Escala Alterada", "root": 0, "intervals": [0, 1, 3, 4, 6, 8, 10, 11]},
    {"name": "Escala Cromática", "root": 0, "intervals": list(range(12))}
]


PLOT_CONFIG =  {
    'colors': {
        'major': 'red',
        'minor': 'blue',
        'diminished': 'green',
        'unknown': 'orange'
    },


  'symbols':{
        'major': 'star-square',
        'minor': 'star-triangle-down',
        'diminished': 'circle',
        'unknown': 'asterisk'
    },
}
DO_chords = [
    {'name': 'C Major', 'octave': 4, 'bass': 0, 'root': 0, 'degree': 1, 'intervals': [4, 3]},
    {'name': 'C Minor', 'octave': 4, 'bass': 0, 'root': 0, 'degree': 1, 'intervals': [3, 4]},
    {'name': 'C Sus2', 'octave': 4, 'bass': 0, 'root': 0, 'degree': 1, 'intervals': [2, 5]},
    {'name': 'C Sus4', 'octave': 4, 'bass': 0, 'root': 0, 'degree': 1, 'intervals': [5, 2]},
    {'name': 'C Aug', 'octave': 4, 'bass': 0, 'root': 0, 'degree': 1, 'intervals': [4, 4]},
    {'name': 'C Dim', 'octave': 4, 'bass': 0, 'root': 0, 'degree': 1, 'intervals': [3, 3]},
    {'name': 'C Maj7', 'octave': 4, 'bass': 0, 'root': 0, 'degree': 1, 'intervals': [4, 3, 4]},
    {'name': 'C m7', 'octave': 4, 'bass': 0, 'root': 0, 'degree': 1, 'intervals': [3, 4, 3]},
    {'name': 'C 7', 'octave': 4, 'bass': 0, 'root': 0, 'degree': 1, 'intervals': [4, 3, 3]},
    {'name': 'C m7b5', 'octave': 4, 'bass': 0, 'root': 0, 'degree': 1, 'intervals': [3, 3, 4]},
    {'name': 'C mM7', 'octave': 4, 'bass': 0, 'root': 0, 'degree': 1, 'intervals': [3, 4, 4]},
    {'name': 'C 7#5', 'octave': 4, 'bass': 0, 'root': 0, 'degree': 1, 'intervals': [4, 4, 2]},
    {'name': 'C Dim7', 'octave': 4, 'bass': 0, 'root': 0, 'degree': 1, 'intervals': [3, 3, 3]}
]

