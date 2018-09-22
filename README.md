# Convert gedcom to html with bootstrap, d3 and jquery using python
## Usage
```
python gedcom2html_test.py
```
or
```
python gedcom2html.py myfile.ged
```
## Examples
* [Dutch Royal Family](//picnicprojects.com/gedcom2html/dutchroyalfamily/)
## Features
- one html page for each individual in the gedcom file
- a parental fan chart for each individual
## Special Thanks
- gedcom2html uses [gedcom.py](https://github.com/nickreynke/python-gedcom) by Nick Reynke to parse the gedcom file
- [famousfamilytrees](http://famousfamilytrees.blogspot.com/?m=1) for the demo gedcom files
## To do
- fix fan chart
- fix jquery for parents
- beautify CSS / colors
- add full gedcom chart
- add descendants chart
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
   * -statcounter
- list of people in right column
- parental tree with collapsable CSS boxes using jquery
- improve age calculation
