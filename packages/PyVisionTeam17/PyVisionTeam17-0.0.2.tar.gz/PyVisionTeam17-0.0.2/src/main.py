from activations import *
from layer import *
from losses import *
from linear import *
from CNN import *
from net import *
from model import *
from Datamodule import *
from Evaluation import *
from optimizer import *
from Utils import *
from Visualization import *

train,validation,test = load_data()
train_label,validation_label,train_array,validation_array,test_array = transform_data(train,validation,test)
train_array,validation_array = normalize_data(train_array,validation_array)
optim1 = Optimizer("AdaGrad", alpha = 0.02)
optim2 = Optimizer("AdaGrad", alpha = 0.02)

model_linear = Model(layers=[Linear(784,20,optim1),Sigmoid(),Linear(20,10,optim2),Softmax()],
              loss = Multinomial_Logistic_Regression())


pred_training_np_AdaGrad,losses_training_np_AdaGrad,pred_validation_np_AdaGrad,losses_validation_np_AdaGrad,epochs_no_AdaGrad = model_linear.train_by_Loss(train_array,train_label,validation_array,validation_label,2)
losses_validation_np_AdaGrad = losses_validation_np_AdaGrad.reshape(-1,1)
dict_losses_validation = {"loss_validation_linear" :losses_validation_np_AdaGrad }
viz = visualization()
viz.live_visualization(dict_losses_validation)
print("training done")
#accuracy
arr_acc_AdaGrad = model_linear.evaluate_accuracy(validation_label,pred_validation_np_AdaGrad)
print("accuracy done")
#visualizing accuracy
dict_x ={"epochs" :list(range(1, epochs_no_AdaGrad + 1))}
dict_y = {"validation accuracy":arr_acc_AdaGrad}

viz.visualize(dict_x,dict_y)

#confusion matrix
evaluate = Evaluation()

arr_pred_AdaGrad_Epoch = pred_validation_np_AdaGrad.reshape(epochs_no_AdaGrad,-1,1)[0]
confusionMatrixDict = evaluate.get_confusion_matrix_components(10,validation_label,arr_pred_AdaGrad_Epoch)

viz = visualization()
viz.draw_table(confusionMatrixDict)

#saving model
utils_ = utils()
utils_.save_model_compressed(model_linear,"model_linear")

