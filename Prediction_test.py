from keras.models import load_model
import numpy as np


path_windows3 = 'E:\Dropbox\TFG\TFG_code\\trained_model.h5'
path_linux3 = r'/home/aaron/Dropbox/TFG/TFG_code/trained_model.h5'

model = load_model(path_linux3)

prediction = model.predict(np.array([[0, 1, -20]]))
print(prediction)

if prediction[0][0] >= prediction[0][1]:
    print('The section is combustion with a probability of %s' % str(prediction[0][0]))
else:
    print('The section is electric with a probability of %s' % str(prediction[0][1]))

#  in the output, first element is combustion mode, electric mode the second