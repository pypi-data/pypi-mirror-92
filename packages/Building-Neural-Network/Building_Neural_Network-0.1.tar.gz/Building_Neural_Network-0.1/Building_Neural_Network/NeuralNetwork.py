
class NeuralNetwork():
  


    def __init__(self, loss='crossentropy', classifier='categorical', metric='accuracy', learning_rate=.04):
        ALLOWED_LOSSES = ['crossentropy']
        ALLOWED_CLASSIFIERS = ['binary', 'categorical']
        ALLOWED_METRICS = ['accuracy','percision','recall','f1 score']

        self.W = [np.NaN]
        self.b = [np.NaN]
        self.Z = [np.NaN]
        self.A = [np.NaN]

        self.layer_activations = [None]
        self.layer_units = [0]
        self.layer_initializers = [None]

        self.loss_function = loss
        self.classifier = classifier
        self.metric = metric
        self.loss_history = [np.NaN]
        self.metric_history = [np.NaN]
        self.loss = 0.
        self.learning_rate = learning_rate

    def activation_func(self, z, activation=None, return_derivative=False):

        if activation == 'sigmoid':
            s = 1/(1 + np.exp(-z))
            if return_derivative:
                return s*(1 - s)

        elif activation == 'tanh':
            s = np.tanh(z)
            if return_derivative:
                return 1 - s**2

        elif activation == 'reLU':
            s = np.maximum(z, 0)
            if return_derivative:
                return (s > 0)*s

        elif activation == 'leakyrelu':
            s = np.where(z > 0, z, z * 0.01)
            if return_derivative:
              s = np.ones_like(z)
              s[z < 0] = alpha
              return s

        elif activation == 'softmax':
            max_z = np.max(z, axis=0, keepdims=True)
            s = np.exp(z - max_z)
            norm = np.sum(s, axis=0, keepdims=True)
            s = s/norm
            if return_derivative:
                return s*(1-s)

        return s

    def forward_propagate(self): 
        num_layers = len(self.layer_units) - 1
        for l in range(1, num_layers+1):
            self.Z[l] = np.dot(self.W[l], self.A[l-1]) + self.b[l]
            self.A[l] = self.activation_func(self.Z[l], activation=self.layer_activations[l])

    def calculate_output_dZ(self, actual):

        if self.classifier=='categorical':
            if self.loss_function=='crossentropy':
                return -actual*(1 - self.A[-1])
        elif self.classifier=='binary':
            if self.loss_function=='crossentropy':
                return -actual + self.A[-1]

    def backward_propagate(self, actual):

        m = actual.shape[-1]
        num_layers = len(self.layer_units) - 1

        # Iterate from layer L-1 to layer 1
        for l in range(num_layers, 0, -1):
            if l == num_layers:
                dZ = self.calculate_output_dZ(actual)
            else:
                g = self.activation_func(self.Z[l], activation=self.layer_activations[l], return_derivative=True)
                dZ = g*np.dot(np.transpose(self.W[l+1]), dZ) 

            dW = (1/m)*np.dot(dZ, np.transpose(self.A[l-1]))
            dB = (1/m)*np.sum(dZ, axis=1, keepdims=True)

            # Update parameters
            self.W[l] = self.W[l] - self.learning_rate*dW
            self.b[l] = self.b[l] - self.learning_rate*dB



    def calculate_loss(self, actual):

        m = actual.shape[-1]
        predicted = self.A[-1]


        if self.loss_function == 'crossentropy' and self.classifier == 'binary':
            loss_vector = -actual*np.log(predicted) - (1 - actual)*np.log(1-predicted)
        elif self.loss_function == 'crossentropy' and self.classifier == 'categorical':
            loss_vector = np.sum(-actual*np.log(predicted), axis=0, keepdims=True)

        self.loss = (1/m)*np.sum(loss_vector)
        self.loss_history.append(self.loss)


    def initialize_params(self, X_input):

        self.layer_units[0] = X_input.shape[0]
        m = X_input.shape[-1]

        num_layers = len(self.layer_units) - 1
        for l in range(1, num_layers+1):
            n_l = self.layer_units[l]
            n_prev = self.layer_units[l-1]

            if self.layer_initializers[l] == 'zeros':
                self.W.append(np.zeros(shape=(n_l, n_prev), dtype=np.float32))
                self.b.append(np.zeros(shape=(n_l, 1), dtype=np.float32))
            elif self.layer_initializers[l] == 'random':
                self.W.append(np.random.rand(n_l, n_prev).astype(np.float32))
                self.b.append(np.random.rand(n_l, 1).astype(np.float32))

            elif self.layer_initializers[l] == 'xavier':
                stddev = np.sqrt(1/n_prev)
                self.W.append(stddev*np.random.randn(n_l, n_prev).astype(np.float32))
                self.b.append(stddev*np.random.randn(n_l, 1).astype(np.float32))
            else:
                return False
            self.Z.append(np.zeros(shape=(n_l, m), dtype=np.float32))
            self.A.append(np.zeros(shape=(n_l, m), dtype=np.float32))


    def add_layer(self, units, activation='tanh', initializer='xavier'):

        self.layer_units.append(units)
        self.layer_activations.append(activation)
        self.layer_initializers.append(initializer)



    def train(self, x_train, y_train, iterations=1):

        if self.classifier == 'categorical':
            if y_train.ndim == 1:
                one_hot_array = np.zeros(shape=(y_train.max()+1, y_train.size))
                one_hot_array[y_train, np.arange(y_train.size)] = 1
                y_train = one_hot_array
        if self.classifier == 'binary':
            if y_train.ndim == 1:
                y_train = np.expand_dims(y_train, axis=0)


        self.A[0] = x_train
        self.initialize_params(x_train)

        print('Training neural network.')
        for i in range(iterations):

            self.forward_propagate()
            self.calculate_loss(y_train)
            self.backward_propagate(y_train)

            print_step_size = int(iterations/100) if iterations > 100 else 1
            if i % print_step_size == 0:
                print('At iteration {}, J = {}'.format(i, self.loss))

    def test(self, x_test, y_test):

        if y_test.ndim == 1:
            y_test = np.expand_dims(y_test, axis=0)

        if self.classifier == 'categorical':
            if y_test.ndim == 1:
                one_hot_array = np.zeros(shape=(y_test.max()+1, y_test.size))
                one_hot_array[y_test, np.arange(y_test.size)] = 1
                y_test = one_hot_array
        if self.classifier == 'binary':
            if y_test.ndim == 1:
                y_test = np.expand_dims(y_test, axis=0)

        self.A[0] = x_test
        self.forward_propagate()
        return self.A[-1]


    def evaluation_metric(self, prediction, actual):

        
        prediction_onehot = np.zeros_like(prediction)
        prediction_onehot[prediction.argmax(0), np.arange(prediction.shape[1])] = 1

        predictedClass= prediction_onehot.T 
        one_dim_predicted_class=[]
        for i in range(len(predictedClass)):
            one_dim_predicted_class.append(np.argmax(predictedClass[i]))
        
        actual_list=actual.tolist()
        sum=0
        for i in range(len(actual_list)):
          if actual_list[i]==one_dim_predicted_class[i]:
              sum+=1
        print("accuracy = ", (sum/ len(actual_list))*100)
        currentDataClass=actual_list
        classes = set(currentDataClass)
        number_of_classes = prediction.shape[0]
        y_actu = pd.Series(currentDataClass)
        y_pred = pd.Series(one_dim_predicted_class)
        conf_matrix = pd.crosstab(y_actu, y_pred)
        cm = conf_matrix.values

        true_pos = np.diag(cm)
        false_pos = np.sum(cm, axis=0) - true_pos
        false_neg = np.sum(cm, axis=1) - true_pos

        precision = true_pos.sum()/ (true_pos.sum() + false_pos.sum()+0.00001)
        recall = true_pos.sum() / (true_pos.sum() + false_neg.sum())
        f1_score= 2*( (precision*recall) / (precision+recall) )
        print("precision = ",precision*100)
        print("f1_score = ",f1_score*100)
        print("recall = ",recall*100)


    def visualize(self):
      import matplotlib.pyplot as plt
      plt.plot(self.loss_history)
      plt.title('Loss Vs iterations')
      plt.xlabel('iterations')
      plt.ylabel('L')
      plt.show()

