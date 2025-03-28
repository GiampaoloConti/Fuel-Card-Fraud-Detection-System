from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import matplotlib.pyplot as plt
import pandas as pd

# Load the data
data = pd.read_csv('data/processed/processed_transactions_with_random_frauds.csv')
data['delta_time_seconds'] = pd.to_timedelta(data['delta_time']).dt.total_seconds()

# Define features and labels
features = data.drop(columns=['delta_time', 'label'])
labels = data['label']

# Split the data
X_train_full, X_temp, y_train_full, y_temp = train_test_split(features, labels, test_size=0.3, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

# Scale the data
scaler = StandardScaler()
X_train_full = scaler.fit_transform(X_train_full)
X_val = scaler.transform(X_val)
X_test = scaler.transform(X_test)

# Train Random Forest Classifier
rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X_train_full, y_train_full)

# Train Neural Network
nn_model = Sequential([
    Dense(64, activation='relu', input_shape=(X_train_full.shape[1],)),
    Dense(32, activation='relu'),
    Dense(1, activation='sigmoid')
])
nn_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
nn_model.fit(X_train_full, y_train_full, epochs=10, batch_size=32, validation_data=(X_val, y_val))

# Evaluate Random Forest
y_test_rf_pred = rf_model.predict(X_test)
rf_accuracy = accuracy_score(y_test, y_test_rf_pred)
rf_cm = confusion_matrix(y_test, y_test_rf_pred)
rf_tn, rf_fp, rf_fn, rf_tp = rf_cm.ravel()
rf_fpr = rf_fp / (rf_fp + rf_tn)
rf_tpr = rf_tp / (rf_tp + rf_fn)  # Recall
rf_fnr = rf_fn / (rf_fn + rf_tp)
rf_tnr = rf_tn / (rf_tn + rf_fp)

# Evaluate Neural Network
y_test_nn_pred = (nn_model.predict(X_test) > 0.5).astype("int32")
nn_accuracy = accuracy_score(y_test, y_test_nn_pred)
nn_cm = confusion_matrix(y_test, y_test_nn_pred)
nn_tn, nn_fp, nn_fn, nn_tp = nn_cm.ravel()
nn_fpr = nn_fp / (nn_fp + nn_tn)
nn_tpr = nn_tp / (nn_tp + nn_fn)  # Recall
nn_fnr = nn_fn / (nn_fn + nn_tp)
nn_tnr = nn_tn / (nn_tn + nn_fp)

# Plot 1: Random Forest Metrics
fig, ax_rf = plt.subplots(figsize=(10, 6))
metrics_rf = [rf_accuracy, rf_fpr, rf_tpr, rf_fnr, rf_tnr]
labels_rf = ['Accuracy', 'FPR', 'Recall (TPR)', 'FNR', 'TNR']
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
ax_rf.bar(labels_rf, metrics_rf, color=colors)
ax_rf.set_xlabel('Metrics')
ax_rf.set_ylabel('Scores')
ax_rf.set_title('Random Forest Performance Metrics')
plt.show()

# Plot 2: Neural Network Metrics
fig, ax_nn = plt.subplots(figsize=(10, 6))
metrics_nn = [nn_accuracy, nn_fpr, nn_tpr, nn_fnr, nn_tnr]
labels_nn = ['Accuracy', 'FPR', 'Recall (TPR)', 'FNR', 'TNR']
ax_nn.bar(labels_nn, metrics_nn, color=colors)
ax_nn.set_xlabel('Metrics')
ax_nn.set_ylabel('Scores')
ax_nn.set_title('Neural Network Performance Metrics')
plt.show()

# Print results
print("Random Forest Classifier:")
print(f"Accuracy: {rf_accuracy}")
print(f"FPR: {rf_fpr}, Recall (TPR): {rf_tpr}, FNR: {rf_fnr}, TNR: {rf_tnr}")

print("\nNeural Network:")
print(f"Accuracy: {nn_accuracy}")
print(f"FPR: {nn_fpr}, Recall (TPR): {nn_tpr}, FNR: {nn_fnr}, TNR: {nn_tnr}")