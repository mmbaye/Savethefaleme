import tensorflow as tf
import os

def image_to_tensor(image_path):
    # Read the image file
    image_raw = tf.io.read_file(image_path)
    
    # Decode the image
    # TensorFlow automatically decodes to HWC format
    # Use `decode_image` for automatic format detection
    # Or use `decode_jpeg` or `decode_png` for specific formats
    image_tensor = tf.image.decode_image(image_raw, channels=3)
    
    # Optionally, convert to float values in [0, 1]
    image_tensor = tf.image.convert_image_dtype(image_tensor, tf.float32)
    
    return image_tensor

def convert_directory_images_to_tensors(directory_path):
    tensor_images = []
    for filename in os.listdir(directory_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(directory_path, filename)
            tensor_image = image_to_tensor(image_path)
            tensor_images.append(tensor_image)
    
    return tensor_images

# Usage example (commented out to prevent execution here)
directory_path = 'path/to/your/images'
tensors = convert_directory_images_to_tensors(directory_path)
print(f'Converted {len(tensors)} images to tensors.')

