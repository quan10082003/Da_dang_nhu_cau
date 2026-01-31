from src.domain.point import Point

from lxml import etree

def get_kilometer_network_boundary(net_path: str) -> (Point, Point, Point):
    """
    get center point, min point and max point of network, unit : meter
    
    Args:
        net_path: path to network file
    
    Returns:
        (center_point, min_point, max_point)
    """
    tree = etree.parse(net_path)
    root = tree.getroot()

    x_list = [float(x)/1000 for x in root.xpath("//network/nodes/node/@x")]
    y_list = [float(y)/1000 for y in root.xpath("//network/nodes/node/@y")]

    x_min = min(x_list)
    x_max = max(x_list)
    y_min = min(y_list)
    y_max = max(y_list)

    center_x = (x_min + x_max) / 2
    center_y = (y_min + y_max) / 2

    return Point(center_x, center_y), Point(x_min, y_min), Point(x_max, y_max)

if __name__ == "__main__":
    center_point, min_point, max_point = get_kilometer_network_boundary("data/simple scenario/network.xml")
    print(center_point)
    print(min_point)
    print(max_point)
    
    