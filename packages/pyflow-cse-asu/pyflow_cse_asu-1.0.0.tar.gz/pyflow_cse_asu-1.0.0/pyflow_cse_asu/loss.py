class Loss:
  def __init__(self,loss_type="categorical_crossentropy"):
    self.loss_type=loss_type
    #built-in functions
      #Probabilistic losses
      #1           
  def categorical_crossentropy (self,predection, label):
    sum=0

    for i in range(len(predection)):
      sum=sum-np.log(predection[i][label[i]])    
    return sum
    
  def delta_categorical_crossentropy(self,pred,label):
      delta=np.array(pred)
      delta[label]=-(1 - pred[label] )
      return delta 
  #Regression losses
  #1
  def MeanSquaredError(self,predection, label):
    error=0.5*np.mean(np.square(y_true - y_pred), axis=-1)
    return  erro 
  def delta_MeanSquaredError(self,predection, label):
    delta=np.mean((y_true - y_pred), axis=-1)
    return delta
  
  #called functions
  def loss(self,predection, label):
      if self.loss_type == "categorical_crossentropy":
        return self.categorical_crossentropy (predection, label)
      elif self.loss_type == "MeanSquaredError":
        return self.MeanSquaredError(predection, label)

  def delta_loss(self,predection, label):
       if self.loss_type == "categorical_crossentropy":
        return self.delta_categorical_crossentropy (predection, label)
       elif self.loss_type == "MeanSquaredError":
        return self.delta_MeanSquaredError(predection, label)
      