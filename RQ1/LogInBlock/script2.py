import os
import re
from pathlib import Path
from pathlib import PureWindowsPath
import subprocess
import uuid
from lxml import etree

ns = {"src": "http://www.srcML.org/srcML/src"}

uniq_log_fun = set()

for line in open('output'):
    uniq_log_fun.add(line[:-1])


def generate_hex_uuid_4() -> str:
    return str(uuid.uuid4().hex)


def run(command: str, cwd=None) -> str:
    working_dir = cwd
    if cwd is not None:
        p = Path(cwd)
        if p.is_file():
            working_dir = p.parent

    return subprocess.run(command, shell=True, cwd=working_dir, stdout=subprocess.PIPE).stdout.decode('utf-8')


def generate_random_file_name_with_extension(file_extension: str) -> str:
    return "{}.{}".format(generate_hex_uuid_4(), file_extension)


def get_xml_of_file(file_path: str):
    
    xml_name = generate_random_file_name_with_extension('xml')
    try:
        run("srcml {} > {}".format(file_path, xml_name))
        xml_p = Path(xml_name)
        xml_bytes = xml_p.read_bytes()
    finally:
        xml_p.unlink()
        return xml_bytes


def is_argument_none(method_xml):
    arguments_xpath = './src:argument_list/src:argument'
    arguments = method_xml.xpath(arguments_xpath, namespaces=ns)
    if len(arguments) == 0:
        return True
    else:
        return False


def get_method_call_name(method_call_xml):
    method_call_name = ''
    call_with_operator_xpath_str = 'src:name//*'
    call_without_operator_xpath_str = 'src:name'
    method_call_name_xml = method_call_xml.xpath(
        call_with_operator_xpath_str, namespaces=ns)
    if len(method_call_name_xml) == 0:
        method_call_name_xml = method_call_xml.xpath(
            call_without_operator_xpath_str, namespaces=ns)
    for item in method_call_name_xml:
        if item.text is not None:
            method_call_name += item.text
    return method_call_name


def _is_logging_call(method_call_xml):
    if is_argument_none(method_call_xml):
        return False
    method_call_name = get_method_call_name(method_call_xml)

    if method_call_name not in uniq_log_fun:
        return False
    return True


def transform_xml_str_to_code(xml_str):
    pre_str = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><unit xmlns="http://www.srcML.org/srcML/src" revision="0.9.5" language="C" filename="code_temp.c">'
    xml_str = pre_str + \
        etree.tostring(xml_str).decode(encoding='utf-8') + '</unit>'
    fifo_name = generate_random_file_name_with_extension('xml')
    os.mkfifo(fifo_name)

    try:
        process = subprocess.Popen(
            ['srcml', fifo_name], stdout=subprocess.PIPE)
        with open(fifo_name, 'w') as f:
            f.write(xml_str)
        output = process.stdout.read().decode('utf-8')
    finally:
        os.remove(fifo_name)
    return str(output)

def get_logging_call_in_method(xml_str):
    parser = etree.XMLParser(huge_tree=True)    
    xml_object = etree.fromstring(xml_str, parser=parser)
    calls = xml_object.xpath('//src:expr_stmt/src:expr/src:call/src:name', namespaces=ns)
    result = []
    for call in calls:
        # print(call.text)
        tmp = str(call.text).rstrip()
        # print(tmp)
        if tmp in uniq_log_fun:
            result.append(call.text)
    return result


def log_calls_in_block(xml, full_path):
    if xml is not None:
        parser = etree.XMLParser(huge_tree=True)
        xml_object = etree.fromstring(xml, parser=parser)
        methods = xml_object.xpath('//src:function', namespaces=ns)
        for m in methods:
            log_call = get_logging_call_in_method(etree.tostring(m))
            print(full_path + "||" + "method" + "||" + str(len(log_call)))


for root, dirs, files in os.walk("/home/keyur/linux"):
    for filename in files:
        full_path = os.path.join(root, filename)
        if(full_path.endswith(".c")):
            try:
                xml = get_xml_of_file(full_path)
                log_calls_in_block(xml, full_path)
            except etree.XMLSyntaxError:
                print("skip")
                with open('error', 'a') as err:
                    err.write(full_path + "\n")
            

