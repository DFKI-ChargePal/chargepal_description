""" urdf_autogen.py
Script to convert xacro files to urdf files. 
This is needed for example for PyBullet since PyBullet cannot load xacro files. 
"""
import os
import xml_utils


# constants
TARGET_DIR = '_bullet_urdf_models'

XACRO_FILE_LIST = [
    'environment/primitive_adapter_station.urdf.xacro',
    'environment/adapter_station_square_socket.urdf.xacro',
    'environment/adapter_station_octa_socket.urdf.xacro',
    'bringups/chargepal_testbed_fix_rod.urdf.xacro',
    'bringups/primitive_chargepal_with_gripper.urdf.xacro',
    'bringups/primitive_chargepal_with_fix_plug.urdf.xacro',
    'bringups/ur10e.urdf.xacro',
    'environment/testbed_table.urdf.xacro',
    'tools/fix_rod_30.urdf.xacro',
]

FIX_LINKS = True


def main() -> None:
    
    # Create target path
    cur_path = os.path.dirname(os.path.abspath(__file__))
    project_path = os.path.split(cur_path)[0]
    tgt_path = os.path.join(project_path, TARGET_DIR)
    
    # Create target directory if not already exist
    if not os.path.exists(tgt_path):
        os.makedirs(tgt_path)

    # Generate urdf files
    for file_path in XACRO_FILE_LIST:

        # check if xacro file
        if file_path[-6:] == '.xacro':
            
            # Make sure that all path starts with urdf/
            split_path = file_path.split('/')
            if 'urdf' in split_path:
                split_path.remove('urdf')
            split_path = ['urdf'] + split_path
            xacro_file_path = os.path.join(project_path, *split_path)

            if not os.path.exists(xacro_file_path):
                print(f'[Warning] File >> {xacro_file_path} << does not exist! Continue with next file...')
            else:
                urdf_file_name = split_path[-1].split('.')[0] + '.urdf'                
                urdf_file_path = os.path.join(tgt_path, urdf_file_name)
                print(f'[INFO] Generate file: {urdf_file_name}...')
                try:
                    os.system('xacro ' + xacro_file_path + ' > ' + urdf_file_path)
                except:
                    print(f'[Warning] Problems during the generation process! Continue with next file...')
                
                if FIX_LINKS:
                    xml_utils.add_missing_link_inertial(urdf_file_path)
                
                print(f'[INFO] ...succeed')
        else:
            print(f'[Warning] File >> {file_path} << is not a xacro file! Continue with next file...')


if __name__ == '__main__':
    main()
