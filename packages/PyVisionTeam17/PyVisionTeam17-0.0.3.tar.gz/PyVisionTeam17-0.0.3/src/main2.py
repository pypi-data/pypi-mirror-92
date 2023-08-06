import numpy
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
test_array = numpy.loadtxt(open("test/test.csv", "rb"), delimiter=",", skiprows=1)
test_array = test_array.astype('float32')
test_array /= 255
utils_ = utils()
#loading model 
loaded_model_linear = utils_.load_model_compressed("model_linear")

out_test =loaded_model_linear.forward(test_array)

#prediction of validation data
pred_test = np.argmax(out_test,axis=1)
print(pred_test)
print(pred_test.shape)