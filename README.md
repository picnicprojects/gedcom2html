# Convert gedcom to html with bootstrap, d3 and jquery using python
## Usage
```
python gedcom2html_test.py
```
or
```
python gedcom2html.py myfile.ged
```
## An example says it all. So have a look at:
* [Dutch Royal Family](//picnicprojects.com/gedcom2html/dutchroyalfamily/)
## Features
- one html page for each individual in the gedcom file
- ancenstor and descendant fan charts
- a navigator chart (with d3 force simulation)
## Special Thanks
- gedcom2html uses [gedcom.py](https://github.com/nickreynke/python-gedcom) by Nick Reynke to parse the gedcom file
- [famousfamilytrees](http://famousfamilytrees.blogspot.com/?m=1) for the demo gedcom files
## To do
- beautify CSS / colors
- add title
- home button
- link to index.html with main person
- command line options
   * -private
      * none
      * hide dates of people alive
      * hide all people alive
   * -output-dir
   * -language
   * -set_main_person
- list of people in right column
- improve age calculation
