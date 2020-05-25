from skimage.io import imread

import triangler

import matplotlib.pyplot as plt

# Read image from disk
img = imread("IMAGE_PATH.jpg")

# Create Triangler instance
t = triangler.Triangler(sample_method=triangler.SampleMethod.POISSON_DISK)

print("Converting... ")
# Convert
img_tri = t.convert(img)
print("[Done]")

_, axes = plt.subplots(1, 2, figsize=(16, 16))
axes[0].imshow(img)
axes[1].imshow(img_tri)
plt.show()
