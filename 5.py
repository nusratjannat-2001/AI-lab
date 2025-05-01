import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split 
   
# pip install scikit-learn

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

model = Sequential([
    Dense(32, activation='relu', input_shape=(1,)),  # 1*32+32=64
    Dense(64, activation='relu'),                    # 32*64+64=2112
    Dense(128, activation='relu'),                   # 64*128+128=8320
    Dense(1)  # Output layer                         #128*1+1=129
])

# Display model summary
model.summary()
x = np.linspace(-20, 20, 1000)
y = 5*x**3 - 10*x**2 + 20*x + 10  # Example polynomial equation

# Normalize the data to the range [-1, 1]
x_normalized = (x - x.min()) / (x.max() - x.min()) * 2 - 1
y_normalized = (y - y.min()) / (y.max() - y.min()) * 2 - 1
x_train, x_temp, y_train, y_temp = train_test_split(x_normalized, y_normalized, test_size=0.1)
x_val, x_test, y_val, y_test = train_test_split(x_temp, y_temp, test_size=0.5)

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])

# Train the model
history = model.fit(x_train, y_train, epochs=50, validation_data=(x_val, y_val), batch_size=32)
#Evaluate the model on test data
test_loss, test_mae = model.evaluate(x_test, y_test)
print(f"Test Loss: {test_loss}, Test MAE: {test_mae}")

# Plot training vs validation MAE (mean absolute error)
plt.figure(figsize=(12, 6))

# Training vs Validation MAE
plt.subplot(1, 2, 1)
plt.plot(history.history['mae'], label='Training MAE')
plt.plot(history.history['val_mae'], label='Validation MAE')
plt.xlabel('Epochs')
plt.ylabel('Mean Absolute Error')
plt.title('Training vs Validation MAE')
plt.legend()

# Training vs Validation "Accuracy" (represented as 1 - normalized loss)
train_accuracy = 1 - np.array(history.history['loss']) / np.max(history.history['loss'])
val_accuracy = 1 - np.array(history.history['val_loss']) / np.max(history.history['val_loss'])

plt.subplot(1, 2, 2)
plt.plot(train_accuracy, label='Training Accuracy (1 - normalized loss)')
plt.plot(val_accuracy, label='Validation Accuracy (1 - normalized loss)')
plt.xlabel('Epochs')
plt.ylabel('Normalized Accuracy')
plt.title('Training vs Validation "Accuracy"')
plt.legend()

plt.tight_layout()
plt.show()

# -------------------- Actual Roots Calculation ---------------------
# Coefficients of the polynomial: 5x^3 - 10x^2 - 20x + 10
coeffs = [5, -10, -20, 10]
actual_roots = np.roots(coeffs)
real_roots = actual_roots[np.isreal(actual_roots)].real  # Filter only real roots

print("Actual Analytical Roots:", np.round(real_roots, 5))

# -------------------- Plot with Actual and Predicted Roots ---------------------
# Denormalize x for plotting
x_denorm = (x_normalized + 1) / 2 * (x.max() - x.min()) + x.min()

# Predict on the normalized x
y_pred = model.predict(x_normalized)

# Denormalize predicted y
y_actual = (y_pred.flatten() + 1) / 2 * (y.max() - y.min()) + y.min()

plt.figure(figsize=(10, 6))
plt.plot(x_denorm, y_actual, label='Predicted f(x)')
plt.axhline(0, color='black', linestyle='--', linewidth=1)

# -------------------- Find Predicted Roots ---------------------
# y_actual is already de-normalized predicted y-values from DNN
# x_denorm is de-normalized x-values
# Find where y crosses zero (approximate roots)
roots = x_denorm[np.isclose(y_actual, 0, atol=0.5)]  # you can adjust `atol` for sensitivity
print("Predicted Roots (from DNN):", np.round(roots, 5))


# Plot predicted roots
plt.scatter(roots, np.zeros_like(roots), color='green', label='Predicted Roots')

# Plot actual roots
for i, r in enumerate(real_roots):
    plt.axvline(r, color='red', linestyle='--', label='Actual Root' if i == 0 else "")

plt.xlabel('x')
plt.ylabel('f(x)')
plt.title('Predicted Polynomial Curve with Predicted & Actual Roots')
plt.legend()
plt.grid(True)
plt.show()