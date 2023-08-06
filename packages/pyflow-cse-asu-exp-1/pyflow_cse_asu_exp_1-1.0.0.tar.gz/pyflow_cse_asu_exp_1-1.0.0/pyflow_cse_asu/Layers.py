class Layer:
    def __init__(self):
        self.input = None
        self.output = None

    # computes the output Y of a layer for a given input X
    def forward(self, input):
        raise NotImplementedError

    # computes dE/dX for a given dE/dY (and update parameters if any)
    def backward(self, output_error, learning_rate):
        raise NotImplementedError
        
class Dense(Layer):
   
    def __init__(self, input_units,output_units,activation="relu" ,learning_rate=0.01):
        # A dense layer is a layer which performs a learned affine transformation:
        # f(x) = <W*x> + b
        self.activation=activation
        self.learning_rate = learning_rate
        self.weights = np.random.normal(loc=0.0, 
                                        scale = np.sqrt(2/(input_units+output_units)), 
                                        size = (input_units,output_units))
        
        self.biases = np.zeros(output_units)
        self.D=1
        self.activationObject=Activation(activation)

    def forward(self,input):
        self.D=np.dot(input,self.weights) + self.biases
        return self.activationObject.ActivationFn(self.D)

    def backward(self,grad_output,input):
        # compute d f / d x = d f / d dense * d dense / d x

        # where d dense/ d x = weights transposed
        if self.activation!="softmax":
          grad_output=np.multiply(grad_output,self.activationObject.DerivativeFn(self.D))  
        grad_input = np.dot(self.weights,grad_output)
        
        # compute gradient w.r.t. weights and biases
        grad_weights=np.zeros((len(grad_output),len(input)))
        ip=input.reshape((input.size,1))
        gop=grad_output.reshape((grad_output.size,1))
        grad_weights=np.dot(ip,gop.T)      
        grad_biases = grad_output

        assert grad_weights.shape == self.weights.shape and grad_biases.shape == self.biases.shape

        self.weights = self.weights - self.learning_rate * grad_weights
        self.biases = self.biases - self.learning_rate * grad_biases

        return grad_input


class Conv():
    def __init__(self,filters=256,n_prev=3,kernel_size=11, strides=1, padding="valid",activation="tanh",learning_rate=0.0001):
 
        self.n_C=filters
        self.W = np.random.normal(loc=0.0,scale=1,size=(kernel_size,kernel_size,n_prev,filters))
        self.b=np.zeros(shape=(1,filters))
        self.stride=strides
        self.learning_rate=learning_rate
        self.padding=padding
        self.f=kernel_size
        self.n_C_prev=n_prev
        self.activation=activation
        self.pad=0
        self.D=1
        self.activationObject=Activation(activation)
 
    def conv_single_step(self,a_slice_prev, W, b):
    
      s = np.multiply(a_slice_prev, W) + b
      Z = np.sum(s)
      return Z

    def zero_pad(self,X):
 
        X_pad = np.pad(X, ((self.pad, self.pad), (self.pad,self.pad), (0, 0)), 'constant', constant_values=0)
        return X_pad
 
    def forward(self,A_prev):

        ( n_H_prev, n_W_prev, n_C_prev) = A_prev.shape
        
        if self.padding=="valid":
          self.pad=0
        else:
          self.pad=int((n_H_prev*(self.stride-1)+self.f-self.stride)/2)
        
        n_H = int((n_H_prev - self.f + 2 * self.pad) / self.stride) + 1
        n_W = int((n_W_prev - self.f + 2 * self.pad) / self.stride) + 1
        
        Z = np.zeros((n_H, n_W, self.n_C))
        A_prev_pad = np.pad(A_prev,((self.pad,self.pad),(self.pad,self.pad),(0,0)), 'constant', constant_values = (0,0))
        a_prev_pad = A_prev_pad  
        for h in range(n_H):                           # loop over vertical axis of the output volume
            for w in range(n_W):                       # loop over horizontal axis of the output volume
                for c in range(self.n_C):                   # loop over channels (= #filters) of the output volume
                    # Find the corners of the current "slice" (≈4 lines)
                    vert_start = h * self.stride
                    vert_end = vert_start + self.f
                    horiz_start = w * self.stride
                    horiz_end = horiz_start + self.f
                    # Use the corners to define the (3D) slice of a_prev_pad (See Hint above the cell). (≈1 line)
                    a_slice_prev = a_prev_pad[vert_start:vert_end, horiz_start:horiz_end, :]
                    # Convolve the (3D)11 slice with the correct filter W and bias b, to get back one output neuron. (≈1 line)
                    Z[ h, w, c] = self.conv_single_step(a_slice_prev, self.W[:,:,:,c], self.b[:,c])
        # Making sure your output shape is correct
        assert(Z.shape == (n_H, n_W, self.n_C))  
        # Save information in "cache" for the backprop
        self.D=Z
        A=self.activationObject.ActivationFn(Z)   
        return A

    def backward(self,dA, A_prev):
 
        dZ=np.multiply(dA,self.activationObject.DerivativeFn(self.D))
        (n_H_prev, n_W_prev, n_C_prev) = A_prev.shape
        ( n_H, n_W, n_C) = dZ.shape
        
        # Initialize dA_prev, dW, db with the correct shapes
        dA_prev = np.zeros((n_H_prev, n_W_prev, n_C_prev))                 
        dW = np.zeros((self.f, self.f, n_C_prev, n_C))
        db = np.zeros(( 1, n_C))
 
        # Pad A_prev and dA_prev
        #if self.padding=="valid":
        A_prev_pad = self.zero_pad(A_prev)
        dA_prev_pad = self.zero_pad(dA_prev)
        
        # select ith training example from A_prev_pad and dA_prev_pad
        a_prev_pad = A_prev_pad
        da_prev_pad = dA_prev_pad

        for h in range(n_H):                   # loop over vertical axis of the output volume
            for w in range(n_W):               # loop over horizontal axis of the output volume
                for c in range(n_C):           # loop over the channels of the output volume
                    
                    # Find the corners of the current "slice"
                    vert_start = h * self.stride
 
                    vert_end = vert_start + self.f
                    horiz_start = w * self.stride
 
                    horiz_end = horiz_start + self.f
                    
                    # Use the corners to define the slice from a_prev_pad
                    a_slice = a_prev_pad[vert_start:vert_end, horiz_start:horiz_end, :]
                    # Update gradients for the window and the filter's parameters using the code formulas given above
                    da_prev_pad[vert_start:vert_end, horiz_start:horiz_end, :] += self.W[:,:,:,c] * dZ[h, w, c]
                    #update each filter c with the gradient in the index h and w of the dZ as each filter parameter is now affected by the gradient of each element gradient in Z 
                    dW[:,:,:,c] += a_slice * dZ[h, w, c]
                    db[:,c] += dZ[h, w, c]
                    
        if self.padding=="valid":
           dA_prev=da_prev_pad
        else:
           dA_prev=da_prev_pad[self.pad:-self.pad, self.pad:-self.pad, :]

        assert(dA_prev.shape == (n_H_prev, n_W_prev, n_C_prev))

        self.W=self.W-self.learning_rate*dW
        self.b=self.b-self.learning_rate*db
        return dA_prev

