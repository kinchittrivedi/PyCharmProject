import matplotlib.pyplot as plt
from ipywidgets import Output
from plt_overfit import overfit_example, output

plt.close("all")
#display(output)
ofit = overfit_example(False)
plt.show()