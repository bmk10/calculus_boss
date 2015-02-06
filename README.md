# Calculus Boss
A simple python script that queries the WolframAlpha API for step-by-step solutions to calculus problems, and generates a PDF of all the solutions.

You need a WolframAlpha App ID to query the WolframAlpha API. You can create an account and request one here: https://developer.wolframalpha.com/portal/apisignup.html

Copy your App ID into the relevant place in calculus_boss.config

## Usage

python calculus_boss.py equations_file

### Equations File

The script reads from a text file formatted as such:

>*title_of_pdf
>
>problem 1
>
>problem 2
>
>...
>
>problem n*

The format of "problem n" is simply a search query just as you would type it into the search field at wolframalpha.com.

Currently this script properly supports queries of the format:

>*integral of n
>
>integral of n from a to b*

Any other types of queries will return unxepected results and either break the script or produce a strange PDF file.

Please see example.math for some examples of well formed queries.

### Output

The script creates a new folder in the same directory as the script itself, with the same name as the first first line of the input equation file. All of the relevant images are then downloaded from wolframalpha.com and saved in that folder, then a PDF is generated and saved to the same folder.

If the destination directory already exists (e.g. the script is run twice in a row with the same equation file for input) the directory and all its contents are deleted and a new directory created.

Sometimes, WolframAlpha will time out on a query, and so no images will be downloaded for the problem. This currently happens silently, so be sure to check that all of the problems are there in the output PDF.

## Warning

This program comes with no guarantee of the correctness of the output! Please check your problems!

