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

import sys, os, shutil, urllib, hashlib
from wolframalpha import wap as wolf
from img2pdf import img2pdf

def main(argv):

    paths_info = []

    sys.stdout.write('Working.')
    sys.stdout.flush()

    paths_info = solve_problems(argv)   # future version will accept args
    generate_pdf(paths_info)

    print   # pretty terminal newline

def parse_config():

    options = []
    file = open('calculus_boss.config','r')

    try:
        app_id = file.readline().split('=')[1].split('\n')[0]
        options += [app_id]
    finally:
        file.close()

    return options

def solve_problems(argv):

    server = 'http://api.wolframalpha.com/v2/query.jsp'
    app_id = parse_config()[0]
    file = open(sys.argv[1],'r')
    paths_info = []
    image_paths = []
    wolf_engine = wolf.WolframAlphaEngine(app_id, server)
    problem_num = 0

    try:
        foldername = file.readline().split('\n')[0] + '_'
        paths_info += [foldername]

    except IOError:
        print 'Cannot open equation file.'
    else:
        if os.path.exists(foldername):
            shutil.rmtree(foldername, ignore_errors=True)

        os.makedirs(foldername)

        for line in file:

            input = line
            queryStr = wolf_engine.CreateQuery(input)
            image_num = 0

            if 'from' in queryStr or 'derivative' in queryStr:
                queryStr += ("&includepodid=Input"
                            +"&podstate=Input__Step-by-step%20solution")
            else:
                queryStr += ("&includepodid=IndefiniteIntegral"
                            +"&podstate=IndefiniteIntegral__Step-by-step%20solution")

            wolf.WolframAlphaQuery(queryStr, app_id)
            result = wolf_engine.PerformQuery(queryStr)
            result = wolf.WolframAlphaQueryResult(result)

            for pod in result.Pods():

                wolf_pod = wolf.Pod(pod)

                for subpod in wolf_pod.Subpods():

                    waSubpod = wolf.Subpod(subpod)
                    plaintext = waSubpod.Plaintext()[0]
                    img = waSubpod.Img()

                    src = wolf.scanbranches(img[0], 'src')[0]
                    alt = wolf.scanbranches(img[0], 'alt')[0]
                    src_hash = hashlib.md5(src).hexdigest()
                    image_path = (foldername + '/' + str(problem_num) + '.' +
                            str(image_num) + '__' + src_hash + "__" + ".gif")

                    urllib.urlretrieve(src,image_path)
                    image_paths.append(image_path)
                    image_num += 1
                    sys.stdout.write(' .')
                    sys.stdout.flush()

            problem_num += 1

    finally:
        paths_info += [image_paths]
        file.close()

    return paths_info

def generate_pdf(paths_info):

    dir = paths_info[0]
    paths = paths_info[1]
    pdf_bytes = img2pdf.convert(paths, dpi=150, x=0, y=0)
    file = open(dir + '/' + dir + ".pdf","wb")

    try:
        file.write(pdf_bytes)
    finally:
        file.close()

if __name__ == "__main__":
    main(sys.argv)

