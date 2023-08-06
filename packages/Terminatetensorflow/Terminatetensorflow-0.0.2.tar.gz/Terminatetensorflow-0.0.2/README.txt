1. Dense Module
This module contain the parameters initialization, layer forward propogation, layer backward propogation and also parameters update.
2. Viz Module
this module contain all vizualization technique used inside our framework, All built with matplotlib
3. Saver module
This module save the model parameters to be used for predection.
The model is built upon pickle implementation for save and restoring model
4. Metrics module
This module contains all the accuracy Metrics that are used to evaluate the model, include but not limited to absolute_metrics, F1_score
5. Preprocessing module
This module contain all data preprocessing from reading and cutting the data into the required ratios.

Mainly the input data is divided into test data and training data

6. Loss module
this module contain all the implemented loss functions include but not limited to multiclass loss
7. Actvfn module
This module contain all activation functions implemented for our model and also their derivatves.
8. Live animation
This module is for live plotting of both training loass and accuracy, Saved as a gif.