class Evaluation_metrics():
  def __init__(self,evaluation_type="accuracy",numberOfClasses=9,plot=0):
    self.evaluation_type=evaluation_type
    self.numberOfClasses=numberOfClasses
    self.plot=plot

  def calculate_matrix(self,predection ,label):
    epslion=0.000001
    label_series=pd.Series(label)
    predection_series=pd.Series( predection)
    df_M =pd.crosstab( predection_series,label_series)
    M=df_M.to_numpy()
    rows_sum= M.sum(axis=1)
    coulmns_sum=M.sum(axis=0)
    M=M.diagonal()
    precision=M/(rows_sum +epslion)  # what proportion of predicted positives is truly positive ?
    recall=M/(coulmns_sum+epslion)   # what proportion of actual positives is correctly classified ?
    F1=2*(precision*recall)/(precision+recall+epslion)
    final_M={"precision":precision,
                            "recall":recall,
                            "F1 Score":F1
                            }
    df=pd.DataFrame(final_M, columns = ['precision', 'recall','F1 Score'])
    precision=sum(precision)/len(precision)
    recall=sum(recall)/len(recall)
    F1=sum(F1)/len(F1)
    return precision , recall ,F1

  def plot_confusion_matrix(self,df_confusion, title='Confusion matrix', cmap=plt.cm.gray_r):
     plt.matshow(df_confusion, cmap=cmap) # imshow
     #plt.title(title)
     plt.colorbar()
     tick_marks = np.arange(len(df_confusion.columns))
     plt.xticks(tick_marks, df_confusion.columns, rotation=45)
     plt.yticks(tick_marks, df_confusion.index)
     #plt.tight_layout()
     plt.ylabel(df_confusion.index.name)
     plt.xlabel(df_confusion.columns.name)
     

  def confusion_matrix(self,predection ,label):
    label_series=pd.Series(label,name="Actual")
    predection_series=pd.Series( predection,name="predectied")
    df_confusion = pd.crosstab( predection_series,label_series)
    self.plot_confusion_matrix(df_confusion, title='Confusion matrix', cmap=plt.cm.gray_r)
 
  def accuracy (self,predection,label):
    accuracy=[]
    for i in range(len(predection)):      
        accuracy.append(predection[i]==label[i])
    return sum(accuracy)/len(predection)    

  def all_evaluation(self,predection,label):

    if (self.evaluation_type=="accuracy"):
      return self.accuracy (predection,label)

    elif (self.evaluation_type=="recall"):
      _,recall,_=self.calculate_matrix(predection ,label)
      return recall

    elif (self.evaluation_type=="precision"):
      precision,_,_=self.calculate_matrix(predection ,label)
      return precision

    elif (self.evaluation_type=="f1"):
      _,_,F1=self.calculate_matrix(predection ,label)
      return F1

    elif (self.evaluation_type=="confusion matrix"):
      self.confusion_matrix(predection ,label)


    else:
      if self.plot==1:
        self.confusion_matrix(predection ,label)

      precision,recall,f1=self.calculate_matrix(predection ,label)
      return  precision,recall,f1,self.accuracy (predection,label)