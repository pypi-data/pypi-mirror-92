class Visualizer():
    '''
    Class encapsulates the visualization method that plots the loss and required evaluation metrics against the epoch number.
    Attributes:
        losses: List of calculated scaler losses occured at each epoch.
        accuracy: List of calculated scaler accuracies occured at each epoch.
        f1score: List of calculated scaler f1scores occured at each epoch.
        precision: List of calculated scaler precisions occured at each epoch.
        recall: List of calculated scaler recalls occured at each epoch. 
        mode: String represents the metric required to be visualized.
        metric_mode: List of metric values according to the passed mode.
    '''
    # This function is called when the training begins
    def __init__(self, mode= 'all'):
        '''
        Initializes the class attributes.
        '''
        # Initialize the lists for holding the logs, losses and metrics
        self.losses = []
        self.accuracy = []
        self.f1score = []
        self.precision = []
        self.recall = []
        self.mode = mode
        self.metric_mode = []


    # This function is called at the end of each epoch
    def on_epoch_end(self, logs={}):
        """
        Calculates and plots Precision, Recall, F1 score
        Arguments:
            logs: Dictionary consists of the metric mode name as dictionary key and its values as dictionary values. The dictionary also have special entry for the loss with the string "loss" as dictionary entry key and the value of the loss at the given epoch as dictionary entry value.
        """
        # Extract from the log
        if self.mode == "all":
            accuracy = logs['accuracy']
            f1score =logs['f1']
            recall =logs['recall']
            precision =logs['precision']
            self.accuracy.append(accuracy)
            self.f1score.append(f1score)
            self.precision.append(precision)
            self.recall.append(recall)
        else:
            metric_mode = logs[self.mode]
            self.metric_mode.append(metric_mode)
        loss=logs['loss']
        self.losses.append(loss)
    
        # Clear the previous plot
        if logs['type']=="train":
          clear_output(wait=True)
        N = np.arange(1, len(self.losses)+1)
        
        # You can chose the style of your preference

        plt.style.use("seaborn")
        plt.figure(figsize=(20,4))
        # Plot train loss, train acc, val loss and val acc against epochs passed
        plt.title("{} Loss over epoch number {}".format(logs['type'],len(self.losses)))
        plt.ylabel("Loss")
        plt.plot(N, self.losses,c='blue', marker='o', linestyle='solid')


        if (self.mode == "all"):
            fig, ax = plt.subplots(1,4, figsize=(20,4))
            ax = ax.ravel()
            ax[0].plot(N, self.precision, label = "Precision", c = 'red', marker='o', linestyle='solid')
            ax[1].plot(N, self.recall, label = "Recall", c = 'red', marker='o', linestyle='solid')
            ax[2].plot(N, self.f1score, label = "F1 score", c = 'red', marker='o', linestyle='solid')
            ax[3].plot(N, self.accuracy, label = "Precision", c = 'red', marker='o', linestyle='solid')
            ax[0].set_title("Precision at Epoch No. {}".format(len(self.losses)))
            ax[1].set_title("Recall at Epoch No. {}".format(len(self.losses)))
            ax[2].set_title("F1-score at Epoch No. {}".format(len(self.losses)))
            ax[3].set_title("Accuracy at Epoch No. {}".format(len(self.losses)))
            ax[0].set_xlabel("Epoch #")
            ax[1].set_xlabel("Epoch #")
            ax[2].set_xlabel("Epoch #")
            ax[3].set_xlabel("Epoch #")
            ax[0].set_ylabel("Precision")
            ax[1].set_ylabel("Recall")
            ax[2].set_ylabel("F1 score")
            ax[3].set_ylabel("Accuracy")
            ax[0].set_ylim(0,1)
            ax[1].set_ylim(0,1)
            ax[2].set_ylim(0,1)
            ax[3].set_ylim(0,1)
        else:
            fig, ax = plt.subplots(1,1, figsize=(12,4))
            ax.plot(N, self.metric_mode, label = self.mode, c = 'red', marker='o', linestyle='solid')
            ax.set_title("{} at Epoch No. {}".format(self.mode, len(self.losses)))
            ax.set_xlabel("Epoch #")
            ax.set_ylabel(self.mode)
            ax.set_ylim(0,1)
        plt.show()