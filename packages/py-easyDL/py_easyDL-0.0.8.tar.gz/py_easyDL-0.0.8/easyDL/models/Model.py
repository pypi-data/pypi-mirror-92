import numpy as np
from easyDL.losses import BinaryCrossEntropy, MeanSquaredError, CategoricalCrossEntropy, SparseCategoricalCrossEntropy
from tqdm import tqdm
from time import sleep
import pickle
import easyDL
from .load_model import load_model
from os import remove
    
class Model:
    def __init__(self, layers = []):
        if len(layers) == 0:    
            self.layers = []
        else:
            self.layers = layers
        self.losses = []
        self.losses_val = []
        self.acc = []
        self.acc_val = []
        self.optimized_layers= ['Dense', 'Conv2D']
    
    def add(self, layer):
        self.layers.append(layer)
    
    def save(self, path):
        with open(path, 'wb') as file:
            pickle.dump(self, file)
    
    def _get_argmax(self, x):
        return np.argmax(x, axis= 0)
    
    def _normalization(self, x):
        z = x - np.mean(x)
        z = z / np.std(x) 
        return z
    # HEllO WORLD
    def _forward_pass(self, X):
        # Forward pass
        for i in range(len(self.layers)):
            forward = self.layers[i].forward(X)
            # print(f"{self.layers[i].type}, input: {X.shape}")
            X = forward
        return forward, X
    
    def _compute_loss(self, forward, Y):
        # print(forward)
        if self.loss_fn_name == 'binary_crossentropy':
            bce = BinaryCrossEntropy(forward, Y)
        elif self.loss_fn_name == 'categorical_crossentropy':
            bce = CategoricalCrossEntropy(forward, Y, self.num_classes)
        elif self.loss_fn_name == 'mse':
            bce = MeanSquaredError(forward, Y)
        elif self.loss_fn_name == 'sparse_categorical_crossentropy':
            bce = SparseCategoricalCrossEntropy(forward, Y)
        else:
            raise ValueError('No Loss functions with that name.')
        
        return bce
    
    def _predict(self, X_val):
        # X_val = np.transpose(X_val)
        # Forward pass
        forward_val, X = self._forward_pass(X_val)
        
        if self.loss_fn_name == 'binary_crossentropy':
            return forward_val, forward_val
        elif self.loss_fn_name == 'categorical_crossentropy' or self.loss_fn_name == 'sparse_categorical_crossentropy':
            return self._get_argmax(forward_val), forward_val
     
    def predict(self, X):
        # X = np.transpose(X)
        # Forward pass
        forward, X = self._forward_pass(X)
        
        if self.loss_fn_name == 'binary_crossentropy':
            return forward
        elif self.loss_fn_name == 'categorical_crossentropy' or self.loss_fn_name == 'sparse_categorical_crossentropy':
            return self._get_argmax(forward)
    
    def compile(self, loss, optimizer):
        self.loss_fn = loss
        self.optimizer = optimizer
    
    def train(self, X_train, Y_train, epochs, batch_size= 32, validation_data= None, verbose= False, restore_best_weights= False):
        self.batch_size = batch_size
        self.validation_data = validation_data
        
        if self.loss_fn == 'categorical_crossentropy':
            self.num_classes = len(set(Y_train))
            
        num_batches = X_train.shape[0] // self.batch_size
            
        num_optimized_layers = 0
        for i in range(len(self.layers)):
            layer = self.layers[i]
            if layer.type in self.optimized_layers:
                num_optimized_layers += 1
            
            if i == 0:
                if layer.input_shape is None:    
                    raise ValueError('First layer should have input shape')
                else:
                    if layer.type == 'Conv2D':
                        X_train = self._normalization(X_train)
                        layer.input_shape = (self.batch_size,*layer.input_shape)
                    layer(layer.input_shape)
                
            else:    
                layer(self.layers[i-1].output_dim)
        
        self.optimizer.set_num_layers(num_optimized_layers)
        
        self.best_val_acc = 0
        cached_model_path = easyDL.__file__.split('__init__')[0] + 'models/cached_model.pkl'
            
        for epoch in range(epochs):
            if verbose:
                if epoch % 1 == 0:
                    print('Epoch {}/{}:'.format(epoch+1, epochs))
            sleep(1)
            for i in tqdm(range(num_batches), position=0, leave=True):
                X = X_train[i*self.batch_size: (i+1) * self.batch_size]
                Y = Y_train[i*self.batch_size: (i+1) * self.batch_size]
                if self.layers[0].type == 'Dense':
                    X = np.transpose(X)
                loss, acc, val_loss, val_acc = self._run_epoch(X, Y, self.optimizer)
            
            self.losses.append(loss)
            self.acc.append(acc)
            
            if len(validation_data) != 0:
                self.losses_val.append(val_loss)
                self.acc_val.append(val_acc)
            
            if restore_best_weights:
                if val_acc > self.best_val_acc:
                    self.best_val_acc = val_acc
                    self.save(cached_model_path)
            
            if verbose:
                if epoch % 1 == 0:
                    print('\nLoss: {:.4f} \t Accuracy: {:.3f}'.format(loss, acc))
                    print('Val_Loss: {:.4f} \t Val_Accuracy: {:.3f}\n'.format(val_loss, val_acc))
        
        if restore_best_weights:
            print(self)
            self = load_model(cached_model_path)
            print(self)
            remove(cached_model_path)
            
    def _run_epoch(self, X, Y, opt):
        
        forward, X = self._forward_pass(X)

        # Validation Forward pass
        # for i in range(len(self.layers)):
        #     forward_val = self.layers[i].forward(X_val)
        #     X_val = forward_val
             
        # Compute loss and first gradient
        self.loss_fn_name = self.loss_fn
        bce = self._compute_loss(forward, Y)
        
        acc = 0
        if self.loss_fn_name == 'binary_crossentropy':
            acc = np.mean(np.around(forward).astype(np.int64) == Y)
        elif self.loss_fn_name == 'categorical_crossentropy' or self.loss_fn_name == 'sparse_categorical_crossentropy':
            index = self._get_argmax(forward)
            acc = np.mean(index.astype(np.int64) == Y)
        
        loss = bce.forward()
        
        gradient = bce.backward()
         

        
        # Backpropagation
        for i, _ in reversed(list(enumerate(self.layers))):
            layer = self.layers[i]
            gradient = layer.backward(gradient)
            if layer.type in self.optimized_layers:
                layer.optimize(opt)
        
        acc_val = 0
        loss_val = 0
        if self.validation_data is not None:
            X_val = self.validation_data[0]
            Y_val = self.validation_data[1]
            
        
            preds, forward_val = self._predict(X_val)
            acc_val = np.mean(preds == Y_val)
            bce_val = self._compute_loss(forward_val, Y_val)
            loss_val = bce_val.forward()
        
        return loss, acc, loss_val, acc_val