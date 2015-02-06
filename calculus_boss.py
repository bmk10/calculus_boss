#!/usr/bin/env python
#
# Calculus Boss v1.0 alpha
#
# Copyright (C) 2015 Ryan Lemieux <ryans.email.2@gmail.com>
#
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more detail.
#
# You should have received a copy of the GNU General Public
# License along with this program.  If not, see
# <http://www.gnu.org/licenses/>.

import sys, urllib, hashlib, os, shutil
from wolframalpha import wap
from img2pdf import img2pdf

server = 'http://api.wolframalpha.com/v2/query.jsp'
file = open('calculus_boss.config','r')
appid = file.readline().split('=')[1].split('\n')[0]
file = open(sys.argv[1],'r')
image_paths = []
problem_num = 0

sys.stdout.write('Working.')
sys.stdout.flush()

first_line = file.readline().split('\n')
foldername = first_line[0]

if os.path.exists(foldername):
    shutil.rmtree(foldername, ignore_errors=True)

os.makedirs(foldername)

for line in file:

    input = line
    waeo = wap.WolframAlphaEngine(appid, server)
    queryStr = waeo.CreateQuery(input)
    image_num = 0

    if 'from' in queryStr:
        queryStr += ("&includepodid=Input"
                    +"&podstate=Input__Step-by-step%20solution")
    else:
        queryStr += ("&includepodid=IndefiniteIntegral"
                    +"&podstate=IndefiniteIntegral__Step-by-step%20solution")

    wap.WolframAlphaQuery(queryStr, appid)
    result = waeo.PerformQuery(queryStr)
    result = wap.WolframAlphaQueryResult(result)

    for pod in result.Pods():

        waPod = wap.Pod(pod)

        for subpod in waPod.Subpods():

            waSubpod = wap.Subpod(subpod)
            plaintext = waSubpod.Plaintext()[0]
            img = waSubpod.Img()

            src = wap.scanbranches(img[0], 'src')[0]
            alt = wap.scanbranches(img[0], 'alt')[0]
            src_hash = hashlib.md5(src).hexdigest()
            image_path = (foldername + '/' + str(problem_num) + '.' +
                    str(image_num) + '__' + src_hash + "__" + ".gif")

            urllib.urlretrieve(src,image_path)
            image_paths.append(image_path)
            image_num += 1
            sys.stdout.write(' .')
            sys.stdout.flush()

    problem_num += 1

pdf_bytes = img2pdf.convert(image_paths, dpi=150, x=0, y=0)

file = open(foldername + '/' + foldername + ".pdf","wb")
file.write(pdf_bytes)
print
