""" mujoco_urdf_autogen.py
Script to convert xacro files to urdf files and solve filepath conflicts
MuJoCo only accept local imports of mesh files. 
"""
import os
import random
import string
import rospkg
import shutil
import xml_utils


import xml.etree.ElementTree as ET


TARGET_DIR = "_mujoco_urdf_models"

XACRO_FILE_LIST = [
    'bringups/primitive_chargepal_with_fix_plug.urdf.xacro',
]

FIX_LINKS = True



def find_assets(file_path: str, tgt_path: str) -> None:
    xml_tree = ET.parse(file_path)
    root = xml_tree.getroot()

    ros_pkg = rospkg.RosPack()

    char_set = string.ascii_lowercase

    def copy_assets(tag_name: str) -> None:
        tag = link.find(tag_name)
        if tag is not None:
            geo = tag.find('geometry')
            if geo is not None:
                mesh = geo.find('mesh')
                if mesh is not None:
                    mesh_file = mesh.get('filename')
                    mesh_file = mesh_file.replace('package://', '')
                    mesh_file_split = mesh_file.split('/')
                    mesh_file_path_tail = os.path.join(*mesh_file_split[1:])
                    mesh_file_name = mesh_file_split[-1]
                    # get a random string
                    rand_string = ''.join(random.choice(char_set) for i in range(5))
                    new_mesh_file_name = rand_string + '_' + mesh_file_name
                    ros_pkg_name = mesh_file_split[0]
                    ros_pkg_path = ros_pkg.get_path(ros_pkg_name)
                    mesh_file_path = os.path.join(ros_pkg_path, mesh_file_path_tail)
                    # copy mesh file and rename it
                    shutil.copyfile(mesh_file_path, os.path.join(tgt_path, new_mesh_file_name))
                    mesh.set('filename', new_mesh_file_name)

    for link in root.iter('link'):
        copy_assets('visual')
        copy_assets('collision')

    xml_tree.write(file_path)



def main() -> None:

    # Create target path
    cur_path = os.path.dirname(os.path.abspath(__file__))
    project_path = os.path.split(cur_path)[0]
    tgt_path = os.path.join(project_path, TARGET_DIR)

    # Create target directory if not already exist
    if not os.path.exists(tgt_path):
        os.makedirs(tgt_path)

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
                new_model_dir_name = split_path[-1].split('.')[0]
                tgt_path = os.path.join(tgt_path, new_model_dir_name)
                # Create target directory if not already exist
                if not os.path.exists(tgt_path):
                    os.makedirs(tgt_path)

                # Remove all files from this folder
                for fn in os.listdir(tgt_path):
                    fp = os.path.join(tgt_path, fn)
                    try:
                        os.remove(fp)
                    except Exception as e:
                        print(f'The object with the name {fn} will not be deleted! Exception: {e}')

                xml_file_path = os.path.join(tgt_path, "model.xml")
                print(f'[INFO] Generate file: {xml_file_path} \n...')
                try:
                    os.system('xacro ' + xacro_file_path + ' > ' + xml_file_path)
                except:
                    print(f'[Warning] Problems during the generation process! \nContinue with next file ...')

                find_assets(xml_file_path, tgt_path)

                if FIX_LINKS:
                    xml_utils.add_missing_link_inertial(xml_file_path)

        else:
            print(f'[Warning] File >> {file_path} << is not a xacro file! \nContinue with next file ...')
            continue


if __name__ == '__main__':
    main()
