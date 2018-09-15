# gedcom2html, a python script to convert gedcom files to html files using bootstrap and jquery.
## Usage
```
python gedcom2html.py myfile.ged
```
## Examples
* [Dutch Royal Family](//picnicprojects.com/dutchroyalfamily/)
## Special Thanks
- gedcom2html uses [gedcom.py](https://github.com/nickreynke/python-gedcom) by Nick Reynke to parse the gedcom file
- [famousfamilytrees](http://famousfamilytrees.blogspot.com/?m=1) for the demo gedcom files
## To do
- fan chart
- make gedcom2html a function
- pytest
- beautify CSS
- home button
- box with notes
- link to index.html with main person
- small box with gedcom statistics
- command line options
   * -private
      * none
      * hide dates of people alive
      * hide all people alive
   * -output-dir
   * -language
   * -set_main_person
- list of people in right column
- parental tree with collapsable CSS boxes using jquery
- improve age calculation
