# -*- coding: utf-8 -*-

from google.cloud import vision
from google.cloud.vision import types
from io import open
from os import remove
from pdf2image import convert_from_path
import numpy as np

#grouping together vertices with maximal gap = maxgap
#//see example: GroupsList.txt
def cluster(data, maxgap):

    data.sort()
    groups = [[data[0]]]
    for x in data[1:]:
        if abs(x - groups[-1][-1]) <= maxgap:
            groups[-1].append(x)
        else:
            groups.append([x])
    return groups

def to_text(image_file, maximum_gap_between_lines=25, dpi_covert_from_pdf=600):

    image_path = image_file.replace('.pdf','.jpg') #prepare a path to save the coverted pdf files to jpeg
    client = vision.ImageAnnotatorClient() #create a client to gvisionAPI, ENV variable GOOGLE_APPLICATION_CREDENTIALS needed (API key)
    pages = convert_from_path(pdf_path=image_file,dpi=dpi_covert_from_pdf,fmt='JPEG') #convert pdf to jpeg, pages=list of jpegs depends on number of pages
                                                                      #//module pdf2image - wrapper around poppler executable pdftoppm, path to .exe file in ${PATH} needed
    all_pages='' #extracted text from all pages
    for page in pages:
        try:
            page.save(image_path, 'JPEG')
            #//Loads the image into memory
            with open(image_path, 'rb') as image_file1:
                content = image_file1.read()
            #//get text from image
            content_image = types.Image(content=content)
            response = client.text_detection(image=content_image,timeout=10000)
            items = [] #//words
            lines = {} #//vertices of words devided to lines (detecting rows=by vertices of words)

            #creating a dictionary: keys= lower bound of each word, the value is the count of the words with the same low bound vertex
            #//see example: LinesDictionaryExample1.json
            for text in response.text_annotations[1:]:
                top_y_axis = text.bounding_poly.vertices[0].y
                bottom_y_axis = text.bounding_poly.vertices[3].y
                if top_y_axis<bottom_y_axis:
                    if bottom_y_axis not in lines:
                        lines[bottom_y_axis] = [(top_y_axis, bottom_y_axis), 1]
                    else:
                        lines[bottom_y_axis][1] +=1
                top_y_axis=0
                bottom_y_axis=0

            #creating an array of lower bound vertices
            if len(lines.keys())>0:
                numbers = np.array([*lines.keys()])
                lines = {}
                #take the highest value of the cluster function output as the dict.key value=lowest and highest value of the output(upper and lower vertices of the row)
                #//creating rows
                for w in cluster(numbers,maximum_gap_between_lines):
                    if max(w) not in lines:
                        lines[max(w)] = [(min(w), max(w)), []]
                #now the lines dictionary is altered the keys are created from the lowest vertex of the row
                #//and the value of the key is the min and max vertex of the row
                #//creates imaginary lines = rows
                #//see example: LinesDictionaryExample2.txt
                #now rows will be populated by words from output
                #//see example: LinesDictionaryExample3.json
                for text in response.text_annotations[1:]:
                    top_x_axis = text.bounding_poly.vertices[0].x
                    top_y_axis = text.bounding_poly.vertices[0].y
                    bottom_y_axis = text.bounding_poly.vertices[3].y
                    if top_y_axis<bottom_y_axis:
                        for s_top_y_axis, s_item in lines.items():
                            if bottom_y_axis >= s_item[0][0] and bottom_y_axis <= s_item[0][1]: #checking if the row_buttom(bottom_y_axis=text.bounding_poly.vertices[3].y)
                                                                                                #//of the word is in the range:
                                                                                                #//s_item[0][0]-the lowest vertex of the row_buttom
                                                                                                #//s_item[0][1]-the highest vertex of the row_buttom
                                lines[s_top_y_axis][1].append((top_x_axis, text.description))   #//addign words to rows
                                break

                #//concatonating words to senteces - sorted acording to left vertex (top_x_axis)
                for _, item in lines.items():
                    if item[1]:
                        words = sorted(item[1], key=lambda t: t[0])
                        items.append((item[0], ' '.join([word for _, word in words]), words))
                for item in items:
                    if item[1]:
                        all_pages += (item[1]) + '\n'
            remove(image_path)
        except Exception as e:
            print(e)
    return all_pages.encode('utf-8'), response
