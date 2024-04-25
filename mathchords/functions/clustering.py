import plotly.graph_objects as go
import plotly.express as px
import ipywidgets as widgets
from IPython.display import display
import numpy as np


def classify_chord(intervals):
    """
    Classify the type of chord based on given intervals.

    Parameters:
    - intervals: List of integers representing the intervals of the chord.

    Returns:
    - A tuple containing the chord type and the corresponding symbol shape.
    """
    if intervals == [4, 3]:
        return 'major'
    elif intervals == [3, 4]:
        return 'minor'
    elif intervals == [3, 3]:
        return 'diminished'
    else:
        return 'unknown'

def get_chord_name(note_names, chord_data):
    """
    Construct the name of the chord from its data.

    Parameters:
    - note_names: List of note names corresponding to indices.
    - chord_data: Dictionary containing chord data.

    Returns:
    - String representing the chord name.
    """
    root_note = note_names[chord_data['root'] % 12]
    bass_note = note_names[chord_data['bass'] % 12]
    name=f"{root_note}"
    intervals=chord_data['intervals']
    if intervals[0]==3:
      if intervals[1]==3:
        name=name + "°"
      else: 
        name=name + "m"


    if bass_note!=root_note:
      name=name + f"/{bass_note}"
    return name

def prepare_marker_data(chord_ids, experiment_data, note_names, classify):
    """
    Prepare marker properties based on the chord data and classification choice.

    Parameters:
    - chord_ids: List of chord identifiers.
    - experiment_data: Dictionary containing the experiment data for each chord.
    - note_names: List of note names for mapping notes to names.
    - classify: Boolean indicating whether to classify the chords.

    Returns:
    - Tuple containing lists for colors, symbols, shapes, and hover text for the markers.
 
  
"""
    dict_from_file={}
    with open('/content/drive/MyDrive/2023/Trabajo de Grado/config.txt', 'r') as dict_file:
        dict_from_file = eval(dict_file.read())
    colors_dict=dict_from_file['colors']
    symbols_dict=dict_from_file['symbols']
    


    
    
    marker_colors = []
    marker_symbols = []
    hover_text = []
    
    for chord_id in chord_ids:
        chord_info = experiment_data['results'][chord_id]['chord']
        hover_text.append(generate_hover_text(chord_info, note_names))
        if classify:
            chord_type = classify_chord(chord_info.get('intervals', []))
            marker_colors.append(colors_dict[chord_type])
            marker_symbols.append(symbols_dict[chord_type])
        else:
            marker_colors.append('black')
            marker_symbols.append('circle')
            
    #marker_shapes = [symbols_dict.get(symbol,'star-triangle-down') for symbol in marker_symbols]
    #print(symbols_dict,marker_symbols)
    return marker_colors, marker_symbols , hover_text

def generate_hover_text(chord_info, note_names):
    """
    Generate the hover text for a chord marker.

    Parameters:
    - chord_info: Dictionary with the chord information.
    - note_names: List of note names corresponding to note indices.

    Returns:
    - String representing the hover text for a chord.
    """
    text_lines = [
        f"Root: {note_names[chord_info['root'] % 12]}",
        f"Bass: {note_names[chord_info['bass'] % 12]}",
        f"Octave: {chord_info.get('octave', 'N/A')}",
        f"Degree: {chord_info.get('degree', 'N/A')}",
        f"Intervals: {chord_info.get('intervals', [])}"
    ]
    return '<br>'.join(text_lines)

def create_scatter_plot(vector_encoding_MDS, text_for_display, hover_text, marker_colors, marker_symbols, show_root_names):
    """
    Create the initial scatter plot for chord representation.

    Parameters:
    - vector_encoding_MDS: numpy array with MDS encoding for the vectors.
    - text_for_display: List of strings for display on the markers.
    - hover_text: List of strings representing the hover text for each marker.
    - marker_colors: List of colors for the markers.
    - marker_shapes: List of shapes for the markers.
    - show_root_names: Boolean indicating whether to show root names on markers.

    Returns:
    - plotly.graph_objects.Scatter object representing the scatter plot.
    """
    scatter = go.Scatter(
        x=vector_encoding_MDS[:, 0],
        y=vector_encoding_MDS[:, 1],
        mode='markers+text' if show_root_names else 'markers',
        text=text_for_display,
        textposition='top center',
        hoverinfo='text',
        hovertext=hover_text,
        marker=dict(color=marker_colors, size=13, symbol=marker_symbols)
    )
    return scatter

def setup_layout(vector_encoding_MDS):
    """
    Set up the layout for the plot.

    Parameters:
    - vector_encoding_MDS: numpy array with MDS encoding for the vectors.

    Returns:
    - plotly.graph_objects.Layout object with the plot layout.
    """
    layout = go.Layout(
        title="Chord Representation (2D)",
        autosize=False,
        width=800,
        height=800,
        xaxis=dict(
            title="",
            range=[np.min(vector_encoding_MDS[:, 0]) - 1, np.max(vector_encoding_MDS[:, 0]) + 1],
            autorange=False
        ),
        yaxis=dict(
            title="",
            range=[np.min(vector_encoding_MDS[:, 1]) - 1, np.max(vector_encoding_MDS[:, 1]) + 1],
            autorange=False,
            scaleanchor="x",
            scaleratio=1
        ),
        showlegend=False
    )
    return layout

