
# Print information of docs
import os
import time


def print_list_docs(transpose_list):
    j = 1
    for s in transpose_list:
        print("Information of document number " + str(j) + ":")
        print("[")
        for t in s:
            print("     " + t + ",")
        j += 1
        print("]\n")


def get_elem_at_index(list, index):
    k = 0
    for x in list:
        if k == index:
            return x
        k += 1


def print_list(list):
    for x in list:
        print(x)


def get_zip_name(url):
    return url.rsplit('/', 1)[1]


def zip_to_xml_name(zipname):
    name_witout_zip = zipname.rsplit('.', 1)[0]
    name_with_xml = name_witout_zip + ".xml"
    return name_with_xml


def getSize(filename):
    if os.path.isfile(filename):
        st = os.stat(filename)
        return st.st_size
    else:
        return -1


def wait_download(file_path):
    current_size = getSize(file_path)
    print("File size calculated")
    time.sleep(5)
    while current_size != getSize(file_path) or getSize(file_path) == 0:
        current_size = getSize(file_path)
        print("current_size:"+str(current_size))
        time.sleep(50)
        # wait download
    print("Downloaded")


def get_text(node, nome, ns, valor_default=''):
    # procura pelo campo a partir do node
    campo = node.find(nome, ns)
    if campo is None:  # campo não existe, retorna o valor default
        return valor_default
    return campo.text  # retorna o text do campo
