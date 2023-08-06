import cv2
import numpy as np
import os

def load_single_image(path, target_size= None):
    """  
    load a single image as numpy array
    
    Attributes
    ----------
    path: str 
        absolute or relative file path to the image.
    target_size: tuple
    """
    image = cv2.imread(path)
    if target_size:
        image = cv2.resize(image, dsize= target_size[::-1], interpolation=cv2.INTER_CUBIC)
    image = image[np.newaxis, ...]
    return np.array(image)

def load_images_from_directory(dir_path, target_size):
    """  
    load all images located in the chosen path as numpy array
    
    Attributes
    ----------
    path: str 
        absolute or relative directory path of the images.
    target_size: tuple
    """
    if dir_path[-1] != '/':
        dir_path = dir_path + '/'
        
    images = []
    for filename in os.listdir(dir_path):
        if not filename.endswith('.jpg'):
            continue
        
        image = cv2.imread(dir_path + filename)        
        image = cv2.resize(image, dsize= target_size[::-1], interpolation=cv2.INTER_CUBIC)
        images.append(image)
    return np.array(images)

def load_images_from_classes_directory(parent_dir_path, target_size, shuffle= True):
    """  
    load all images located in the chosen path as numpy array
    
    Attributes
    ----------
    path: str 
        absolute or relative directory path of the images.
    target_size: tuple
    """
    if parent_dir_path[-1] != '/':
        parent_dir_path = parent_dir_path + '/'
    
    classes_dir = os.listdir(parent_dir_path)
    X = load_images_from_directory(parent_dir_path + classes_dir[0], target_size)
    Y = np.zeros((len(X),))
    for i in range(1, len(classes_dir)):
        images = load_images_from_directory(parent_dir_path + classes_dir[i], target_size)
        num_images = len(images)
        y_i = np.array([i]*num_images)           
        X = np.concatenate((X, images), axis= 0)
        Y = np.concatenate((Y, y_i), axis= 0)
    
    if shuffle:
        shuffler = np.random.permutation(len(Y))
        X = X[shuffler]
        Y = Y[shuffler]
    
    return X.astype(np.int16), Y.astype(np.int16)
