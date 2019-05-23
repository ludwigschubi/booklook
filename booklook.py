import requests
import json
import sys

def query(query_string, language="en"):
    json_response = requests.get("https://www.googleapis.com/books/v1/volumes?q={}&order_by=relevance&langRestrict=en".format(query_string.replace(" ", "+")))
    results = json.loads(json_response.text)
    return results

def get_options(string):
    options_string = string.replace("-", "")
    options = options_string.split("")
    return options

def display_error(error):
    print(error)
    error_message = """Synopsis:
    booklook [-ivc]
    booklook [-in PATH] [-out PATH]\n
    Available options:
    -i: Interactive search prompt
    -c: Option for single query execution
    -v: Verbose query output
    -in: Option for specifying path of input file
    -out: Option for specifying output file"""

def switch_options(options):
    if "-v" in multiple_options:
        verbosity_level = 1
        
    if "-i" in multiple_options:
        get_prompt()

if __name__ == "__main__":
    error_message = """Synopsis:
    booklook [-ivc]
    booklook [-in PATH] [-out PATH]\n
    Available options:
    -i: Interactive search prompt
    -c: Option for single query execution
    -v: Verbose query output
    -in: Option for specifying path of input file
    -out: Option for specifying output file"""

    try:
        options = str(sys.argv[1])
    except IndexError:
        display_error("Please specify the path to an input file or use the interactive prompt.")
        exit()
    
    if len(sys.argv) == 1:
        options = get_options(sys.argv[1])
        if "v" in options and "i" in options:
            get_prompt(verbosity=1)
        elif "i" in options:
            get_prompt()
    else:
        multiple_options = sys.argv[1:]
        switch_options(multiple_options)

    available_options = ["-i", "-c", "-in"]
    if option not in available_options:
        print("Invalid option.")
        print(error_message)
        exit()
    else:
        if option == "-i":
            get_interactive_prompt()
        elif option == "-c":
            query_string = str(sys.argv[2])
            print(query(query_string))
            exit()