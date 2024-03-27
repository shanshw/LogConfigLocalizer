# Drain
For the detailed information about Drain, please refer to [README](https://github.com/logpai/logparser/blob/main/logparser/Drain/README.md)


# Installation

To use this project, ensure you have Python 3 installed. 

Once you've set up the Python 3 environment, run the following command to install the required dependencies:
`pip3 install -r requirements.txt`

# Start

To get started, run the following command:
`python3 parser.py -i xxx -l xxx -o xxx` or `./parser.py -i xx -l xx -o xxx`, as you prefer.

This command requires three arguments to be set. The `-i` argument refers to the input directory where the log file exists. The `-l` argument specifies the name of the log file, and the `-o` argument indicates the output directory where the parsed results will be stored.

For example, if the log file is located at `/home/workspace/logs/application_01.log`, then `-i` can be set to `/home/workspace/logs`, `-l` can be set to `application_01.log`, and `-o` can be set to wherever you prefer.



