import triangler

# TODO: Change this
img_path = "IMAGE_PATH.jpg"

# Create Triangler instance
t = triangler.Triangler(
    # TODO: Customize these arguments
    # edge_method=EdgeMethod.SOBEL,
    # sample_method=SampleMethod.THRESHOLD,
    # color_method=ColorMethod.CENTROID,
    # points=1000,
    # blur=2,
    # pyramid_reduce=True,
)

print("Converting {}... ".format(img_path))
# Convert
img_tri = t.convert(img_path)

# Save
save_path = "triangler_example.{ext}".format(ext=img_path.split(".")[-1])
triangler.imsave(save_path, img_tri)

input("Done! Press Enter to continue...")
