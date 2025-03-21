import json

def load_drawings(filename):
    drawings = []
    with open(filename, 'r') as file:
        for line in file:
            drawings.append(json.loads(line))
    return drawings

# Example usage with a local path
squares = load_drawings('C:/Users/wonto/Downloads/QuickDrawData/full_simplified_square.ndjson')
circles = load_drawings('C:/Users/wonto/Downloads/QuickDrawData/full_simplified_circle.ndjson')

import matplotlib.pyplot as plt

def plot_drawing(drawing):
    for stroke in drawing['drawing']:
        x, y = stroke[0], stroke[1]
        plt.plot(x, y, marker='.')
    plt.gca().invert_yaxis() 
    plt.axis('off')
    plt.show()

# Plot the first square and circle
plot_drawing(squares[0])
plot_drawing(circles[0])
