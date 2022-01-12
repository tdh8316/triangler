import triangler

# TODO: Change this
img_path = "IMAGE_PATH.jpg"

# Create Triangler instance
triangler_instance = triangler.Triangler(
    # TODO: Customize these arguments
    # edge_method=EdgeMethod.SOBEL,
    # sample_method=SampleMethod.THRESHOLD,
    # color_method=ColorMethod.CENTROID,
    # points=1000,
    # blur=2,
    # pyramid_reduce=True,
)

print("Converting {}... ".format(img_path))

# Convert and save as an image
triangler_instance.convert_and_save(img_path)


input("Done! Press Enter to continue...")
