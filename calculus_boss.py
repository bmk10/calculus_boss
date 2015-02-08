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

server = 'http://api.wolframalpha.com/v2/query.jsp'
config = 'calculus_boss.config'
app_id = ''

def main(argv):

    equations_file = argv[1]
    options = parse_config()

    sys.stdout.write('Working.')
    sys.stdout.flush()

    paths_info = solve_problems(equations_file, options)
    generate_pdf(paths_info)

    print   # pretty terminal newline

def parse_config():

    global app_id
    options = []
    file = open(config,'r')

    try:
        app_id = file.readline().split('=')[1].split('\n')[0]
    except IOError:
        print 'Cannot open config file.'
    else:
        options += [app_id]

        for line in file:
            options += [line.split('=')[1].split('\n')[0]]
    finally:
        file.close()

    return options

def solve_problems(equations_file, options):

    file = open(equations_file,'r')
    wolf_engine = wolf.WolframAlphaEngine(app_id, server)
    paths_info = []
    image_paths = []
    problem_num = 0

    try:
        foldername = file.readline().split('\n')[0] + '_'
    except IOError:
        print 'Cannot open equations file.'
    else:
        paths_info += [foldername]

        if os.path.exists(foldername):
            shutil.rmtree(foldername, ignore_errors=True)

        try:
            os.makedirs(foldername)
        except OSError:
            print('Cannot create destination directory')
        else:
            for line in file:

                input = line
                query_str = wolf_engine.CreateQuery(input) + '&includepodid='
                image_num = 0

                if 'from' in query_str or 'derivative' in query_str:
                    query_type = 'Input'
                else:
                    query_type = 'IndefiniteIntegral'

                query_str += query_type

                if options[1].lower() == 'true':
                    query_str += ('&podstate=' + query_type +
                                '__Step-by-step%20solution')

                if options[2].lower() == 'true':
                    query_str += '&includepodid=Plot'

                wolf.WolframAlphaQuery(query_str, app_id)
                result = wolf_engine.PerformQuery(query_str)
                result = wolf.WolframAlphaQueryResult(result)

                for pod in result.Pods():

                    wolf_pod = wolf.Pod(pod)

                    for subpod in wolf_pod.Subpods():

                        wolf_sub_pod = wolf.Subpod(subpod)
                        img = wolf_sub_pod.Img()
                        src = wolf.scanbranches(img[0], 'src')[0]
                        src_hash = hashlib.md5(src).hexdigest()

                        image_path = (foldername + '/' + str(problem_num) + '.' +
                                str(image_num) + '__' + src_hash + "__" + ".gif")
                        urllib.urlretrieve(src,image_path)
                        image_paths.append(image_path)
                        image_num += 1

                        sys.stdout.write(' .')
                        sys.stdout.flush()

                problem_num += 1

            paths_info += [image_paths]
    finally:
        file.close()

    return paths_info

def generate_pdf(paths_info):

    dir = paths_info[0]
    paths = paths_info[1]
    pdf_bytes = img2pdf.convert(paths, dpi=150, x=0, y=0)
    file = open(dir + '/' + dir + ".pdf","wb")

    try:
        file.write(pdf_bytes)
    except IOError:
        print('Cannot write PDF file.')
    finally:
        file.close()

if __name__ == "__main__":
    main(sys.argv)

