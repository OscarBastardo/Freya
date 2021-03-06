
# Loss imports
from freya.loss import BinaryCrossEntropy, MeanSquaredError
from freya.layers import *

class Model:
    """Model.

    A class to create a model. The model currently supports only sequential
    connections. Networks that require skip-connections cannot be built.

    Example
    -------
    >>> model = Model()
    >>> model.add(Linear(2,5))
    >>> model.add(ReLU(5))
    >>> model.add(Linear(5,2))
    >>> model.add(Sigmoid(2))
    >>> model.train(X, Y, 0.05, 400, "BinaryCrossEntropy, verbose=True")
    >>> model.predict(X)

    """
    def __init__(self):
        self.layers = []
        self.loss = []
    
    def add(self, layer):
        """Adds.
        
        Adds a new layer to the model.
        
        Parameters
        ----------
        layer : freya.Layer
            A freya layer to add to the model.
        """
        self.layers.append(layer)
    
    def predict(self, X):
        """Predicts.
        
        Given a set of data X, this function makes a prediction of X.
        
        Parameters
        ----------
        X : numpy.Array
            Data to make the predictions.
        
        Returns
        -------
        forward : numpy.Array
            Prediction for the given dataset.
        
        """
        # Forward pass
        for i, _ in enumerate(self.layers):
            forward = self.layers[i].forward(X)
            X = forward
            
        return forward
    
    def train(
        self, 
        X_train, 
        Y_train, 
        learning_rate, 
        epochs, 
        loss_function, 
        verbose=False
    ):
        """Trains.
        
        Fits the model using the given parameters.
        
        Parameters
        ----------
        X_train : numpy.Array
            Training data. Must match the input size of the first layer.
        Y_train : numpy.Array
            Training labels.
        learning_rate : float
            Number of epochs to train the model
        epochs : int
            asdad
        loss_function : str
            Chosen function to compute loss.
            
        """
        for epoch in range(epochs):
            loss = self._run_epoch(X_train, Y_train, learning_rate, loss_function)
            
            if verbose:
                if epoch % 50 == 0:
                    print(f'Epoch: {epoch}. Loss: {loss}')
    
    def _run_epoch(self, X, Y, learning_rate, loss_function):
        """Runs epoch.
        
        Helper function of train procedure.
        
        Parameters
        ----------
        X_train : numpy.Array
            Training data. Must match the input size of the first layer.
        Y_train : numpy.Array
            Training labels.
        learning_rate : float
            Number of epochs to train the model
        epochs : int
            asdad
        loss_function : str
            Chosen function to compute loss.
        
        Returns
        -------
        error : float
            Model error in this epoch.
        
        """
        # Forward pass
        for i, _ in enumerate(self.layers):
            forward = self.layers[i].forward(input_val=X)
            X = forward
            
        # Compute loss and first gradient
        if loss_function == "BinaryCrossEntropy":
            loss_f = BinaryCrossEntropy(forward, Y)
        elif loss_function == "MeanSquaredError":
            loss_f = MeanSquaredError(forward, Y)
        else:
            raise ValueError(f"{loss_function} is not supported.")
            
        error = loss_f.forward()
        gradient = loss_f.backward()
        
        self.loss.append(error)
        
        # Backpropagation
        for i, _ in reversed(list(enumerate(self.layers))):
            if self.layers[i].type != 'Linear':
                gradient = self.layers[i].backward(gradient)
            else:
                gradient, dW, dB = self.layers[i].backward(gradient)
                self.layers[i].optimize(dW, dB, learning_rate)
                
        return error