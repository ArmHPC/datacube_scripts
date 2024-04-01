from netCDF4 import Dataset  # http://code.google.com/p/netcdf4-python/
import netCDF4 as nc
import numpy as np
from scipy.interpolate import griddata

def ncdump(nc_fid, verb=True):
    def print_ncattr(key):
        try:
            print("\t\ttype:", repr(nc_fid.variables[key].dtype))
            for ncattr in nc_fid.variables[key].ncattrs():
                print('\t\t%s:' % ncattr,\
                      repr(nc_fid.variables[key].getncattr(ncattr)))
        except KeyError:
            print("\t\tWARNING: %s does not contain variable attributes" % key)

    # NetCDF global attributes
    nc_attrs = nc_fid.ncattrs()
    if verb:
        print("NetCDF Global Attributes:")
        for nc_attr in nc_attrs:
            print ('\t%s:' % nc_attr, repr(nc_fid.getncattr(nc_attr)))
    nc_dims = [dim for dim in nc_fid.dimensions]  # list of nc dimensions
    # Dimension shape information.
    if verb:
        print ("NetCDF dimension information:")
        for dim in nc_dims:
            print ("\tName:", dim)
            print ("\t\tsize:", len(nc_fid.dimensions[dim]))
            print_ncattr(dim)
    # Variable information.
    nc_vars = [var for var in nc_fid.variables]  # list of nc variables
    if verb:
        print ("NetCDF variable information:")
        for var in nc_vars:
            if var not in nc_dims:
                print ('\tName:', var)
                print ("\t\tdimensions:", nc_fid.variables[var].dimensions)
                print ("\t\tsize:", nc_fid.variables[var].size)
                print_ncattr(var)
    return nc_attrs, nc_dims, nc_vars



def findValues(nc_file_path, param_name, point_lat, point_lon):
    # Open the NetCDF file and read the latitude, longitude, and variable data
    nc_file = -1
    try:
        nc_file = nc.Dataset(nc_file_path, 'r')
    except:
        print('Error')
        return 0
    
    lats = nc_file.variables['lat'][:]
    lons = nc_file.variables['lon'][:]
    data = nc_file.variables[param_name][:][0]
    # print(data)
    # print(lats)
    # print(lons)

    # Find the indices of the nearest lat/long values to the point of interest
    lat_index = np.abs(lats - point_lat).argmin()
    lon_index = np.abs(lons - point_lon).argmin()

    # Extract the value at the point of interest using nearest neighbor interpolation
    value_nearest = data[lat_index, lon_index]

    # # Extract the value at the point of interest using linear interpolation
    # lat_lon_array = np.meshgrid(lats, lons, indexing='ij')
    # lat_lon_points = np.array(list(zip(lat_lon_array[0].ravel(), lat_lon_array[1].ravel())))
    # values = data.ravel()
    # value_linear = griddata(lat_lon_points, values, (point_lat, point_lon), method='linear')

    # # Extract the value at the point of interest using cubic interpolation
    # value_cubic = griddata(lat_lon_points, values, (point_lat, point_lon), method='cubic')
    # Close the NetCDF file
    nc_file.close()
    return value_nearest #, value_linear, value_cubic


def findValuesV2(nc_file, param_name, point_lat, point_lon):
    # Open the NetCDF file and read the latitude, longitude, and variable data
    lats = nc_file.variables['lat'][:]
    lons = nc_file.variables['lon'][:]
    data = nc_file.variables[param_name][:][0]
    # print()
    # print(data.shape)
    # print(lats.shape)
    # print(lons.shape)

    # Find the indices of the nearest lat/long values to the point of interest
    lat_index = np.abs(lats - point_lat).argmin()
    lon_index = np.abs(lons - point_lon).argmin()
    
    # Extract the value at the point of interest using nearest neighbor interpolation
    value_nearest = data[lat_index, lon_index]#data[lat_index, lon_index]

    # # Extract the value at the point of interest using linear interpolation
    # lat_lon_array = np.meshgrid(lats, lons, indexing='ij')
    # lat_lon_points = np.array(list(zip(lat_lon_array[0].ravel(), lat_lon_array[1].ravel())))
    # values = data.ravel()
    # value_linear = griddata(lat_lon_points, values, (point_lat, point_lon), method='linear')

    # # Extract the value at the point of interest using cubic interpolation
    # value_cubic = griddata(lat_lon_points, values, (point_lat, point_lon), method='cubic')
    # Close the NetCDF file
    # nc_file.close()
    return value_nearest #, value_linear, value_cubic