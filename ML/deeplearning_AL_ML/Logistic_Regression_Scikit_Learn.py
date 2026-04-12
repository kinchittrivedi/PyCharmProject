import numpy as np
import matplotlib.pyplot as plt
from lab_utils_common1 import  dlc, plot_data, plt_tumor_data, sigmoid, compute_cost_logistic

X = np.array([[0.5, 1.5], [1,1], [1.5, 0.5], [3, 0.5], [2, 2], [1, 2.5]])
y = np.array([0, 0, 0, 1, 1, 1])

from sklearn.linear_model import LogisticRegression

lr_model = LogisticRegression()
lr_model.fit(X, y)

y_pred = lr_model.predict(X)

print("Prediction on training set:", y_pred)

print("Accuracy on training set:", lr_model.score(X, y))

fig,ax = plt.subplots(1,1,figsize=(4,4))
plot_data(X, y, ax)

ax.axis([0, 4, 0, 3.5])
ax.set_ylabel('$x_1$', fontsize=12)
ax.set_xlabel('$x_0$', fontsize=12)
plt.show()