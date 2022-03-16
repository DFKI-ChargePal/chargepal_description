""" urdf_autogen.py
Script to convert xacro files to urdf files. 
This is needed for example for PyBullet since PyBullet cannot load xacro files. 
"""
import os
import xml.etree.ElementTree as ET


TARGET_DIR = '_bullet_urdf_autogen'

XACRO_FILE_LIST = [
    'environment/primitive_adapter_station.urdf.xacro',
    'bringups/primitive_chargepal_with_gripper.urdf.xacro',
    'bringups/primitive_chargepal_with_fix_plug.urdf.xacro',
]

FIX_LINKS = True


def add_missing_link_inertial(file_path: str) -> None:
    xml_tree = ET.parse(file_path)
    root = xml_tree.getroot()

    for link in root.iter('link'):

        if not link.find('inertial'):
            inertial_elem = ET.Element('inertial')
            mass_elem = ET.SubElement(inertial_elem, 'mass')
            mass_elem.set('value', str(0.0))
            origin_elem = ET.SubElement(inertial_elem, 'origin')
            origin_elem.set('rpy', '0 0 0')
            origin_elem.set('xyz', '0 0 0')
            inertia_elem = ET.SubElement(inertial_elem, 'inertia')
            inertia_elem.set('ixx', str(0.0))
            inertia_elem.set('ixy', str(0.0))
            inertia_elem.set('ixz', str(0.0))
            inertia_elem.set('iyy', str(0.0))
            inertia_elem.set('iyz', str(0.0))
            inertia_elem.set('izz', str(0.0))
            link.insert(-1, inertial_elem)

    xml_tree.write(file_path)


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
                    add_missing_link_inertial(urdf_file_path)
                
                print(f'[INFO] ...succeed')
        else:
            print(f'[Warning] File >> {file_path} << is not a xacro file! Continue with next file...')
            continue


if __name__ == '__main__':
    main()
