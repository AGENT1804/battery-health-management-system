import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Preset battery data
battery_data = {
    'Cell Voltage': [3.4, 3.5, 3.6, 3.7, 3.8, 3.9],
    'Temperature': [25, 27, 23, 30, 25, 32],
    'Current': [5, 6, 4, 7, 5, 8],
    'State of Charge': [80, 85, 75, 90, 80, 95],
    'State of Health': [90, 85, 95, 80, 90, 75],
    'Overcurrent': [0, 0, 1, 0, 0, 0]
}

# Convert to DataFrame
battery_df = pd.DataFrame(battery_data)

# Split data into features (input) and targets (outputs)
X_soc_soh = battery_df[['Cell Voltage', 'Temperature', 'Current']]
y_soc = battery_df['State of Charge']
y_soh = battery_df['State of Health']
y_cell_voltage = battery_df['Cell Voltage']
y_overcurrent = battery_df['Overcurrent']

# Train SOC and SOH models
soc_model = np.polyfit(X_soc_soh['Cell Voltage'], y_soc, 1)  # Linear regression
soh_model = np.polyfit(X_soc_soh['Cell Voltage'], y_soh, 1)  # Linear regression

# Train cell voltage model (simple mean)
cell_voltage_model = np.mean(y_cell_voltage)

# Train overcurrent protection model (simple majority vote)
overcurrent_model = y_overcurrent.mode()[0]

# Predict SOC for test data
test_soc_voltage = np.array([3.6, 3.7])  # Test data for SOC prediction
y_pred_soc = np.polyval(soc_model, test_soc_voltage)

# Predict SOH for test data
test_soh_voltage = np.array([3.8, 3.9])  # Test data for SOH prediction
y_pred_soh = np.polyval(soh_model, test_soh_voltage)

# Predict cell voltage for test data (using mean of preset data)
y_pred_cell_voltage = np.full(len(test_soc_voltage), cell_voltage_model)

# Predict overcurrent for test data (using majority vote of preset data)
y_pred_overcurrent = np.full(len(battery_df), overcurrent_model)

# Plot actual and predicted SOC
plt.figure(figsize=(10, 5))
plt.scatter(X_soc_soh['Cell Voltage'], y_soc, color='blue', label='Actual SOC')
plt.plot(X_soc_soh['Cell Voltage'], np.polyval(soc_model, X_soc_soh['Cell Voltage']), color='red', label='Predicted SOC')
plt.xlabel('Cell Voltage')
plt.ylabel('State of Charge')
plt.title('Actual vs Predicted State of Charge')
plt.legend()
plt.show()

# Plot actual and predicted SOH
plt.figure(figsize=(10, 5))
plt.scatter(X_soc_soh['Cell Voltage'], y_soh, color='blue', label='Actual SOH')
plt.plot(X_soc_soh['Cell Voltage'], np.polyval(soh_model, X_soc_soh['Cell Voltage']), color='red', label='Predicted SOH')
plt.xlabel('Cell Voltage')
plt.ylabel('State of Health')
plt.title('Actual vs Predicted State of Health')
plt.legend()
plt.show()
