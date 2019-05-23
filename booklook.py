import requests
import json
import sys

def query(query_string, language="en"):
    json_response = requests.get("https://www.googleapis.com/books/v1/volumes?q={}&order_by=relevance&langRestrict=en".format(query_string.replace(" ", "+")))
    results = json.loads(json_response.text)
    return results

def get_options(string):
    options_string = string.replace("-", "")
    options = [str(option) for option in options_string]
    return options

def display_error(error):
    print(error)
    error_message = """\nUSAGE:
    Synopsis:
        booklook [-ivc]
        booklook [-in PATH] [-out PATH]\n
    Available options:
        -i: Interactive search prompt
        -c: Option for single query execution
        -v: Verbose query output
        -in: Option for specifying path of input file
        -out: Option for specifying output file"""
    print(error_message)
    exit()

def check_for_paths(options):
    try:
        input_path = options[1]
    except IndexError:
        display_error("Missing input path")
        
    try:
        if options[2] == "-out":
            output_path = options[3]
        else:
            display_error("Missing output path")    
    except IndexError:
        display_error("Missing output path")
    return input_path, output_path

def check_validity(options):
    available_options = ["i", "c", "v"]
    for option in options:
        if option not in available_options:
            display_error("Invalid Option: " + option)
    return

def switch_multiple_options(options):
    if options[0] == "-in":
        try:
            if options[4] == "-v":
                verbosity_level = 1
        except IndexError:
            verbosity_level = 0

        input_path, output_path = check_for_paths(options)
        #print("[DEBUG] Read inputs from " + input_path + " and write to output file " + output_path + " with verbosity " + str(verbosity_level))
        inputs = read_inputs(input_path)
        results = execute_queries(inputs, verbosity=1)
        write_outputs(results, output_path)
        exit()
    return

def switch_options(options):
    if len(options) > 1:
        switch_multiple_options(options)
        
    first_options = get_options(options[0])
    check_validity(first_options)
    
    if "v" in first_options:
        verbosity_level = 1
    else:
        verbosity_level = 0

    if "c" in first_options:
        try:
            #print("[DEBUG] Execute query: " + options[1] + " with verbosity " + str(verbosity_level))
            results = execute_query(options[1])
            if verbosity_level == 1:
                results = parse_results(results)
            else:
                print(results)
            exit()
        except IndexError:
            display_error("Missing bookname.")

    elif "i" in first_options:
        #print("[DEBUG] Get Prompt with verbosity " + str(verbosity_level))
        get_prompt(verbosity=verbosity_level)
        exit()
    
    #If this executes no options were recognized
    display_error("Invalid options")

if __name__ == "__main__":
    error_message = """Synopsis:
    booklook [-iv]
    booklook [-ic] BOOKNAME
    booklook [-in PATH] [-out PATH] [-v]\n
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
    
    options = sys.argv[1:]
    switch_options(options)