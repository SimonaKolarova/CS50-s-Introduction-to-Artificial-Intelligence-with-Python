# Background

The aim of this project is to create a convolutional neural network (CNN) for the classification of road signs images. For this purpose, the [German Traffic Sign Recognition Benchmark](http://benchmark.ini.rub.de/?section=gtsrb&subsection=news) dataset was employed.

# Data structure
The dataset contains more than 50000 images classified into 43 road sign classes. 

# Data splitting and preprocessing
60% of the data was randomly selected to train the models, while 40% was used to test the CNNs' generalization abilities. All images were resized to a size of 30 x 30 px and their RGB values were normalized.

# Convolutional neural network structure optimisation
To classify the road sign data, a range of CNN models was developed in Python using the `TensorFlow keras` package's [sequential model](https://www.tensorflow.org/guide/keras/sequential_model). The models were compiled using an `adam` optimization (a stochastic gradient descent method that is based on adaptive estimation of first-order and second-order moments) and a  crossentropy loss function.The number of training epochs was kept constant at 10, while the number of CNN layers, the properties of the convolution and pooling layers filters and the hidden layers architecture were varied to determine the optimum model parameters. 
The predictive performance of the different models on the training and testing data was assessed in triplicate (n = 3) and the accuracy metric was used to select the optimum model for the multi-class classification problem.

## Initial model

The structure of the CNN model constructed initially is:
```
Model: "sequential"
_________________________________________________________________
Layer (type)                     Output Shape            Param #
=================================================================
Convolutional layer (Conv2D)     (None, 28, 28, 32)      896
(filter size: 3 x 3 px;
'relu' activation function)
_________________________________________________________________
Pooling layer (MaxPooling2D)     (None, 14, 14, 32)      0
(filter size: 2 x 2 px)
_________________________________________________________________
Flatten layer (Flatten)          (None, 6272)            0
_________________________________________________________________
Hidden layer (Dense)             (None, 128)             802944
('relu' activation function)
_________________________________________________________________
Output layer (Dense)             (None, 43)              5547
('softmax' activation function)
=================================================================
Total params: 809,387
Trainable params: 809,387
Non-trainable params: 0
```

The accuracy of the model's predictions on training and testing data was already relatively high at **0.9897 ± 0.002** and **0.9648 ± 0.0116**.

## Number of convolution/pooling layers 
The effect of employing one, two or three pairs of convolutional/pooling layers was assessed first. 

![Image of graph](https://github.com/SimonaKolarova/CS50-s-Introduction-to-Artificial-Intelligence-with-Python/blob/master/Traffic/Plots/Number%20of%20CL-PL%20pairs.png?raw=true)

As can be seen in the figure above, the predictoin performance of the CNN on both the training and testing data was notably better when 2 convolution/pooling layer (CL/PL) pairs were employed when compared to CNN of 1 or 3 CL/PL pairs. Additionally, both the models employing 1 and 3 CL/PL pairs predicted unseen data notably worse than they predicted training data suggesting that the training data was possibly overfitted. Hence, the CNN architecture employing 2 CL/PL pairs was selected to carry forward in CNN model optimisation.

## Size of convolutional layer filters

The size of the convolution layer filters was also varied (2 x 2 px, 3 x 3 px, 4 x 4 px) to assess its nfluence on the CNN model performance. 

![Image of graph](https://github.com/SimonaKolarova/CS50-s-Introduction-to-Artificial-Intelligence-with-Python/blob/master/Traffic/Plots/Size%20of%20CL%20filters.png?raw=true)

The predictive performance of the models employing 3 x 3 px convolutional layer filters was marginally better compared those employing 4 x 4 px filters and notably better than those employing 2 x 2 px filters. Therefore, this convolutional layer size (3 x 3 px) was selected to carry forward.

## Size of pooling layer filters
The size of the pooling layer filters was also varied (2 x 2 px, 3 x 3 px, 4 x 4 px) to assess its effect on the CNN model performance. 

![Image of graph](https://github.com/SimonaKolarova/CS50-s-Introduction-to-Artificial-Intelligence-with-Python/blob/master/Traffic/Plots/Size%20of%20PL%20filters.png?raw=true)


The results suggest that the use of smaller max pooling layers filters is correlated with a significant improvent in CNN predictive performance. This could be speculatively attributed to a loss of detailed image information with increase in the size of the max pooling filter. The selected size of the pooling layer filters to carry forward is 2 x 2 px.

## Number of hidden layers 
Next, the effect of employing 1, 2 or 3 hidden CNN layers (with 128 hidden neurons each) was investigted. 

![Number of hidden layers](https://github.com/SimonaKolarova/CS50-s-Introduction-to-Artificial-Intelligence-with-Python/blob/master/Traffic/Plots/Number%20of%20hidden%20layers.png?raw=true)

The results suggests that the addition of hidden CNN layers is associated with a notable decrease in predictive performance, which could be likely attributed to data overfitting. The CNN architecture with 1 hidden layer was carried forward.

## Dropout
The effect of adding a dropout layer with a dropout rate of 0.125, 0.25 or 0.5 to the CNN structure is assessed next.

![Dropout](https://github.com/SimonaKolarova/CS50-s-Introduction-to-Artificial-Intelligence-with-Python/blob/master/Traffic/Plots/Dropout.png?raw=true)

While the performance of the CNN models on the training data notably decreased with increase in the dropout rate, the performance of the CNN models on the testing data generally followed the opposite trend, with the highest prediction accuracy on the testing data achieved using a dropout rate of 0.25. Hence, a dropout layer with a rate of 0.25 was implemented in the subsequent CNN models.

## Size of hidden layer
Next, the influence of the number of hidden neurons in the hidden CNN layer on the performance of the models was assessed. 

![Number of hidden neurons](https://github.com/SimonaKolarova/CS50-s-Introduction-to-Artificial-Intelligence-with-Python/blob/master/Traffic/Plots/Number%20of%20hidden%20neurons.png?raw=true)

Generally, the models' predictive performance on the training data increased with the number of hidden neurons, while that on the testing data changed marginally over the series. The model employing 256 hidden neurons was selected to carry forward due to its balanced predictive performance on both training and testing data, suggesting that the structure is both complex enough to model the training data with a relatively high accuracy but also not so complex as to overfit the training data and lose its ability to generalise to unseen data.

## Number of filters in convolutional layers
Lastly, the effect of employing 32 or 64 filters in the first and/or second convolutiona layer was assessed.

![Number of CL filters](https://github.com/SimonaKolarova/CS50-s-Introduction-to-Artificial-Intelligence-with-Python/blob/master/Traffic/Plots/Number%20of%20CL%20filters.png?raw=true)

The difference between the four types of models trained appears to be only marginal. Nevertheless, the models employing a combination of 32 filters in the first convolutional layer and 64 filters in the latter appear to slightly outperform the other models and this architecture was, therefore, selected as optimum.


# Final CNN structure

The structure of the optimised CNN model is:

```
Model: "sequential"
_________________________________________________________________
Layer (type)                     Output Shape            Param #
=================================================================
Convolutional layer (Conv2D)     (None, 28, 28, 32)      896
(filter size: 3 x 3 px;
'relu' activation function)   
_________________________________________________________________
Pooling layer (MaxPooling2D)     (None, 14, 14, 32)      0
(filter size: 2 x 2 px)
_________________________________________________________________
Convolutional layer (Conv2D)     (None, 12, 12, 64)      18496
(filter size: 3 x 3 px;
'relu' activation function)
_________________________________________________________________
Pooling layer (MaxPooling2D)     (None, 6, 6, 64)        0
(filter size: 2 x 2 px)
_________________________________________________________________
Flatten layer (Flatten)          (None, 2304)            0
_________________________________________________________________
Hidden layer (Dense)             (None, 256)             590080
('relu' activation function)
_________________________________________________________________
Dropout layer (Dropout)          (None, 256)             0
_________________________________________________________________
Output layer (Dense)             (None, 43)              11051
('softmax' activation function)
=================================================================
Total params: 620,523
Trainable params: 620,523
Non-trainable params: 0
```

## Predictive performance

The accuracy of the predictions of the final CNN on the training and testing data were **0.9891 ± 0.001** and **0.9863 ± 0.002**, respectively. 