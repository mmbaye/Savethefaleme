import os
import numpy as np
from skimage.io import imread
from skimage.transform import resize
from sklearn.model_selection import train_test_split
import tensorflow as tf

def load_and_preprocess_image(path, target_size=(128, 128)):
    """
    Load an image file and preprocess it for model training.
    :param path: Path to the image file.
    :param target_size: A tuple specifying the target image size.
    :return: Preprocessed image.
    """
    image = imread(path)
    image_resized = resize(image, target_size, anti_aliasing=True)
    image_normalized = image_resized / 255.0  # Normalize to [0, 1]
    return image_normalized

def prepare_datasets(data_directory, target_size=(128, 128), test_size=0.2, val_size=0.2):
    """
    Prepare training, validation, and test datasets from the image directory.
    :param data_directory: Directory where the image data is stored.
    :param target_size: Target size for each image.
    :param test_size: Fraction of data to be used as the test set.
    :param val_size: Fraction of data to be used as the validation set.
    :return: train, validation, and test datasets.
    """
    images = []
    labels = []

    # Assuming subdirectories in 'data_directory' are class names
    for class_id, class_name in enumerate(os.listdir(data_directory)):
        class_dir = os.path.join(data_directory, class_name)
        for image_file in os.listdir(class_dir):
            image_path = os.path.join(class_dir, image_file)
            image = load_and_preprocess_image(image_path, target_size)
            images.append(image)
            labels.append(class_id)
    
    images = np.array(images)
    labels = np.array(labels)

    # Splitting dataset into train, validation, and test sets
    X_train, X_test, y_train, y_test = train_test_split(images, labels, test_size=test_size, random_state=42)
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=val_size, random_state=42)

    return (X_train, y_train), (X_val, y_val), (X_test, y_test)

# Example usage
data_directory = "path/to/your/data"
(X_train, y_train), (X_val, y_val), (X_test, y_test) = prepare_datasets(data_directory)

print("Training data shape:", X_train.shape)
print("Validation data shape:", X_val.shape)
print("Test data shape:", X_test.shape)
