import numpy as np
from net import *
from Evaluation import *
class Model(Net):

  __slots__ = ['epochs_no','no_of_classes','evaluate','train_strategy']

  def __init__(self, layers, loss):

    super().__init__(layers, loss)
    self.epochs_no = 0
    self.no_of_classes = 0
    self.evaluate = Evaluation()

  def train_by_epochs(self,X_train,Y_train,X_validation,Y_validation,epochs): 

    Y_train = Y_train.astype(int)
    Y_validation = Y_validation.astype(int)

    self.epochs_no = epochs
    print("start training ...")
    
    pred_training_np = np.empty((0))
    losses_training_np = np.empty((0))
    pred_validation_np = np.empty((0))
    losses_validation_np = np.empty((0))

    for epoch_idx in range(self.epochs_no):

      print("Epoch no. %d" % epoch_idx)

      #validation 
      out_validation = super().forward(X_validation)

      #prediction of validation data
      pred_validation = np.argmax(out_validation,axis=1)
      pred_validation_np = np.append(pred_validation_np,pred_validation,axis=0)

       # losses of validation data
      loss_validation = super().loss(out_validation, Y_validation)
      # print(f"loss.shape : {loss_training.shape}")
      losses_validation_np = np.append(losses_validation_np,[loss_validation], axis=0)

      print(f"Loss at epoch no.{epoch_idx} = {loss_validation}")
      print("__________________________________")

      out = super().__call__(X_train)
      self.no_of_classes = int(out.shape[1])
      
      # prediction of training data 
      pred_training = np.argmax(out,axis=1)
      pred_training_np = np.append(pred_training_np,pred_training,axis=0)

      # losses of training data
      loss_training = super().loss(out, Y_train)
      # print(f"loss.shape : {loss_training.shape}")
      losses_training_np = np.append(losses_training_np,[loss_training], axis=0)

      print(f"Loss at epoch no.{epoch_idx} = {loss_training}")
      print("__________________________________")

      #optimization technique
      grad = super().backward()
      super().update_weights(epoch_idx)

    # #column vector
    # losses_np = losses_np.reshape(-1,1)
    #row vector
    losses_training_np = losses_training_np.reshape(1,-1)
    losses_validation_np = losses_validation_np.reshape(1,-1)

    return pred_training_np,losses_training_np,pred_validation_np,losses_validation_np

  def train_by_Loss(self,X_train,Y_train,X_validation,Y_validation,stopping_loss): 

    Y_train = Y_train.astype(int)

    print("start training ...")
    
    epochs_no = 0
    pred_training_np = np.empty((0))
    losses_training_np = np.empty((0))
    pred_validation_np = np.empty((0))
    losses_validation_np = np.empty((0))
	

    while True:
	  
      epochs_no += 1
      print("Epoch no. %d" % epochs_no)

      out_validation = super().forward(X_validation)

      # prediction
      pred_validation = np.argmax(out_validation,axis=1)
      pred_validation_np = np.append(pred_validation_np,pred_validation,axis=0)

      loss_validation = super().loss(out_validation, Y_validation)
      losses_validation_np = np.append(losses_validation_np,[loss_validation], axis=0)

      print(f"Loss at epoch no.{epochs_no} = {loss_validation}")
      print("__________________________________")


      out = super().__call__(X_train)
      self.no_of_classes = int(out.shape[1])
      
      # prediction
      pred_training = np.argmax(out,axis=1)
      pred_training_np = np.append(pred_training_np,pred_training,axis=0)

      loss_training = super().loss(out, Y_train)
      losses_training_np = np.append(losses_training_np,[loss_training], axis=0)

      print(f"Loss at epoch no.{epochs_no} = {loss_training}")
      print("__________________________________")

      #optimization technique
      grad = super().backward()
      super().update_weights(epochs_no-1)
	  
      if loss_validation <= stopping_loss :
        break
    self.epochs_no = epochs_no
    # #column vector
    # losses_np = losses_np.reshape(-1,1)
    #row vector
    losses_training_np = losses_training_np.reshape(1,-1)
    losses_validation_np = losses_validation_np.reshape(1,-1)
    return pred_training_np,losses_training_np,pred_validation_np,losses_validation_np,epochs_no

  def evaluate_accuracy(self,label,pred_np):

    
    #reshaping label
    label = label.astype(int)
    label = label.reshape(-1,1)
    #reshaping pred_np
    pred_np = pred_np.astype(int)
    #accuracy 
    acc_np = np.empty((0))
    pred_np = pred_np.reshape(self.epochs_no,-1,1)
    #evaluating accuracy
    for i in range(self.epochs_no):
      acc = self.evaluate.accuracy(label,pred_np[i])
      acc_np = np.append(acc_np,[acc], axis=0)
      # print(f"accuracy at epoch {i} = {acc}")
    return acc_np

  def evaluate_precision(self,label,pred_np):

    #reshaping label
    label = label.astype(int)
    label = label.reshape(-1,1)
    #reshaping pred_np
    pred_np = pred_np.astype(int)
    #precision
    precision_np = np.empty((0))
    precision_dict = {}
    # print(self.epochs_no)
    pred_np = pred_np.reshape(self.epochs_no,-1,1)
    #evaluating precision
    for class_label in  range(self.no_of_classes):
      precision_np_class = np.empty((0))
      for i in range(self.epochs_no):
        precision_val_class = self.evaluate.precision_score(class_label,label, pred_np[i])
        precision_np_class = np.append(precision_np_class,[precision_val_class],axis=0)

      key = "class_"+str(class_label)
      precision_dict[key] = precision_np_class
      precision_np = np.append(precision_np,precision_np_class)

    precision_np = precision_np.reshape(self.no_of_classes,1,self.epochs_no)
    return precision_np,precision_dict


  def evaluate_recall(self,label,pred_np):

    #reshaping label
    label = label.astype(int)
    label = label.reshape(-1,1)
    #reshaping pred_np
    pred_np = pred_np.astype(int)
    #recall
    recall_np = np.empty((0))
    recall_dict = {}
    pred_np = pred_np.reshape(self.epochs_no,-1,1)
    #evaluating recall 
    for class_label in  range(self.no_of_classes):
      recall_np_class = np.empty((0))
      for i in range(self.epochs_no):
        recall_val_class = self.evaluate.recall_score(class_label,label, pred_np[i])
        recall_np_class = np.append(recall_np_class,[recall_val_class],axis=0)

      key = "class_"+str(class_label)
      recall_dict[key] = recall_np_class
      recall_np = np.append(recall_np,recall_np_class)

    recall_np = recall_np.reshape(self.no_of_classes,1,self.epochs_no)
    return recall_np,recall_dict

  def train_cnn_by_epochs_no(self,X_train,Y_train,X_validation,Y_validation,epochs,N_imgs):

    Y_train = Y_train.astype(int)
    Y_validation = Y_validation.astype(int)
    
    self.epochs_no = epochs

    pred_training_np = np.empty((0))
    losses_training_np = np.empty((0))

    pred_validation_np = np.empty((0))
    losses_validation_np = np.empty((0))

    print("start training ...")

    for epoch_idx in range(self.epochs_no):

      batch_training_idx = np.random.choice(range(len(X_train)), size=N_imgs, replace=False)
      
      batch_validation_idx = np.random.choice(range(len(X_validation)), size=N_imgs, replace=False)

      #validation
      out_validation = super().forward(X_validation[batch_validation_idx])
      loss_validation = super().loss(out_validation, Y_validation[batch_validation_idx])

      # loss validation
      losses_validation_np = np.append(losses_validation_np,[loss_validation], axis=0)
      print(f"Loss at epoch no.{epoch_idx+1} = {loss_validation}")
      print("__________________________________")

      # prediction validation
      pred_validation= np.argmax(out_validation,axis=1)
      pred_validation_np = np.append(pred_validation_np,pred_validation,axis=0)


      out = super().__call__(X_train[batch_training_idx])
      # print("out.shape : ",out.shape)

      self.no_of_classes = int(out.shape[1])

      loss_training = super().loss(out, Y_train[batch_training_idx])
      # print(f"loss.shape : {loss.shape}")
      # loss = loss.reshape(1)
      losses_training_np = np.append(losses_training_np,[loss_training], axis=0)
      print(f"Loss at epoch no.{epoch_idx+1} = {loss_training}")
      print("__________________________________")

      # prediction
      pred_training = np.argmax(out,axis=1)
      pred_training_np = np.append(pred_training_np,pred_training,axis=0)

      super().backward()
      super().update_weights(epoch_idx)
      # print("Epoch no. %d loss =  %2f4 " % (epoch_idx + 1, loss))

    losses_training_np = losses_training_np.reshape(1,-1)
    losses_validation_np = losses_validation_np.reshape(1,-1)
	
    return pred_training_np,losses_training_np,pred_validation_np,losses_validation_np
