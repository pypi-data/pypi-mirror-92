from easyDL import Layer
import numpy as np

class Conv2D(Layer):
    """
    Conv2D(num_filters, kernel_size= 3, stride= 1)
    
    Conv2D Layer class.

    Attributes
    ----------
    num_filters : int
    kernel_size : int or tuple
        ex. 2 or (2, 2)
    stride : int
    input_shape: tuple
    """
    def __init__(self, num_filters, kernel_size= (3, 3), stride= 1, input_shape= None, padding= 'valid'):
        self.input_shape = input_shape          
        self.num_filters = num_filters
        self._kernel_size = kernel_size                    
        self._stride = stride
        self._padding = padding
        self.type = 'Conv2D'
    
    def __call__(self, image_dim):
        self.image_dim = image_dim            
        # self._weights = np.random.randn(*self._kernel_size, self.image_dim[-1], self.num_filters) * 0.1
        # self._biases = np.random.randn(self.num_filters) * 0.1
        scale = 1/np.maximum(1., (self.num_filters+self.image_dim[-1])/2.)
        limit = np.sqrt(3.0 * scale)
        self._weights = np.random.uniform(-limit, limit, size=(*self._kernel_size, self.image_dim[-1], self.num_filters))
        self._biases = np.random.uniform(-limit, limit, size=(self.num_filters))
        self.output_dim = self.calculate_output_dims(self.image_dim)
    
    def forward(self, input_val):
        """
        This function convolves `filters` over `images` using stride.
        Args:
            A_prev:  Activations/Input Data coming into the layer from previous layer
        """
        self._a_prev = np.array(input_val, copy=True)
        # print(input_val.shape)
        output_shape = self.calculate_output_dims(input_dims=self._a_prev.shape)
        n, h_in, w_in, _ = self._a_prev.shape
        _, h_out, w_out, _ = output_shape
        h_f, w_f, _, n_f = self._weights.shape
        pad = self.calculate_pad_dims()
        a_prev_pad = self.pad(self._a_prev, pad)
        output = np.zeros(output_shape)

        for i in range(h_out):
            for j in range(w_out):
                h_start = i * self._stride
                h_end = h_start + h_f
                w_start = j * self._stride
                w_end = w_start + w_f
        
                output[:, i, j, :] = np.sum(
                    a_prev_pad[:, h_start:h_end, w_start:w_end, :, np.newaxis] *
                    self._weights[np.newaxis, :, :, :],
                    axis=(1, 2, 3)
                )

        return output + self._biases
    
    def backward(self, dZ):
        """
        Backpropagation through a maxpooling layer. The gradients are passed through
        the indices of greatest value in the original maxpooling during the forward step.
        """
        _, h_out, w_out, _ = dZ.shape
        n, h_in, w_in, _ = self._a_prev.shape
        h_f, w_f, _, _ = self._weights.shape
        pad = self.calculate_pad_dims()
        a_prev_pad = self.pad(array=self._a_prev, pad=pad)
        output = np.zeros_like(a_prev_pad)

        self._db = dZ.sum(axis=(0, 1, 2)) / n
        self._dw = np.zeros_like(self._weights)
        
        for i in range(h_out):
            for j in range(w_out):
                h_start = i * self._stride
                h_end = h_start + h_f
                w_start = j * self._stride
                w_end = w_start + w_f
    
                output[:, h_start:h_end, w_start:w_end, :] = np.add(
                    output[:, h_start:h_end, w_start:w_end, :],
                    np.sum(
                        self._weights[np.newaxis, :, :, :, :] *
                        dZ[:, i:i+1, j:j+1, np.newaxis, :],
                        axis=4
                        ), casting= 'unsafe'
                    )
                
                self._dw += np.sum(
                    a_prev_pad[:, h_start:h_end, w_start:w_end, :, np.newaxis] *
                    dZ[:, i:i+1, j:j+1, np.newaxis, :],
                    axis=0
                )
                
        # print(np.sum(self._dw))
        self._dw /= n
        return output[:, pad[0]:pad[0]+h_in, pad[1]:pad[1]+w_in, :]
    
    def optimize(self, optimizer):
        """
        This function performs the gradient descent update
        Args:
            optimizer: optimizer.
        """
        self._weights, self._biases = optimizer.update(self._weights, self._biases, self._dw, self._db)
    
    def calculate_output_dims(self, input_dims):
        n, h_in, w_in, _ = input_dims
        h_f, w_f, _, n_f = self._weights.shape
        if self._padding == 'same':
            return n, h_in, w_in, n_f
        elif self._padding == 'valid':
            h_out = (h_in - h_f) // self._stride + 1
            w_out = (w_in - w_f) // self._stride + 1
            return n, h_out, w_out, n_f
        else:
            raise ValueError("Unsupported padding value: {}".format(self._padding))
    
    def calculate_pad_dims(self):
        if self._padding == 'same':
            h_f, w_f, _, _ = self._weights.shape
            return (h_f - 1) // 2, (w_f - 1) // 2
        elif self._padding == 'valid':
            return 0, 0
        else:
            raise ValueError(f"Unsupported padding value: {self._padding}")

    
    def pad(self, array, pad):
        return np.pad(array=array, 
                      pad_width=((0, 0), (pad[0], pad[0]), (pad[1], pad[1]), (0, 0)),
                      mode='constant')

