import requests
import time
import json
import sys
import os

def query(query_string, language="en"):
    result = ""

    while(result == ""):
        json_response = requests.get(
            "https://www.googleapis.com/books/v1/volumes?q={}&order_by=relevance&langRestrict=en".format(query_string.replace(" ", "+")), 
            proxies={"https": "socks5h://127.0.0.1:9050"}
        )
        results = json.loads(json_response.text)
        try:
            result = results["items"][0]["volumeInfo"]
        except KeyError:
            print("Connection refused trying again in a bit...")
            time.sleep(10)
    
    return result

def not_found(datapoint, title):
    print("Couldn't find a " + datapoint + " for " + title)
    return

def get_title(result):
    title = result["title"]
    try: 
        title += " - " + result["subtitle"]
    except KeyError:
        pass
    return title


def get_isbn(result, title):
    try:
        isbn = result["industryIdentifiers"][0]["identifier"]
    except KeyError:
        not_found("isbn", title)
        isbn = ""
    return isbn

def get_author(result, title):
    try:
        if len(result["authors"]) > 1:
            author = ", ".join(result["authors"])
        else:
            author = result["authors"][0]
    except:
        not_found("authors", title)
        author = ""
    return author

def get_publisher(result, title):
    try:
        publisher = result["publisher"]
    except KeyError:
        not_found("publisher", title)
        publisher = ""
    return publisher

def get_cover(result, title):
    try:
        cover = result["imageLinks"]["thumbnail"]
    except KeyError:
        not_found("cover", title)
        cover = ""
    return cover

def get_topic(result, title):
    try:
        if len(result["categories"]) > 1:
            topic = " & ".join(result["categories"])
        else:
            topic = result["categories"][0]
    except KeyError:
        not_found("category", title)
        topic = ""
    return topic

def get_release(result, title):
    try:
        release_date = result["publishedDate"]
    except KeyError:
        not_found("publishing date", title)
        release_date = ""
    return release_date

def get_language(result, title):
    try:
        language = result["language"]
    except KeyError:
        not_found("language", title)
        language = ""
    return language

def parse_result(result, verbosity=0):
    if verbosity == 0:
        title = get_title(result)
        isbn = get_isbn(result, title)
        author = get_author(result, title)
        publisher = get_publisher(result, title)
        cover = get_cover(result, title)
        topic = get_topic(result, title)
        release_date = get_release(result, title)
        language = get_language(result, title)
        
        clean_result = {
            "isbn": isbn,
            "title": title,
            "author": author,
            "publisher": publisher,
            "cover": cover,
            "topic": topic,
            "release_date": release_date,
            "language": language
        }
        return clean_result

    elif verbosity == 1:
        return result

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

def validate_input_path(path):
    if path.split(".")[-1] != "csv":
        display_error("This program only supports csv files as input")

    if os.path.exists(path):
        #print("[DEBUG] Input File exists")
        print("Opening input file...")
    else:
        display_error("Input File does not exist")
        exit()

def read_inputs(path):
    validate_input_path(path)
    with open(path) as input_file:
        inputs = [" ".join(line.replace("\n", "").split(";")) for line in input_file.readlines()]    
    return inputs

def write_outputs(results, path):
    with open(path, "w+") as output_file:
        for result in results:
            result_array = [result[key] for key in result]
            csv_line = ";".join(result_array)
            output_file.write(csv_line + "\n")
    print("Finished writing to " + path)
    return


def execute_queries(queries, verbosity):
    results = []
    for query_ in queries:
        single_result = query(query_)
        single_result = parse_result(single_result, verbosity)
        results.append(single_result)
    return results

def get_prompt(verbosity):
    while(True):
        print("\nEnter a book you want to search for:")
        book_name = input()
        result = query(book_name)
        result = parse_result(result, verbosity)
        for key in result:
            print("{}: {}".format(key, result[key]))

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
        results = execute_queries(inputs, verbosity=verbosity_level)
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
            results = query(options[1])
            result = parse_result(results, verbosity_level)
            for key in result:
                print("{}: {}".format(key, result[key]))
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
    try:
        options = str(sys.argv[1])
    except IndexError:
        display_error("Please specify the path to an input file, a keyword or use the interactive prompt.")
    
    options = sys.argv[1:]
    switch_options(options)