# Technical Documentation

## Problem attempted to solve:
The process of entering all our books, with additional metadata, into our database seemed too time consuming. That's why we thought we would need a small program that could produce database entries in an automated fashion, by just getting keywords as input. A program like this would also save the maintainers of the library database a lot of time in the future when adding new books.

## Code Walkthrough:

Since this program will primarily be executed from the commandline, we have to check if the options/arguments needed to run properly are given. Therefore the first lines of code have to check for the presence of and also validate these arguments:

```python
if __name__ == "__main__":
    try:
        options = str(sys.argv[1])
    except IndexError:
        display_error("Please specify the path to an input file, a keyword or use the interactive prompt.")
    options = sys.argv[1:]
    switch_options(options)
```
    
For this checking, among other things, the built-in sys module is utilised. The display_error function prints the specified message along with a hardcoded message, informing the user about the usage patterns of this program. It is used oftentimes throughout the code to display errors. The switch_options function switches the flow of the program according to the options specified. It also does some parsing/validating of the given command line arguments. Since python does not have a built-in switch statement, this function contains a lot of single conditional logic blocks. Check_for_paths, check_validity and get_options are helper functions to parse and validate the specified options.

In this part of the code the amount of verbosity is also evaluated and passed to other functions.

No matter how the user specifies his keywords, the way this program executes the keyword search is always the same - through the query function. The specified keywords get formatted into the q url parameter of the Google Books API url. Then a request is made with the requests library for python:
```python
requests.get(
            "https://www.googleapis.com/books/v1/volumes?q={}&order_by=relevance&langRestrict=en".format(query_string.replace(" ", "+")), 
            proxies={"https": "socks5h://127.0.0.1:9050"}
)
```
To avoid Google's request rate limit, the requests are made through a tor proxy. Of course there are a lot of other ways to bypass these kind of mechanisms, I choose tor because it is easy to set up and relatively reliable.
If our request is successful we can load the json response into a python dictionary by using the json library for python. If it is not successfull we wait some time, before trying again. The program will not continue before a successful request was made.

We can then pick the top result:
```python
result = results["items"][0]["volumeInfo"]
```

We then send our result to the parse_result function where, based on the specified verbosity, we extract the information we need. If the verbosity option is given, the program basically just returns the naked API response. If it is not then a handpicked amount of attributes is filtered out. Based on whether the resulting datapoint is written to a file or standard output, it is formatted accordingly. Each attribute has their own set of small requirements, and to keep extensibility high, the parsing is encapsulated for each attribute.
The parsing function for the title, for example, checks whether there's a subtitle to merge with:
```python
title = result["title"]
try: 
    title += " - " + result["subtitle"]
except KeyError:
    pass
return title
```

Since API documentation/responses can change over time, I tried to design my code as modular and extensible as possible. With requirements for our library that change over time as well, I tried to orchestrate the functionalities of this program in a way that makes it easy to add new functionality.

## That's it for now, I look forward to your feedback.
