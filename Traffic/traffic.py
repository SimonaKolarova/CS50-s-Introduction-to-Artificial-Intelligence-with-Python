import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Loads image data from directory `data_dir`, which is assumed to contain
    one directory named after each category and the corresponding image files.

    Returns tuple `(images, labels)`. `images` is a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` is
    a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """

    # Initiate lists
    images = []
    labels = []

    main_dir = os.path.abspath(os.curdir)

    for i in range(NUM_CATEGORIES):
        os.chdir(os.path.join(data_dir, str(i)))  # Open directory i
        dir_images = os.listdir()  # Create a list of all images in directory

        for j in range(len(dir_images)):
            image = cv2.imread(dir_images[j])  # Read image from file
            image = tf.keras.preprocessing.image.img_to_array(image)  # Transform image to numpy array
            image = tf.image.resize(image, (IMG_WIDTH, IMG_HEIGHT))  # Reshape image to 30 x 30 px
            image = image/255  # Normalize image RGB values
            images.append(image) 
            labels.append(i)

        os.chdir(main_dir)
 
    return (images, labels)

def get_model():
    """
    Returns a compiled convolutional neural network model.
    """

    # Create a convolutional neural network
    model = tf.keras.models.Sequential([

        tf.keras.layers.Conv2D(32, (3,3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),  # Convolutional layer with 32 filters of a 3 x 3 kernel

        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),  # Max-pooling layer with a 2 x 2 pool size

        tf.keras.layers.Conv2D(64, (3, 3), activation="relu"),  # Convolutional layer with 64 filters of a 3 x 3 kernel
        
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),  # Max-pooling layer with a 2 x 2 pool size

        tf.keras.layers.Flatten(),  # Flatten units

        tf.keras.layers.Dense(256, activation="relu"),  # Hidden layer with 256 neurons

        tf.keras.layers.Dropout(0.25),  # Dropout layer with a rate of 0.25

        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax") # Output layer with an output unit for each image category
    ])

    # Compile model
    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model

if __name__ == "__main__":  
    main()