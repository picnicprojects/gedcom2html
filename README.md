# Convert gedcom to html with bootstrap, d3 and jquery using python
## Usage
```
python example.py
```
Open generated/index.html in a browser
## Features
- one html page for each individual in the gedcom file
- ancenstor and descendant fan charts
- a navigator chart (with d3 force simulation)
<br>
An example of the Dutch King:

![(https://raw.githubusercontent.com/picnicprojects/gedcom2html/master/img/dutchroyalfamily.jpg)](https://raw.githubusercontent.com/picnicprojects/gedcom2html/master/img/dutchroyalfamily.jpg) 

## Special Thanks
- gedcom2html uses [gedcom.py](https://github.com/nickreynke/python-gedcom) by Nick Reynke to parse the gedcom file
- [famousfamilytrees](http://famousfamilytrees.blogspot.com/?m=1) for the demo gedcom files
## To do
- beautify CSS / colors
- command line options
   * -private
      * none
      * hide dates of people alive
      * hide all people alive
   * -output-dir
   * -language
- list of people in right column
- improve age calculation
