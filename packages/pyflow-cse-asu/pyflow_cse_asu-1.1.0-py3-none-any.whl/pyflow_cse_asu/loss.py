import numpy as np
class Loss:
  '''
  Class encapsulates the following loss functions: Categorical Crossentropy and Mean Squared Error.
  The class is meant to be used via the functions: loss, delta_loss.
  Attributes:
    loss_type: String indicates the type of the loss function required.
  '''
  def __init__(self,loss_type="categorical_crossentropy"):
    '''
    Sets the attributes.
    '''
    self.loss_type=loss_type
    #built-in functions
      #Probabilistic losses
      #1           
  def categorical_crossentropy (self, predection, label):
    '''
    Calculates the categorical crossentropy loss of a given set of predictions of certain learning process.
    Arguments:
      predection: Array of predictions.
      label: Array of labels.
    Returns:
      float representing the categorical crossentropy (log) loss. 
    '''
    sum=0

    for i in range(len(predection)):
      sum=sum-np.log(predection[i][label[i]])    
    return sum
    
  def delta_categorical_crossentropy(self, pred, label):
    '''
    Calculates the derivative of the categorical crossentropy loss with respect to its inputs.
    Arguments:
      predection: Array of predictions.
      label: Array of labels.
    Returns:
      Array representing the derivative of the categorical crossentropy (log) loss with respect to every (scaler) input
    '''
    delta=np.array(pred)
    delta[label]=-(1 - pred[label] )
    return delta 
  #Regression losses
  #1
  def MeanSquaredError(self, predection, label):
    '''
    Calculates the MSE loss of a given set of predictions of certain learning process.
    Arguments:
      predection: Array of predictions.
      label: Array of labels.
    Returns:
      float representing the MSE loss. 
    '''
    error = 0.5*np.mean(np.square(label- predection), axis=-1)
    return error 
  def delta_MeanSquaredError(self,predection, label):
    '''
    Calculates the derivative of the MSE loss with respect to its inputs.
    Arguments:
      predection: Array of predictions.
      label: Array of labels.
    Returns:
      Array representing the derivative of the MSE with respect to every (scaler) input
    '''
    delta=np.mean((label - predection), axis=-1)
    return delta
  
  def loss(self, predection, label):
    '''
    Single entry point to calculate the loss according to the attribute loos_type.
    Arguments:
      predection: Array of predictions.
      label: Array of labels.
    Returns:
      float representing the required loss. 
    '''
    if self.loss_type == "categorical_crossentropy":
      return self.categorical_crossentropy (predection, label)
    elif self.loss_type == "MeanSquaredError":
      return self.MeanSquaredError(predection, label)

  def delta_loss(self, predection, label):
    '''
    Single entry point to calculate the derivative of the loss with respect to its inputs according to the attribute loos_type.
    Arguments:
      predection: Array of predictions.
      label: Array of labels.
    Returns:
      Array representing the derivative of the loss with respect to every (scaler) input.
    '''
    if self.loss_type == "categorical_crossentropy":
      return self.delta_categorical_crossentropy (predection, label)
    elif self.loss_type == "MeanSquaredError":
      return self.delta_MeanSquaredError(predection, label)
  