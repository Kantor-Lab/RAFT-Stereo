import open3d as o3d
import numpy as np


def select_inliers(cloud, voxel_size, nb_neighbors=50, std_ratio=0.5):
    # o3d.visualization.draw_geometries([cloud])
    # print("Downsample the point cloud with a voxel of ", voxel_size)
    # voxel_down_pcd = cloud.voxel_down_sample(voxel_size)
    # o3d.visualization.draw_geometries([voxel_down_pcd])

    # print("Every 10th points are selected")
    # uni_down_pcd = cloud.uniform_down_sample(every_k_points=10)
    # o3d.visualization.draw_geometries([uni_down_pcd])

    print("Statistical oulier removal")
    cl, ind = cloud.remove_statistical_outlier(nb_neighbors=nb_neighbors,
                                                        std_ratio=std_ratio)
    display_inlier_outlier(cloud, ind)
    # uni_down_pcd = uni_down_pcd.select_by_index(ind)
    # cl, ind = uni_down_pcd.remove_radius_outlier(nb_points=50, radius=0.7)
    # display_inlier_outlier(uni_down_pcd, ind)
    return cloud.select_by_index(ind)


def display_inlier_outlier(cloud, ind):
    inlier_cloud = cloud.select_by_index(ind)
    outlier_cloud = cloud.select_by_index(ind, invert=True)

    print("Showing outliers (red) and inliers (gray): ")
    outlier_cloud.paint_uniform_color([1, 0, 0])
    inlier_cloud.paint_uniform_color([0.8, 0.8, 0.8])
    o3d.visualization.draw_geometries([inlier_cloud, outlier_cloud])

