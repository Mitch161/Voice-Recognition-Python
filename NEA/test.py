class SpeechRecognition():
    def __init__(self):
        # Hyperparameters
        self.learning_rate = 0.0001  # lower = more accuracy
        # For testing and nea reasons this is set to a lower value so that it can complete, in practice this would be 300000 steps.
        self.training_iters = 10  # training steps
        self.batch_size = 64

        self.width = 20  # mfcc features
        self.height = 80  # (max) length of utterance
        self.classes = 3  # amount of digits

    def get_data(self):
        batch = word_batch = speech_data.mfcc_batch_generator(self.batch_size)
        X, Y = next(batch)
        trainX, trainY = X, Y
        testX, testY = X, Y  # overfit for now
        return trainX, trainY, testX, testY, X, Y

    def init_neuralnetwork(self):
        # Network building
        net = tflearn.input_data([None, self.width, self.height])
        net = tflearn.lstm(net, 128, dropout=0.8)
        net = tflearn.fully_connected(net, self.classes, activation='softmax')
        net = tflearn.regression(net, optimizer='adam', learning_rate=self.learning_rate, loss='categorical_crossentropy')
        return net

    def training(self, net, trainX, trainY, testX, testY, X, Y):
        # Training
        # tflearn_logs is the folder location
        model = tflearn.DNN(net, tensorboard_verbose=0)
        for iters in range(self.training_iters):  # training_iters
            model.fit(trainX, trainY, n_epoch=10, validation_set=(testX, testY), show_metric=True,
                      batch_size=self.batch_size)  # n_epoch the amount of iterations it will do per loop
            _y = model.predict(X)
        #model.save("tflearn.lstm.model")
        print(_y)
        return model

    def save_model(self, model):
        print("Saving Model...")
        model.save("tflearn.lstm.model")

    def load_model(self):
        print("Loading Model...")
        new_model = tf.keras.models.load_model('/home/mitchell/Documents/speech_data_files/models/my_model')
        return new_model

    def prepare(self, filepath):
        img_size = 70
        img_array = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
        new_array = cv2.resize(img_array,(img_size,img_size))
        return new_array.reshape(-1, img_size,img_size, 1)

    def predict_model(self, model, prepare, filepath):
        prediction = model.predict([prepare(filepath)])
        print(prediction)

    def create_spectrogram(self):
        sample_rate, samples = wavfile.read('~/Documents/speech_data_files/yes/test/1.wav')
        frequencies, times, spectrogram = signal.spectrogram(samples, sample_rate)
        plt.pcolormesh(times, frequencies, spectrogram)
        plt.imshow(spectrogram)
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [sec]')
        plt.show()

def call_iris():
    filepath = "/home/mitchell/Documents/speech_data_files/yes/test/my_model"
    ai = SpeechRecognition()
    trainX, trainY, testX, testY, X, Y = ai.get_data()
    net = ai.init_neuralnetwork()
    save = ai.training(net, trainX, trainY, testX, testY, X, Y)
    ai.save_model(save)

    #loaded_model=ai.load_model()
    #created=ai.prepare(filepath)
    #ai.predict_model(loaded_model,created,filepath)

#test = "hey bob"
#test.index("")
#test = test[:3]
#print(test)


def doooo():
    for loop in range(5):
        if loop == 5:
            return True
        else:
            print("yeet")

    print("hahahahahah")

doooo()