#def update_plot(fig, chord_ids, vector_encoding_MDS, hover_text):
    """
    Update plot based on the selected chord.

    Parameters:
    - fig: plotly.graph_objects.FigureWidget object representing the current figure.
    - chord_ids: List of chord identifiers.
    - vector_encoding_MDS: numpy array with MDS encoding for the vectors.
    - hover_text: List of strings representing the hover text for each marker.
    """
    # Inicializar un diccionario para mantener el color actual de cada acorde seleccionado
#    color_state = {chord_id: 'gray' for chord_id in chord_ids}  # Todos los puntos empiezan con 'gray'

   

#    def inner_update(change):
#        nonlocal color_state  # Referenciamos el diccionario definido fuera de la función
#        selected_chord_id = change['new']

        # Alternar el color del acorde seleccionado entre 'red' y 'blue'
#        current_color = color_state[selected_chord_id]
#        new_color = 'blue' if current_color == 'red' else 'red'
#        color_state[selected_chord_id] = new_color

        # Actualizar colores para todos los acordes
#        colors = [new_color if chord_id == selected_chord_id else 'gray' for chord_id in chord_ids]

#        with fig.batch_update():
#            fig.data[0].marker.color = colors

#    return inner_update

# Variable global para mantener el índice del último punto seleccionado
last_selected_index=None  # Asegúrate de definir esta variable fuera de tus funciones para mantener el estado

def update_plot(selected_chord_id, fig, chord_ids):
    global last_selected_index
    colors = list(fig.data[0].marker.color)  # Convertir a lista mutable

    # Reiniciar el color del último punto seleccionado a negro, si existe
    if last_selected_index is not None and last_selected_index < len(colors):
        colors[last_selected_index] = 'black'

    # Cambiar el color del acorde seleccionado a rojo
    if selected_chord_id in chord_ids:
        index = chord_ids.index(selected_chord_id)
        colors[index] = 'red'
        last_selected_index = index
    else:
        print("ID del acorde seleccionado no encontrado en la lista de acordes.")

    # Aplicar el cambio de color
    fig.data[0].marker.color = colors


def highlight_selected_chord(selected_chord_id, fig, chord_ids):
    # Obtener los colores y tamaños actuales de los marcadores
    colors = ['black'] * len(chord_ids)
    sizes = [10] * len(chord_ids)

    # Actualizar el color y tamaño del acorde seleccionado
    if selected_chord_id in chord_ids:
        index = chord_ids.index(selected_chord_id)
        colors[index] = 'red'  # Color para el punto seleccionado
        sizes[index] = 15      # Tamaño aumentado para el punto seleccionado

    # Aplicar los cambios a la figura
    with fig.batch_update():
        fig.data[0].marker.color = colors
        fig.data[0].marker.size = sizes





def plot_chords_with_selection(vector_encoding_MDS,matrix, chord_ids, experiment_data, show_root_names=False, classify=False):
    """
    Main function to plot chords with selection.

    Parameters:
    - vector_encoding_MDS: numpy array with MDS encoding for the vectors.
    - chord_ids: List of chord identifiers.
    - experiment_data: Dictionary containing the experiment data for each chord.
    - show_root_names: Boolean indicating whether to show root names on markers.
    - classify: Boolean indicating whether to classify the chords.
    """
    note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    marker_colors, marker_symbols, hover_text = prepare_marker_data(
        chord_ids, experiment_data, note_names, classify
    )
    text_for_display = [
        get_chord_name(note_names, experiment_data['results'][chord_id]['chord']) if show_root_names else ''
        for chord_id in chord_ids
    ]
   
    scatter = create_scatter_plot(vector_encoding_MDS, text_for_display, hover_text, marker_colors, marker_symbols, show_root_names)
    layout = setup_layout(vector_encoding_MDS)
    fig = go.FigureWidget(data=[scatter], layout=layout)



    # Initial color state for selection
    #current_color = ['red']
    
    # Omit the legend addition if not classifying

   


    chord_selector = widgets.Dropdown(
        options=[(f"Chord ID: {chord_id}, {get_chord_name(note_names, experiment_data['results'][chord_id]['chord'])}", chord_id) for chord_id in chord_ids],
        description='Chord ID:'
    )

    def on_chord_selected(change):
        highlight_selected_chord(change['new'], fig, chord_ids)
        
    # Configuración del observador en plot_chords_with_selection, cerca del final de la función
    # Dentro de plot_chords_with_selection, configura el observador así
    chord_selector.observe(on_chord_selected, names='value')


    #chord_selector.observe(update_plot(fig, chord_ids, vector_encoding_MDS, hover_text), names='value')
  

    names_matrix= [
                    get_chord_name(note_names, experiment_data['results'][chord_id]['chord']) if show_root_names else ''
                      for chord_id in chord_ids
                    ]
    print(names_matrix)

    fig2 = px.imshow(matrix,
                labels=dict(color="Dissimilarity"),
                x=names_matrix,
                y=names_matrix
               )
    #fig2.update_xaxes(side="top")
    fig2.update_layout(
        autosize=False,
        width=800,  # Ancho reducido para dejar espacio a la barra de colores
        height=800,  # Alto para mantener la ventana cuadrada
        margin=dict(
            l=50,  # Margen izquierdo
            r=50,  # Margen derecho (reducir si es necesario para acercar la barra de colores)
            b=100, # Margen inferior
            t=100, # Margen superior
            pad=4  # Padding entre los elementos de la figura
        ),
        coloraxis_colorbar=dict(
            x=1.1,  # Ajustar posición horizontal de la barra de colores (reducir para acercar)
            len=0.55
        )
    )
    #fig2.show()


    display(chord_selector)
    display(fig, fig2)

