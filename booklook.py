import requests
import json
import sys

def query(query_string, language="en"):
    json_response = requests.get("https://www.googleapis.com/books/v1/volumes?q={}&order_by=relevance&langRestrict=en".format(query_string.replace(" ", "+")))
    results = json.loads(json_response.text)
    return results

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
        option = str(sys.argv[1])
    except IndexError:
        print("Please specify the path to an input file or use the interactive prompt.")
        print(error_message)
        exit()
    
    if len(sys.argv) > 2:
        for arg in sys.argv[1:]:
            print(arg)
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