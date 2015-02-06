# Calculus Boss
A simple python script that queries the WolframAlpha API for step-by-step solutions to calculus problems, and generates a PDF of all the solutions.

You need a WolframAlpha App ID to query the WolframAlpha API. You can create an account and request one here: https://developer.wolframalpha.com/portal/apisignup.html

Copy your App ID into the relevant place in calculus_boss.config

The script reads from a text file formatted as such:

title_of_pdf
problem 1
problem 2
...
problem n

The format of "problem n" is simply a search query just as you would type it into the search field at wolframalpha.com.

Currently this script properly supports queries of the format:

integral of n
integral of n from a to b

Any other types of queries will return unxepected results and either break the script or produce a strange PDF file.
