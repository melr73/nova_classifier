This binary nova classifier uses a trained neural network to predict the classification of a transient's spectrum as a classical nova (1) or non-nova (0). It works well with large datasets of mixed transient types to detect classical novae. 

The classifier is intended for optical spectra that encompasses most or all of the 4000Å to 8000Å range. 

For further information on model training and citing this work, please reference M. Ficarra et al (in prep).

To use the classifier, download the use_nova_classifier notebook and the following dependencies: final_model.pth, architecture.py, predict.py, and scale.py. One nova spectrum and one supernova spectrum are provided to start and ensure the classifier is working smoothly. 