from tensorflow.keras.preprocessing.image import ImageDataGenerator

def create_data_generators(train_dir, val_dir, test_dir, target_size=(128, 128), batch_size=32):
    """
    Create data generators for training, validation, and test datasets with data augmentation applied to the training data.
    
    :param train_dir: Directory with training data.
    :param val_dir: Directory with validation data.
    :param test_dir: Directory with test data.
    :param target_size: Tuple specifying the image size to resize.
    :param batch_size: Number of samples per gradient update.
    :return: A tuple (train_generator, validation_generator, test_generator).
    """
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )

    test_datagen = ImageDataGenerator(rescale=1./255)  # Note: Do not augment validation/test data
    
    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=target_size,
        batch_size=batch_size,
        class_mode='sparse'  # Use 'sparse' for integer labels
    )

    validation_generator = test_datagen.flow_from_directory(
        val_dir,
        target_size=target_size,
        batch_size=batch_size,
        class_mode='sparse'
    )

    test_generator = test_datagen.flow_from_directory(
        test_dir,
        target_size=target_size,
        batch_size=batch_size,
        class_mode='sparse'
    )

    return train_generator, validation_generator, test_generator

# Assuming your model is defined in 'model'
# And assuming you've set your directories: train_dir, val_dir, test_dir

train_generator, validation_generator, test_generator = create_data_generators(train_dir, val_dir, test_dir)

history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // train_generator.batch_size,
    epochs=50,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // validation_generator.batch_size
)

# Assuming 'model' is your CNN model defined earlier
# And 'train_generator', 'validation_generator' are defined using the create_data_generators function

epochs = 30  # You can adjust this based on your computational resources and how the model performs

history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // train_generator.batch_size,
    epochs=epochs,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // validation_generator.batch_size
)
