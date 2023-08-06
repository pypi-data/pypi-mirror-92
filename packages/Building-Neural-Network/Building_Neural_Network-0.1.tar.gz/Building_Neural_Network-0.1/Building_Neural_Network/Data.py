class Data():
      def shuffle_split_data(self,X,y,train_size=0.7):
        arr_rand = np.random.rand(X.shape[0])
        split = arr_rand < np.percentile(arr_rand, train_size*100)
        X_train =  np.array(X[split]).T
        y_train = np.array(y[split]).ravel()
        X_test = np.array( X[~split]).T
        y_test = np.array(y[~split]).ravel()
        return X_train, y_train, X_test, y_test

      def load_data(self,path,label):
        data=pd.read_csv(path)
        Y = data[[label]]
        data.drop([label], inplace=True, axis=1)
        X=data
        return self.shuffle_split_data(X,Y)