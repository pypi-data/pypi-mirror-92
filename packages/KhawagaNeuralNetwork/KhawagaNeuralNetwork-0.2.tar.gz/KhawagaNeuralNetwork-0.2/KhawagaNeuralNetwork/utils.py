import pickle

def Save_Model(Model):
  Pkl_Filename = "Pickle_RL_Model.pkl"
  with open(Pkl_Filename, 'wb') as file:  
    pickle.dump(Model, file)
#Loading Model using Pickle, Pass file name
def Load_Model(filename):
  with open(filename, 'rb') as file:  
    Pickled_LR_Model = pickle.load(file)
  return Pickled_LR_Model