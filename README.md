# README

This program was created in the realm of a Library Application for the CODE Library. It is supposed to be used to quickly get metadata about a given book. It uses the Google Books API to find books.

## Installation:
Make sure you have python 3.6 or higher installed:
 - `python3 --version`
 
You'll have to install a couple of libraries first. The easiest would be:
 - `pip3 install -r requirements.txt`
 
Since we are accessing the google API without an API key we'll need to use tor in order to avoid Google's request rate limit. You can install tor really easily with brew:
 - `brew install tor` on macOS
 &
 - `sudo apt-get install tor` on Linux

And start it with
 - `tor` on macOS
 &
 - `sudo service tor start` on Linux
 
## Reference:

There are multiple options to look up information about a book:

### Interactive Prompt
 - `python3 booklook.py -i`
This will open a prompt that will listen to your input.
 
### Inline query
 - `python3 booklook.py -c KEYWORDS`
 
This will execute a keyword search with the given keywords.

### From table into table
 - `python3 booklook.py -in PATH_TO_INPUTS -out PATH_TO_OUTPUTS`
 
This will read keywords from the specified input file and write to a specified output file. At the moment only csv files are supported. You can test this with:
 - `python3 booklook.py -in ./test.csv -out ./test\ \(filled\).csv` 

### Verbose mode
All of the previously showcased options can be combined with -v to get the complete output from the Google Books API:
 - `python3 booklook.py -iv`
 - `python3 booklook.py -cv`
 - `python3 booklook.py -in PATH_TO_INPUTS -out PATH_TO_OUTPUTS -v`

## Troubleshooting

In case your requests are blocked by google's request rate limit you can restart tor while the program is running to get it back up again:
 - CTRL-C and then `tor` on macOS
 &
 - `sudo service tor restart` on Linux
