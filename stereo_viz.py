fx= 1760.466789 
fy= 1759.986350
cx1= 720.366851
cy= 492.207186
cx2= 690.244907
baseline= 60.038 # millimeters

from imageio import imread
import os
import plotly.graph_objects as go
import numpy as np
from pathlib import Path
from imageio import imread
from PIL import Image
import sys
from core.utils.utils import InputPadder
from numpy import savez_compressed


# Plot
def plot_points(points, colors):
    NUM_POINTS_TO_DRAW = int(len(points)* 0.3)

    subset = np.random.choice(points.shape[0], size=(NUM_POINTS_TO_DRAW,), replace=False)
    points_subset = points[subset]
    colors_subset = colors[subset]

    print("""
    Controls:
    ---------
    Zoom:      Scroll Wheel
    Translate: Right-Click + Drag
    Rotate:    Left-Click + Drag
    """)

    x, y, z = points_subset.T


    fig = go.Figure(
        data=[
            go.Scatter3d(
                x=x, y=y, z=z, # flipped to make visualization nicer
                mode='markers',
                marker=dict(size=1, color=colors_subset)
            )
        ],
        layout=dict(
            scene=dict(
                xaxis=dict(visible=True),
                yaxis=dict(visible=True),
                zaxis=dict(visible=True),
            )
        )
    )
    fig.show()

stereo_images = []
disp_images = []
mask_images = []

output_directory = '../extracted_images/2022-07-02-20-21-19/outputs/'
print(output_directory)


for file in os.listdir(output_directory):
    if file.endswith("stereo.png"):
        stereo_images.append(os.path.join(output_directory, file))
    elif file.endswith(".npy"):
        disp_images.append(os.path.join(output_directory, file))
    elif file.endswith("mask.jpg"):
        mask_images.append(os.path.join(output_directory, file))
    else:
        continue

stereo_images.sort()
disp_images.sort()
mask_images.sort()

for disp_path, img_path, seg_mask in zip(disp_images, stereo_images, mask_images):
    # Load images
    print(disp_path, img_path, seg_mask)
    disp = np.load(disp_path)
    image = imread(img_path)
    seg_mask = imread(seg_mask)
    seg_mask = np.array(Image.fromarray(seg_mask).resize((disp.shape[1], disp.shape[0])))
    print(disp.shape, image.shape, seg_mask.shape)

    # inverse-project
    depth = (fx * baseline) / (-disp + (cx2 - cx1))
    H, W = depth.shape
    print('depth', depth.shape)
    xx, yy = np.meshgrid(np.arange(W), np.arange(H))
    points_grid = np.stack(((xx-cx1)/fx, (yy-cy)/fy, np.ones_like(xx)), axis=0) * depth
    print('points_grid', points_grid.shape)
    

    # Remove flying points
    #TODO: Add Statsitical outlier filter (SOR) -> open3d, cloudcompare
    # mask = np.ones((H, W), dtype=bool)
    # mask[1:][np.abs(depth[1:] - depth[:-1]) > 1] = False
    # mask[:,1:][np.abs(depth[:,1:] - depth[:,:-1]) > 1] = False
    # print(mask.shape, points_grid.shape)
    # points = points_grid.transpose(1,2,0)[mask]
    # # colors = disp[mask].astype(np.float64) / 255
    # colors = image[mask].sum(axis=1) / 3
    # # Overlay segmentation mask on color
    # print(points.shape, colors.shape)

    # Select points with valid seg_mask
    points = points_grid.transpose(1,2,0)
    colors = seg_mask
    print(points.shape, colors.shape)
    mask = colors[:,:,1] > 0
    print(mask.shape)
    points = points[mask]
    colors = colors[mask]
    print(points.shape, colors.shape)


    # Remove points with depth > 300m
    # points_select = points[:,2] < 300
    # points = points[points_select]
    # colors = colors[points_select]

    # Plot
    plot_points(points, colors)
    break

    # Save as .npz
    # savez_compressed(os.path.splitext(disp_path)+'.npz', points=points, colors=colors)

