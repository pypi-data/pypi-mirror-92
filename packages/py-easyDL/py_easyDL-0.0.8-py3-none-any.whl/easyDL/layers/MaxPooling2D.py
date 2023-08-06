from easyDL import Layer
import numpy as np

class MaxPooling2D(Layer):
    """
    MaxPooling2D(pool_size= (2, 2), stride= 1)
    
    MaxPooling2D Layer class.

    Attributes
    ----------
    input_shape : int
        Dimensions of the input of the first layer of the network (Data dimensions).
    output_dim : int
        Output dimensions of the layer.
    """
    def __init__(self, pool_size= (2, 2), stride= 2):
        self._pool_size = pool_size
        
        if type(self._pool_size) != tuple:
            self._pool_size = (self._pool_size, self._pool_size)
        else:
            if len(self._pool_size) != 2:
                raise ValueError('pool_size must have 2 dimensions')
            else:
                if self._pool_size[0] != self._pool_size[1]:
                    raise ValueError('pool_size dimensions must be the same')
                    
        self._stride = stride
        self._a = None
        self._cache = {}
        self.type = 'MaxPooling2D'
    
    def __call__(self, input_dim):
        self.original_img_dim = input_dim
        self.output_dim = self._get_output_dim()
    
    def _get_output_dim(self):
        n, h_in, w_in, c = self.original_img_dim
        h_pool, w_pool = self._pool_size
        h_out = 1 + (h_in - h_pool) // self._stride
        w_out = 1 + (w_in - w_pool) // self._stride
        return (n, h_out, w_out, c)
        
    
    def forward(self, input_val):
        """
        This function performs the forwards propagation using activations from previous layer
        Args:
            A_prev:  Activations/Input Data coming into the layer from previous layer
        """
        self._a = np.array(input_val, copy=True)
        n, h_in, w_in, c = self._a.shape
        h_pool, w_pool = self._pool_size
        h_out = 1 + (h_in - h_pool) // self._stride
        w_out = 1 + (w_in - w_pool) // self._stride
        output = np.zeros((n, h_out, w_out, c))

        for i in range(h_out):
            for j in range(w_out):
                h_start = i * self._stride
                h_end = h_start + h_pool
                w_start = j * self._stride
                w_end = w_start + w_pool
                a_prev_slice = input_val[:, h_start:h_end, w_start:w_end, :]
                self._save_mask(x=a_prev_slice, cords=(i, j))
                output[:, i, j, :] = np.max(a_prev_slice, axis=(1, 2))
        return output
     
    def backward(self, dZ):
        """
        Backpropagation through a maxpooling layer. The gradients are passed through
        the indices of greatest value in the original maxpooling during the forward step.
        """
        output = np.zeros_like(self._a)
        _, h_out, w_out, _ = dZ.shape
        h_pool, w_pool = self._pool_size

        for i in range(h_out):
            for j in range(w_out):
                h_start = i * self._stride
                h_end = h_start + h_pool
                w_start = j * self._stride
                w_end = w_start + w_pool
                # output[:, h_start:h_end, w_start:w_end, :] += dZ[:, i:i + 1, j:j + 1, :] * self._cache[(i, j)]
                output[:, h_start:h_end, w_start:w_end, :] = \
                    np.add(output[:, h_start:h_end, w_start:w_end, :],
                           dZ[:, i:i + 1, j:j + 1, :] * self._cache[(i, j)], 
                           casting= 'unsafe')
        return output
    
    def _save_mask(self, x, cords):
        mask = np.zeros_like(x)
        n, h, w, c = x.shape
        x = x.reshape(n, h * w, c)
        idx = np.argmax(x, axis=1)

        n_idx, c_idx = np.indices((n, c))
        mask.reshape(n, h * w, c)[n_idx, idx, c_idx] = 1
        self._cache[cords] = mask
