# VRCFM
Simple OSC for your scrobbles.

# Requirements
`Python >= 3.10`<br>
`requests`<br>
`time`<br>
`python-osc`<br><br>
After installing Python, `requests` and `time` should already be satisfied.<br>
For `python-osc`, you will likely have to run `python3 -m pip install python-osc` in a terminal/command prompt.<br><br>
If you have a Python version less than 3.10, you can use `vrcfm-oldpython.py`.<br>
### What's the difference?
The primary script uses switch/case "match" statements to ultimately be a bit faster at runtime, however these were only added in Python 3.10, the latter script uses if/else statements, compatible with older Python versions.

# API Key
You can get a Last.FM API key [here](https://www.last.fm/api/account/create).

You will need to set your API key in the script, see the "CONFIG" section!

# Preview
![](/preview.png)
