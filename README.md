# emta_inputter
Estonian tax system stock inputter

Running on python and selenium (pip install selenium), using chrome browser
Add chrome to PATH or start manually in chrome install folder with 
chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenium\ChromeProfile"
where C:\selenium\ChromeProfile will be used to save a new chrome location
  - this will allow you to use an already opened brower (so you can log in) 
  -
  - Login to EMTA 
  - go to tax declaration page
  - open appropriate subsection 
  - run desired scrip

