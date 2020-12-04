A `TensorFlow keras` convolutional neural network (CNN) for the classification of Traffic Roadsign images from the [German Traffic Sign Recognition Benchmark](http://benchmark.ini.rub.de/?section=gtsrb&subsection=news) (GTSRB) dataset (provided in `GTSRB data`, over 50 000 images) into 43 classses. 

Models were trained using 60% of the GTSRB dataset and their generalisation abilities were assessed using the remaining 40% hold-out testing data. The number of CNN layers, the properties of the convolution and pooling layers filters and the hidden layers architecture were varied to determine the optimum machine learning parameters (details provided in `Development.md`).

The accuracy of the final model's predictions (n=3) on the training and validation datasets were 0.9891 ± 0.001 and 0.9863 ± 0.002, respectively.

