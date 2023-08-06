import pickle
import gzip

class utils:
  
  def __init__(self):
    pass

  # using gzip
  
  def save_model_compressed(self,model,filename):
    filename_ = filename + ".gz"
    outfile = gzip.open(filename_,'wb')
    pickle.dump(model,outfile)
    outfile.close()

  def load_model_compressed(self,filename):
    filename = filename+".gz"
    infile = gzip.open(filename,'rb')
    loaded_nn = pickle.load(infile)
    infile.close()
    return loaded_nn
    
  # without gzip

  def save_model(self,model,filename):
    filename_ = filename
    outfile = open(filename_,'wb')
    pickle.dump(model,outfile)
    outfile.close()
          
  def load_model(self,filename):
      infile = open(filename,'rb')
      loaded_nn = pickle.load(infile)
      infile.close()
      return loaded_nn