class Pool(Layer):
    def __init__(self,pool_size=2,n_prev=3, strides=2, padding="valid", mode = "max"):

        self.f=pool_size
        self.n_prev=n_prev
        self.stride=strides
        self.padding=padding
        self.pad=0
        self.mode=mode

    def forward(self ,A_prev):
       
        (n_H_prev, n_W_prev, n_C_prev) = A_prev.shape 
        # Define the dimensions of the output

        if self.padding=="valid":
          self.pad=0
        else:
          self.pad=int((n_H_prev*(self.stride-1)+self.f-self.stride)/2)

        n_H = int(1 + (n_H_prev - self.f) / self.stride)
        n_W = int(1 + (n_W_prev - self.f) / self.stride)
        n_C = n_C_prev
        
        # Initialize output matrix A
        A = np.zeros((n_H, n_W,n_C))              
        for h in range(n_H):                     # loop on the vertical axis of the output volume
            for w in range(n_W):                 # loop on the horizontal axis of the output volume
                for c in range (n_C):            # loop over the channels of the output volume
                    
                    # Find the corners of the current "slice" (≈4 lines)
                    vert_start = h * self.stride
                    vert_end = vert_start + self.f
                    horiz_start = w * self.stride
                    horiz_end = horiz_start + self.f
                    
                    # Use the corners to define the current slice on the ith training example of A_prev, channel c. (≈1 line)
                    a_prev_slice = A_prev[vert_start:vert_end, horiz_start:horiz_end, c]
                    # Compute the pooling operation on the slice. Use an if statment to differentiate the modes. Use np.max/np.mean.

                    if self.mode == "max":
                        A[h, w, c] = np.max(a_prev_slice)
                    elif self.mode == "average":
                        A[h, w, c] = np.mean(a_prev_slice)
        
        # Making sure your output shape is correct
        assert(A.shape == (n_H, n_W, n_C))

        return A

    def create_mask_from_window(self ,x):

        mask = x == np.max(x) 
        return mask

    def distribute_value(self ,dz, shape):

        (n_H, n_W) = shape
        # Compute the value to distribute on the matrix
        average = dz / (n_H * n_W)       
        # Create a matrix where every entry is the "average" value 
        a = np.ones(shape) * average   
        return a

    def backward(self ,dA,A_prev):

        n_H_prev, n_W_prev, n_C_prev = A_prev.shape
        n_H, n_W, n_C = dA.shape
        # Initialize dA_prev with zeros 
        dA_prev = np.zeros(A_prev.shape)
        # select training example from A_prev
        a_prev = A_prev
        for h in range(n_H):                   # loop on the vertical axis
            for w in range(n_W):               # loop on the horizontal axis
                for c in range(n_C):           # loop over the channels (depth)
                    # Find the corners of the current "slice" 
                    vert_start = h
                    vert_end = vert_start + self.f
                    horiz_start = w
                    horiz_end = horiz_start + self.f
  
                    # Compute the backward propagation in both modes.
                    if self.mode == "max":
                        # Use the corners and "c" to define the current slice from a_prev 
                        a_prev_slice = a_prev[vert_start:vert_end, horiz_start:horiz_end, c]
                        # Create the mask from a_prev_slice 
                        mask = self.create_mask_from_window(a_prev_slice)
                        # Set dA_prev to be dA_prev + (the mask multiplied by the correct entry of dA) 
                        #update the element with the max value
                        dA_prev[ vert_start:vert_end, horiz_start:horiz_end, c] += np.multiply(mask, dA[ h, w, c])
                        
                    elif self.mode == "average":
                        # Get the value a from dA 
                        da = dA[h, w, c]
                        # Define the shape of the filter as fxf 
                        shape = (self.f,self.f)
                        # Distribute it to get the correct slice of dA_prev. i.e. Add the distributed value of da. 
                        dA_prev[vert_start:vert_end, horiz_start:horiz_end, c] += self.distribute_value(da, shape)
        
        assert(dA_prev.shape == A_prev.shape)
        
        return dA_prev       