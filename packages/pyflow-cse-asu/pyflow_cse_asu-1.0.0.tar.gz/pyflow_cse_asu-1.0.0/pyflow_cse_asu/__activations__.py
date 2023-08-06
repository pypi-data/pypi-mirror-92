class Activation:
  def __init__(self,activation="relu"):
    self.activation=activation

  def sigmoid(self,z):
      s = 1/(1+np.exp(-z))     
      return s
      
  def tanh(self,z):
      s = (np.exp(z)-np.exp(-z))/(np.exp(z)+np.exp(-z))    
      return s
      
  def relu(self,x):
      s = np.maximum(0,x)    
      return s

  def sigmoid_derivative(self,x):
      s = self.sigmoid(x)
      ds = s*(1-s)
      return ds

  def tanh_derivative(self,x):
      t = self.tanh(x)
      dt = 1-np.power(t,2)
      return dt
  
  def relu_derivative(self,x):
      return x>0     

  def softmax(self,x):
      exps=np.exp(x)
      return exps/np.sum(exps)

  def DerivativeFn(self,x):
      if self.activation=="relu":
        return  self.relu_derivative(x)
      elif self.activation=="tanh":
          return self.tanh_derivative(x)    
      elif self.activation=="sigmoid":
          return self.sigmoid_derivative(x)
      #elif self.activation=="softmax":
          #return self.softmax_derivative(x)
          
  def ActivationFn(self,x):
      if self.activation=="relu":
          return self.relu(x)
      elif self.activation=="tanh":
          return np.tanh(x)    
      elif self.activation=="sigmoid":
          return self.sigmoid(x)
      elif self.activation=="softmax":
          return self.softmax(x) 
