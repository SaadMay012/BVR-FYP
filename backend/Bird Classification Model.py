import os
import librosa
import numpy as np
import pandas as pd
import sys
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

def extract_features(file_name):
    try:
        print(f"Processing file: {file_name}")
        audio, sample_rate = librosa.load(file_name, sr=None)  # Load with original sample rate
        zero_crossing_rate = np.mean(librosa.feature.zero_crossing_rate(y=audio).T, axis=0)
        rms_energy = np.mean(librosa.feature.rms(y=audio).T, axis=0)
        spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=audio, sr=sample_rate).T, axis=0)
        spectral_bandwidth = np.mean(librosa.feature.spectral_bandwidth(y=audio, sr=sample_rate).T, axis=0)
        spectral_rolloff = np.mean(librosa.feature.spectral_rolloff(y=audio, sr=sample_rate).T, axis=0)
        mfccs = np.mean(librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=13).T, axis=0)
        
        
        pitches, magnitudes = librosa.core.piptrack(y=audio, sr=sample_rate)
        pitch = np.mean(pitches[magnitudes > np.median(magnitudes)])
        
       
        rms_volume = np.mean(librosa.feature.rms(y=audio))

        features = np.hstack([zero_crossing_rate, rms_energy, spectral_centroid, spectral_bandwidth, spectral_rolloff, mfccs, pitch, rms_volume])
        return features
    except Exception as e:
        print(f"Error encountered while parsing file: {file_name}. Error: {e}")
        return None
    
output_csv = 'bird_voice_features.csv'

df = pd.read_csv(output_csv)

le = LabelEncoder()
df['label_encoded'] = le.fit_transform(df['label'])


X = df.drop(columns=['label', 'label_encoded'])
y = df['label_encoded']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

clf = RandomForestClassifier(n_estimators=100, random_state=42)

clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"Test Accuracy: {accuracy:.4f}")


new_file_path = sys.argv[1]                                 #'/home/anonymousje/Downloads/backend/backend/uploads/XC467432 - Asian Barred Owlet - Glaucidium cuculoides.mp3'
new_features = extract_features(new_file_path).reshape(1, -1)

prediction = clf.predict(new_features)
predicted_species = le.inverse_transform(prediction)

print(f"Predicted species: {predicted_species[0]}")
