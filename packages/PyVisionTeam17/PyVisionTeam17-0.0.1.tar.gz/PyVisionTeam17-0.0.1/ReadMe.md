# Deep-Learning-Framework

The Frame work allows us to build deep learning models more easily and quickly, without getting into the details of underlying algorithms. They provide a clear and concise way for defining models using a collection of pre-built and optimized components

# important 
you must download kaggle json file from you kaggle account and put it in .kaggle folder in your user folder

# The Frame Work consits of the following modules
- [Data pre-processing Module](#Data-pre-processing-Module)
- [Evaluation Module](#Evaluation-Module)
- [Utils Module](#Utils-Module)
- [Visualization Module](#Visualization-Module)
- [Optimizer Module](#Optimizer-Module)
- [Core Module](#Core-Module)
- [Model Class](#Model-Class)

# Data pre-processing Module<a name="Data-pre-processing-Module"></a>

The Module responsible for loading ,transforming and normalizing data.

# Evaluation Module<a name="Evaluation-Module"></a>

The Module responsible for calculating model accuracy, number of true positives,false positives,true negatives, false negatives,the precision score, recall score, F1 score and buliding the confusion matrix.

# Utils Module<a name="Utils-Module"></a>

The Module responsible for reading and saving models compressed or uncompressed

# Visualization Module<a name="Visualization-Module"></a>

The Module responsible for view input samples wether they are RGB or gray scale, plotting the necessary graphs live during training for accuracy and loss calculation, plotting static graphs between any given inputs and outputs and the table of the confusion matrix.

# Optimizer Module<a name="Optimizer-Module"></a>

The Module responsible for implementing diffrent optimization algorithms:
    - Adam.
    - AdaDelta.
    - AdaGrade.
    - RMSProp.
    - Momentum.
    - vanilla gradient descent.

# Core Module<a name="Core-Module"></a>

The core of the Frame work responsible for building the neural network and consists of the following submodules.
  - [Net Module](#net)
  - [Layers](#layers)
    - [Linear](#linear)
    - [CONV](#conv)
    - [LCN](#LCN)
  -[MaxPool](#MaxPool)
  -[Flatten](#Flatten)
  - [Losses](#losses)
    - [Multinomial_Logistic_Regression](#Multinomial_Logistic_Regression)
    - [MeanSquareLoss](#meansquareloss)
  - [Activations](#activations)


## Net Module<a name="net"></a>

Defines the neural network (its layers the activation function of each layer and the method for loss calulations).

## Layers<a name="layers"></a>

Layer is a callable object, where calling performs the forward pass and calculates local gradients.

> ### Linear<a name="linear"></a>
  A simple fully connected layer. 

> ### CONV<a name="conv"></a>
  It is the first layer to extract features from the input image. Here we define the kernel as the layer parameter. We perform matrix multiplication operations on the input image using the kernel.

> ### LCN<a name="LCN"></a>
  Local Contrast Normalization is a type of normalization that performs local subtraction and division normalizations, enforcing a sort of local competition between adjacent features in a feature map, and between features at the same spatial location in different feature maps.

## MaxPool<a name ="MaxPool"></a>

we perform pooling to reduce the number of parameters and computations.
There are different types of pooling operations, the most common ones are max pooling and average pooling.

## Flatten <a name ="Flatten"></a>

It is used to convert the data into 1D arrays to create a single feature vector. After flattening we forward the data to a fully connected layer for final classification.

## Losses<a name="losses"></a>

An abstract Module for implementing diffrent losses algorithms.


> ### Multinomial_Logistic_Regression<a name="Multinomial_Logistic_Regression"></a>
  A class for implementing Loss calculations and the gradient  using  Multinomial_Logistic_Regression .


> ### MeanSquareLoss<a name="meansquareloss"></a>
  A class for implementing Loss calculations and the gradient  using mean square loss.

## Activations<a name="activations"></a>

Implementation of diffrent activation functions:
- ReLU
- Leaky ReLU
- Sigmoid
- softmax

# Model Class<a name="Model-Class"></a>

The module that groups all the framework components together, perform training and evaluation

## How to use:

Below is an example for bulding and training a model with a neural network that has two layers with sigmoid activation function, adaDelta optimaization and cross entropy loss.
### code sample:

> from activations import *

> from layer import *

> from losses import *

> from linear import *

> from CNN import *

> from net import *

> from model import *

> from Datamodule import *

> from Evaluation import *

> from optimizer import *

> from Utils import *

> from Visualization import *

> train,validation,test = load_data()

> train_label,validation_label,train_array,validation_array,test_array = transform_data(train,validation,test)

> train_array,validation_array = normalize_data(train_array,validation_array)

> optim1 = Optimizer("AdaGrad", alpha = 0.2)

> optim2 = Optimizer("AdaGrad", alpha = 0.2)


> model_linear = Model(layers=[Linear(784,20,optim1),Sigmoid(),Linear(20,10,optim2),Softmax()],
              loss = Multinomial_Logistic_Regression())


>pred_training_np_AdaGrad,losses_training_np_AdaGrad,pred_validation_np_AdaGrad,losses_validation_np_AdaGrad,epochs_no_AdaGrad = model_linear.train_by_Loss(train_array,train_label,validation_array,validation_label,0.5)
losses_validation_np_AdaGrad = losses_validation_np_AdaGrad.reshape(-1,1)

> dict_losses_validation = {"loss_validation_linear" :losses_validation_np_AdaGrad }
> viz = visualization()

> viz.live_visualization(dict_losses_validation)

###accuracy
> arr_acc_AdaGrad = model_linear.evaluate_accuracy(validation_label,pred_validation_np_AdaGrad)

###visualizing accuracy
> dict_x ={"epochs" :list(range(1, epochs_no_AdaGrad + 1))}

> dict_y = {"validation accuracy":arr_acc_AdaGrad}

> viz.visualize(dict_x,dict_y)

###confusion matrix
> evaluate = Evaluation()

> arr_pred_AdaGrad_Epoch = pred_validation_np_AdaGrad.reshape(epochs_no_AdaGrad,-1,1)[0]
> confusionMatrixDict = evaluate.get_confusion_matrix_components(10,validation_label,arr_pred_AdaGrad_Epoch)

> viz = visualization()

> viz.draw_table(confusionMatrixDict)

###saving model
> utils_ = utils()

> utils_.save_model_compressed(model_linear,"model_linear")

###loading model 
> loaded_model_linear = utils_.load_model_compressed("model_linear")

