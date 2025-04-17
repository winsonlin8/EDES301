import json
import numpy as np
import cv2
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

def load_drawings(filename, max_drawings=1000):
    drawings = []
    with open(filename, 'r') as file:
        for i, line in enumerate(file):
            if i >= max_drawings:
                break
            drawings.append(json.loads(line))
    return drawings

def preprocess_drawing(drawing):
    size = 256
    img = np.zeros((size, size), dtype=np.uint8)
    for stroke in drawing['drawing']:
        points = list(zip(stroke[0], stroke[1]))
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            cv2.line(img, (x1, y1), (x2, y2), 255, 2)
    return img

def extract_features(img):
    moments = cv2.moments(img)
    hu_moments = cv2.HuMoments(moments).flatten()
    scaled_hu_moments = -np.sign(hu_moments) * np.log10(np.abs(hu_moments) + 1e-10)
    return scaled_hu_moments

def train_model(features, labels, model_path):
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")

def main():
    quickdraw_dir = 'C:/Users/wonto/Downloads/QuickDrawData'
    model_output_path = os.path.join(quickdraw_dir, 'drawing_classifier.pkl')

    circles = load_drawings(os.path.join(quickdraw_dir, 'full_simplified_circle.ndjson'))
    squares = load_drawings(os.path.join(quickdraw_dir, 'full_simplified_square.ndjson'))

    circle_images = [preprocess_drawing(d) for d in circles]
    square_images = [preprocess_drawing(d) for d in squares]

    circle_features = [extract_features(img) for img in circle_images]
    square_features = [extract_features(img) for img in square_images]

    features = circle_features + square_features
    labels = [1] * len(circle_features) + [0] * len(square_features)

    print("Final feature shape:", np.array(features).shape)
    train_model(features, labels, model_output_path)

if __name__ == '__main__':
    main()
