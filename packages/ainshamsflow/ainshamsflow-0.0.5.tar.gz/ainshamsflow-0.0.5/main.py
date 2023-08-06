"""Used to test all created objects."""

import ainshamsflow as asf
import pandas as pd


K_train = pd.read_csv('../train.csv').to_numpy()
ds_split = 40000
X_train = K_train[:ds_split, 1:].reshape((-1, 28, 28, 1)) / 255
X_valid = K_train[ds_split:, 1:].reshape((-1, 28, 28, 1)) / 255
y_train = K_train[:ds_split, :1].astype('int')
y_valid = K_train[ds_split:, :1].astype('int')

ds_train = asf.data.Dataset(X_train, y_train)
ds_valid = asf.data.Dataset(X_valid, y_valid)


# K_train = pd.read_csv('../train.csv').to_numpy()
# ds_split = 40000
# X_train = K_train[:ds_split, 1:] / 255
# X_valid = K_train[ds_split:, 1:] / 255
# y_train = K_train[:ds_split, :1].astype('int')
# y_valid = K_train[ds_split:, :1].astype('int')
#
# ds_train = asf.data.Dataset(X_train, y_train)
# ds_valid = asf.data.Dataset(X_valid, y_valid)


model = asf.models.Sequential([
	asf.layers.FastConv2D( 8, kernel_size=5),
	asf.layers.FastPool2D( 2, mode='avg'),
	asf.layers.FastConv2D(16, kernel_size=5),
	asf.layers.FastPool2D( 2, mode='avg'),
	asf.layers.Flatten(),
	asf.layers.Dense(120, activation='relu'),
	asf.layers.Dense( 84, activation='relu'),
	asf.layers.Dense( 10, activation='softmax')
], input_shape=(28, 28, 1), name='LeNet5_model')

# model = asf.models.Sequential([
# 	asf.layers.Conv2D( 8, kernel_s
# 	asf.layers.Pool2D( 2, mode='avg'),
# 	asf.layers.Conv2D(16, kernel_size=5),
# 	asf.layers.Pool2D( 2, mode='avg'),
# 	asf.layers.Flatten(),
# 	asf.layers.Dense(120, activation='relu'),
# 	asf.layers.Dense( 84, activation='relu'),
# 	asf.layers.Dense( 10, activation='softmax')
# ], input_shape=(28, 28, 1), name='LeNet5_model')

# model = asf.models.Sequential([
# 	asf.layers.Dense(300, 'relu'),
# 	asf.layers.Dense(100, 'relu'),
# 	asf.layers.Dense(10, 'softmax')
# ], input_shape=(28*28,), name='DNN_model')

model.print_summary()

model.compile(
	asf.optimizers.SGD(lr=0.01),
	'sparsecategoricalcrossentropy',
	['accuracy']
)

history = model.fit(
	ds_train,
	epochs=10,
	valid_data=ds_valid,
	batch_size=1024,
	valid_batch_size=512
)
history.show()

model.evaluate(ds_valid)
