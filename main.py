import numpy as np
import matplotlib.pyplot as plt
import open3d as o3d
import cv2


file_gth_path = "D:\GT.png"
file_rgb_path = "D:\color.png"

gt_depth = cv2.imread(file_gth_path, cv2.COLOR_RGB2GRAY)
gt_depth = gt_depth[:,:,0]  #depth정보만 남기기
gt_depth = np.array(gt_depth, dtype=np.double)
gt_rgb = cv2.imread(file_rgb_path)
gt_rgb = np.array(gt_rgb, dtype=np.double)

row = np.size(gt_rgb, 1)
col = np.size(gt_rgb, 0)
range_y = np.array(range(row)) - (row/2) #-y/2부터 +y/2까지 range지정

range_z = np.array(range(col)) - (col/2)

xyz_file_y = np.tile(range_y, (1,col)).squeeze() #가로로 스캔하니까, -y/2부터 +y/2까지 z번 반복
xyz_file_z = np.repeat(range_z, row)   #세로축은 각 요소를 y번 반복
xyz_file_x = gt_depth.reshape([row*col]) #깊이 정보 저장장
xyz_file_x = np.multiply(xyz_file_x, -5) #스케일 맞추기

xyz_file_r = gt_rgb[:,:,2]
xyz_file_r = xyz_file_r.reshape([row*col])
xyz_file_g = gt_rgb[:,:,1]
xyz_file_g = xyz_file_g.reshape([row*col])
xyz_file_b = gt_rgb[:,:,0]
xyz_file_b = xyz_file_b.reshape([row*col])
#xyz_file_normals = np.ones([row*col,1]).squeeze()

xyz_file = np.vstack([xyz_file_x, xyz_file_y, xyz_file_z, xyz_file_r, xyz_file_g, xyz_file_b]).transpose() #3개 행렬 붙인 뒤에 trspse.
#위에서  z y x 로 저장한 이유는, x y z 해도 되지만 z y x 해야지 프린트할때 이쁘게 나옴

#np.savetxt('D:/xyzdata.ply',xyz_file, fmt="%d") #행렬저장
#point_cloud = np.loadtxt("D:/xyzdata.ply")
point_cloud = xyz_file
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(point_cloud[:,:3])
pcd.colors = o3d.utility.Vector3dVector(point_cloud[:,3:6]/255)
print(pcd)


o3d.visualization.draw_geometries([pcd])

