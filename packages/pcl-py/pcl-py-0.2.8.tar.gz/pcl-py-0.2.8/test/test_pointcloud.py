import pcl
import numpy as np
import unittest

class TestPointCloud(unittest.TestCase):
    def test_normal_init(self):
        cloud_array = np.array([[1,2,3],[2,3,4]], dtype='f4')
        with self.assertRaises(ValueError):
            cloud = pcl.PointCloud(cloud_array)

        # add padding zeros after points
        cloud_array_pad = np.insert(cloud_array, 3, 0, axis=1)
        cloud = pcl.PointCloud(cloud_array_pad)
        assert len(cloud) == 2
        assert np.allclose(cloud.xyz, cloud_array)
        assert len(cloud.fields) == 3
        assert cloud.names == ['x', 'y', 'z']

    def test_list_init(self):
        cloud = pcl.PointCloud([(1,2,3),(2,3,4)], 'xyz')
        assert len(cloud) == 2
        assert np.allclose(cloud.xyz, [[1,2,3],[2,3,4]])
        assert cloud.names == ['x', 'y', 'z']

    def test_struct_init(self):
        cloud_array = np.array([(1,2,3),(2,3,4)],
            dtype={'names':['x','y','z'], 'formats':['f4','f4','f4'], 'itemsize':16})
        cloud = pcl.PointCloud(cloud_array)
        assert len(cloud) == 2
        assert np.allclose(cloud.xyz, [[1,2,3],[2,3,4]])
        assert cloud.names == ['x', 'y', 'z']

        cloud = pcl.PointCloud(np.array([(1,2,3,5),(2,3,4,5)], 
            dtype={'names':['x','y','z','i'], 'formats':['f4','f4','f4','i1'], 'offsets':[0,4,8,16]}))
        assert len(cloud) == 2
        assert np.allclose(cloud.xyz, [[1,2,3],[2,3,4]])
        assert cloud.names == ['x', 'y', 'z', 'i']

    def test_copy_init(self):
        cloud_array = np.array([[1,2,3],[2,3,4]], dtype='f4')
        cloud = pcl.PointCloud([(1,2,3),(2,3,4)], 'xyz')
        copy = pcl.PointCloud(cloud)
        assert np.all(copy.xyz == cloud_array)
        assert copy == cloud
        cloud.xyz[0,0] = 0
        assert np.any(cloud.xyz != cloud_array)
        assert np.all(copy.xyz == cloud_array)

    def test_point_type(self):
        cloud = pcl.PointCloud([(1,2,3,255),(2,3,4,255)], 'xyzrgb')
        assert len(cloud) == 2
        assert cloud.names == ['x', 'y', 'z', 'rgb']
        assert len(cloud.rgb) == 2

    def test_origin(self):
        cloud = pcl.PointCloud([(1,2,3),(2,3,4)])
        assert np.all(cloud.sensor_origin == np.zeros(3))
        cloud.sensor_origin = [1, 2, 3]
        assert np.all(cloud.sensor_origin == np.array([1,2,3]))

    def test_orientation(self):
        cloud = pcl.PointCloud([(1,2,3),(2,3,4)])
        assert np.all(cloud.sensor_orientation == np.array([0,0,0,1]))
        cloud.sensor_orientation = [1, 2, 3, 1]
        assert np.all(cloud.sensor_orientation == np.array([1,2,3,1]))

    def test_field_operations(self):
        cloud = pcl.PointCloud([(1,2,3),(2,3,4)])
        new_fields = np.array([(4,5),(6,7)], dtype=[('f1','f4'),('f2','f8')])
        cloud = cloud.append_fields(new_fields)
        assert cloud.names == ['x', 'y', 'z', 'f1', 'f2']
        assert len(cloud.to_ndarray()) == 2
        assert np.all(cloud.xyz == np.array([(1,2,3),(2,3,4)]))

        cloud = pcl.PointCloud([(1,2,3),(2,3,4)])
        new_fields = np.array([(4,5),(6,7)], dtype=[('f1','f4'),('f2','f8')])
        cloud = cloud.insert_fields(new_fields, [1,1])
        assert cloud.names == ['x', 'f2', 'f1', 'y', 'z']
        assert len(cloud.to_ndarray()) == 2
        with self.assertRaises(ValueError):
            _ = cloud.xyz

    def test_creators(self):
        cloud = pcl.create_xyz([[1,2,3], [4,5,6]])
        assert np.all(cloud.xyz == np.array([[1,2,3], [4,5,6]]))
        assert cloud.ptype == "XYZ"

        cloud = pcl.create_xyzi([[1,2,3,1], [4,5,6,4]])
        assert np.all(cloud.xyz == np.array([[1,2,3], [4,5,6]]))
        assert cloud.ptype == "XYZI"

        cloud = pcl.create_xyzl([[1,2,3,1], [4,5,6,4]])
        assert np.all(cloud.xyz == np.array([[1,2,3], [4,5,6]]))
        assert cloud.ptype == "XYZL"

        cloud = pcl.create_xyzrgb([[1,2,3,1,2,3], [4,5,6,4,5,6]])
        assert np.all(cloud.xyz == np.array([[1,2,3], [4,5,6]]))
        assert cloud.ptype == "XYZRGB"

        cloud = pcl.create_xyzrgba([[1,2,3,1,2,3,1], [4,5,6,4,5,6,4]])
        assert np.all(cloud.xyz == np.array([[1,2,3], [4,5,6]]))
        assert cloud.ptype == "XYZRGBA"

        cloud = pcl.create_xyzrgbl([[1,2,3,1,2,3,1], [4,5,6,4,5,6,4]])
        assert np.all(cloud.xyz == np.array([[1,2,3], [4,5,6]]))
        assert cloud.ptype == "XYZRGBL"

        cloud = pcl.create_normal([[1,2,3,3], [4,5,6,6]])
        assert np.all(cloud.normal == np.array([[1,2,3], [4,5,6]]))
        assert cloud.ptype == "NORMAL"

        cloud = pcl.create_normal([[1,2,3], [4,5,6]])
        assert np.all(cloud.normal == np.array([[1,2,3], [4,5,6]]))
        assert np.all(cloud['curvature'] == 0)
        assert cloud.ptype == "NORMAL"

    def test_infer_ptype(self):
        c1 = pcl.create_xyz(np.random.rand(10, 3))
        c2 = pcl.create_normal(np.random.rand(10, 3))
        c3 = c1.append_fields(c2)
        c3.infer_ptype()
        assert c3.ptype == 'XYZN'
