import json
import numpy as np
import cv2
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib

def load_drawings(filename, max_drawings=1000):
    """Load drawings from an NDJSON file until max_drawings is reached."""
    drawings = []
    with open(filename, 'r') as file:
        for i, line in enumerate(file):
            if i >= max_drawings:
                break
            drawings.append(json.loads(line))
    return drawings

def preprocess_drawing(drawing):
    """Convert a drawing to a binary image representation."""
    size = 256  # Define the size of the image
    img = np.zeros((size, size), dtype=np.uint8)
    for stroke in drawing['drawing']:
        points = zip(stroke[0], stroke[1])
        for (x1, y1), (x2, y2) in zip(points, points[1:]):
            cv2.line(img, (x1, y1), (x2, y2), 255, 2)
    return img

def extract_features(img):
    """Calculate Hu Moments which describe the shape from the image."""
    moments = cv2.moments(img)
    hu_moments = cv2.HuMoments(moments)
    return -np.sign(hu_moments) * np.log10(np.abs(hu_moments)).flatten()

def train_model(features, labels):
    """Train a Logistic Regression model using the given features and labels."""
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)
    model = LogisticRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, y_pred)}")
    joblib.dump(model, 'drawing_classifier.pkl')

def main():
    """Main function to load data, extract features, and train the model."""
    circles = load_drawings('path_to_circle.ndjson')
    squares = load_drawings('path_to_square.ndjson')
    
    circle_images = [preprocess_drawing(drawing) for drawing in circles]
    square_images = [preprocess_drawing(drawing) for drawing in squares]
    
    circle_features = [extract_features(img) for img in circle_images]
    square_features = [extract_features(img) for img in square_images]
    
    features = circle_features + square_features
    labels = [1] * len(circle_features) + [0] * len(square_features)
    
    train_model(features, labels)

if __name__ == '__main__':
    main()
