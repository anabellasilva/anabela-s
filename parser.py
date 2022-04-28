import os.path
import re

import requests
import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import wget

from faux import get_elem_at_index, get_zip_name, print_list, wait_download, zip_to_xml_name
from zipfile import ZipFile

URL = 'https://registers.esma.europa.eu/solr/esma_registers_firds_files/select?q=*&fq=publication_date:%5B2021-01-17T00:00:00Z+TO+2021-01-19T23:59:59Z%5D&wt=xml&indent=true&start=0&rows=100'
response = requests.get(URL)

if not os.path.exists('input1.xml'):
    with open('input1.xml', 'wb') as file:
        file.write(response.content)

wait_download('input1.xml')

root = ET.fromstring(response.content)

Checksum = []
Download_link = []
Publication_date = []
Id = []
Root = []
Published_instrument_file_id = []
File_name = []
File_type = []
Version = []
Timestamp = []

file = open("input1.xml", "r")
nDocs = len(re.findall(r"(<doc>)", file.read()))

i = 0
for child in root.iter('doc'):
    Checksum.append(child[i].text)
    Download_link.append(child[i + 1].text)
    Publication_date.append(child[i + 2].text)
    Id.append(child[i + 3].text)
    Root.append(child[i + 4].text)
    Published_instrument_file_id.append(child[i + 5].text)
    File_name.append(child[i + 6].text)
    File_type.append(child[i + 7].text)
    Version.append(child[i + 8].text)
    Timestamp.append(child[i + 9].text)

lists = [Checksum, Download_link, Publication_date, Id, Root, Published_instrument_file_id, Publication_date,
         File_name, File_type, Version, Timestamp]
numpy_array = np.array(lists)
transpose = numpy_array.T
transpose_list = transpose.tolist()

listOfZips = []
for innerlist in transpose_list:
    listOfZips.append(get_elem_at_index(innerlist, 1))
print_list(listOfZips)

if nDocs == 0:
    print("Error. There's no zip urls for transferring. Aborting.")
else:
    print("There are " + str(nDocs) + " docs.\nTransferring 1st one.")
    url = str(listOfZips[0])
    zip_name = get_zip_name(url)
    if not os.path.exists(zip_name):
        wget.download(url)
    else:
        # Create a ZipFile Object and load sample.zip in it
        with ZipFile(zip_name, 'r') as zipObj:
            zipObj.extractall("SteelEye/input")
        print("\nExtracted Successfully.\n")

        xml_name = zip_to_xml_name(zip_name)
        with open(xml_name, 'r'):
            cols = ["FinInstrmGnlAttrbts.Id", "FinInstrmGnlAttrbts.FullNm", "FinInstrmGnlAttrbts.ClssfctnTp",
                    "FinInstrmGnlAttrbts.CmmdtyDerivInd", "FinInstrmGnlAttrbts.NtnlCcy", "Issr"]
            rows = []

            xmlparse = ET.parse(xml_name)
            rooti = xmlparse.getroot()

            for i in rooti:
                id = getattr(i.find("Id"), 'text', None)
                full_name = getattr(i.find("FullNm"), 'text', None)
                classif = getattr(i.find("ClssfctnTp"), 'text', None)
                cmm = getattr(i.find("CmmdtyDerivInd"), 'text', None)
                ntnl = getattr(i.find("NtnlCcy"), 'text', None)
                issr = getattr(i.find("Issr"), 'text', None)

            rows.append({"FinInstrmGnlAttrbts.Id": id,
                        "FinInstrmGnlAttrbts.FullNm": full_name,
                         "FinInstrmGnlAttrbts.ClssfctnTp": classif,
                         "FinInstrmGnlAttrbts.CmmdtyDerivInd": cmm,
                         "FinInstrmGnlAttrbts.NtnlCcy": ntnl,
                         "Issr": issr})

            df = pd.DataFrame(rows, columns=cols)
            df.to_csv('output.csv')
            print("Successfully Converted to CSV.")
