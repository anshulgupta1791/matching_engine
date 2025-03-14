import sys
import platform
import xml.etree.ElementTree

def write_env_values(root, op_sys, env, browser):
    """
    Write environment values to the XML root element.

    :param root: XML root element
    :param op_sys: Operating system
    :param env: Environment
    :param browser: Browser
    :return: None
    """
    def write_value(tag, value):
        """
        Write a value to the specified tag.

        :param tag: XML tag
        :param value: Value to write
        :return: None
        """
        for child in tag:
            if child.tag == 'value':
                child.text = value
    for tag in root:
        if tag.attrib['name'] == 'env':
            write_value(tag, env)
        elif tag.attrib['name'] == 'os':
            write_value(tag, op_sys)
        elif tag.attrib['name'] == 'browser':
            write_value(tag, browser)

"""
Below script dynamically updates an XML configuration file with details about the current operating system, 
environment, and driver. It retrieves these values from both system information and command-line arguments, 
processes them using Python’s XML parsing tools, and writes them back into the specified XML file for further use.
"""
if __name__ == '__main__':
    CURRENT_OS = platform.system() + " " + platform.release()
    print(f"CURRENT OS: {CURRENT_OS}")
    CURRENT_ENV = sys.argv[1]
    print(f"CURRENT ENV: {CURRENT_ENV}")
    CURRENT_DRIVER = sys.argv[2]
    print(f"CURRENT DRIVER: {CURRENT_DRIVER}")
    ENV_FILE = sys.argv[3]
    ELEM_TREE = xml.etree.ElementTree.parse(ENV_FILE)
    ROOT = ELEM_TREE.getroot()
    write_env_values(ROOT, CURRENT_OS, CURRENT_ENV, CURRENT_DRIVER)
    ELEM_TREE.write(ENV_FILE)
