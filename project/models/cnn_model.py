import tensorflow as tf
from tensorflow.keras import layers, models

def build_model(input_shape=(128, 128, 3), num_classes=3):
    """
    Build a CNN model for image classification.
    
    :param input_shape: Shape of the input images (height, width, channels).
    :param num_classes: Number of classes for classification.
    :return: A Keras model.
    """
    model = models.Sequential([
        # Convolutional layer block 1
        layers.Conv2D(64, (3, 3), activation='relu', input_shape=input_shape),
        layers.MaxPooling2D((2, 2)),
        # Convolutional layer block 2
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        # Convolutional layer block 3
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        # Dense layers for classification
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    
    return model

# Build the model
model = build_model()

# Model summary
model.summary()
