"""
import qrcode
# example data
data = "https://bnk-app.herokuapp.com/"
filename = "QR.png"
img = qrcode.make(data)
# save img to a file
img.save(filename)
"""
import numpy as np
print(np.arange(2))
