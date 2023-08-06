import os

base_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(base_dir, "static_files", "initial_images")
segmentation_analysis_default_image = os.path.join(images_dir, "one_nucleus.tiff")
segmentation_mask_default_image = os.path.join(images_dir, "stack.tif")
icons_dir = os.path.join(base_dir, "static_files", "icons")
colors_file = os.path.join(base_dir, "static_files", "colors.npz")
font_dir = os.path.join(base_dir, "fonts")
