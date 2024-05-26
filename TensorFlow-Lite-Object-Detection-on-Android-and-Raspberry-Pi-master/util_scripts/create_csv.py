# Script to create CSV data file from Pascal VOC annotation files
# Based off code from GitHub user datitran: https://github.com/datitran/raccoon_dataset/blob/master/xml_to_csv.py

# import os
# import glob
# import pandas as pd
# import xml.etree.ElementTree as ET

# def xml_to_csv(path):
#     xml_list = []
#     for xml_file in glob.glob(path + '/*.xml'):
#         tree = ET.parse(xml_file)
#         root = tree.getroot()
#         for member in root.findall('object'):
#             value = (root.find('filename').text,
#                      int(root.find('size')[0].text),
#                      int(root.find('size')[1].text),
#                      member[0].text,
#                      int(member[4][0].text),
#                      int(member[4][1].text),
#                      int(member[4][2].text),
#                      int(member[4][3].text)
#                      )
#             xml_list.append(value)
#     column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
#     xml_df = pd.DataFrame(xml_list, columns=column_name)
#     return xml_df

# def main():
#     for folder in ['train','valid']:
#         image_path = os.path.join(os.getcwd(), ('images/' + folder))
#         xml_df = xml_to_csv(image_path)
#         xml_df.to_csv(('images/' + folder + '_labels.csv'), index=None)
#         print('Successfully converted xml to csv.')

# main()

import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET

def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            try:
                filename = root.find('filename').text
                width = int(root.find('size')[0].text)
                height = int(root.find('size')[1].text)
                class_name = member.find('name').text

                bndbox = member.find('bndbox')
                xmin = int(bndbox.find('xmin').text)
                ymin = int(bndbox.find('ymin').text)
                xmax = int(bndbox.find('xmax').text)
                ymax = int(bndbox.find('ymax').text)

                value = (filename, width, height, class_name, xmin, ymin, xmax, ymax)
                xml_list.append(value)
            except AttributeError as e:
                print(f"Missing attribute in file {xml_file}, skipping this member. Error: {e}")
            except IndexError as e:
                print(f"Index error in file {xml_file}, skipping this member. Error: {e}")

    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df

def main():
    image_path = os.path.join(os.getcwd(), 'images/train')
    xml_df = xml_to_csv(image_path)
    xml_df.to_csv('images/all/train/train_labels.csv', index=None)

    image_path = os.path.join(os.getcwd(), 'images/valid')
    xml_df = xml_to_csv(image_path)
    xml_df.to_csv('images/all/valid/test_labels.csv', index=None)

main()