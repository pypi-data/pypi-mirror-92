class utils():
  def load_model(self,filename):
    import pickle 
    loaded_model = pickle.load(open(filename, 'rb'))
    return loaded_model

  def save_model(self,nn,filename):
    import pickle 
    pickle.dump(nn, open(filename, 'wb'))
