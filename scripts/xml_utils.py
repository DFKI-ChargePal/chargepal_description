import xml.etree.ElementTree as ET


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
