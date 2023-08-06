from utils import *

# load mnist_conv model
data = load_model('D:/Projects/PyloXyloto/saved models/mnist_conv.pkl')
x_train_conv, y_train_conv = data[0], data[2]
label_conv = data[4]
predicted_conv = data[5]
print(predicted_conv)
print(label_conv)

# load mnist_fc model
data = load_model('D:/Projects/PyloXyloto/saved models/mnist_fc.pkl')
x_train_fc, y_train_fc = data[0], data[2]
label_fc = data[4]
predicted_fc = data[5]
print(predicted_fc)
print(label_fc)

# load xor_fc model
data = load_model('D:/Projects/PyloXyloto/saved models/xor_fc.pkl')
x, y = data[0], data[1]
pred = data[2]
print(pred)
decoded_out = label_decoder(pred)
print(decoded_out)

