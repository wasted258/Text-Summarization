#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from subprocess import Popen,PIPE
from distutils import spawn
from os import path
import pdftotext
import gvision
import datetime

logger = logging.getLogger(__name__)
handler = logger.setLevel(logging.INFO)


#checking if the document is scanned
def pdf_scanned(pdf_file):

    cmd = ['pdffonts',pdf_file] #pdffonts.exe in poppler, path to .exe file in ${PATH} needed
    proc = Popen(cmd, stdout=PIPE, bufsize=0, text=True, shell=False)
    out, err = proc.communicate()
    scanned = False
    for idx, line in enumerate(out.splitlines()):
        if idx > 2: #if scanned then the output has no lines, just a error message
            scanned = True
    return scanned
def main(pdf_file):

    if pdf_scanned(pdf_file): #use "if not" to use gvision
        res = pdftotext.to_text(pdf_file)
    else:                            
        res = gvision.to_text(pdf_file)  
    return res


