# Installiation
To use this project, ensure you have Python 3 installed. 

Once you've set up the Python 3 environment, run the following command to install the required dependencies:

`pip3 install -r requirements.txt`

# Introduction
Localizer contains two stages, the *Anomaly Identification Stage* and the *Anomaly Inference Stage*. 

The first stage involves utilizing fault-free logs to identify informative key log messages. In the second stage, these key log messages, along with a configuration file, are used as input to localize the suspected configuration property and its value, generating a diagnosis report.

Before utilizing the localizer, please ensure the fault-free log and the may-fault log have been parsed utilize [parser](../parser/). 

## Anomaly Identification Stage
To start the first stage, please use this command:

`python3 anomaly_identifier.py -fp xxx -mp xxxx`

The `-fp` arg refers to the directory of the parsed results of fault-free logs.

The `-mp` arg refers to the directory of theh parsed results of may-fault logs.

For example, run the following command

`python3 anomaly_identifier.py -fp {path_to_the_project}/benchmark/wordcount/fault-free/parsed_output -mp {path_to_the_project}/benchmark/wordcount/may-fault-8/experimental/o-baseline-logs/application_1701142038763_0255/combined/container_1701142038763_0255_01_000001/parsed_output` 

then, you will find `may_specific.csv` and `free_specific.csv` generated in the directory specified by the `-mp` arg. 

Notably, a `diagnose report.html` file will be generated if no key log messages identified. Otherwise, the identified key log messages will store in the file `anomaly_logs.csv`.

## Anomaly Inference Stage

To start the second stage, please use the command:

`python3 failure_diagnoser.py -cp xxx -af xxxx -rej -api xxx`

The `-cp` argument denotes the path to the user-defined configuration file. Currently, the project supports configuration files in xml format only.

The `-af` argument specifies the path to the anomaly log file (i.e., the key log messages generated in the first stage, stored in anomaly_logs.csv).

The `-rej` argument determines whether to generate a fabricated configuration file or not. To disable this feature, simply include the `-rej` flag. Otherwise, the configuration file passed to the second stage (and the GPT-4 Model) will be the fabricated configuration file instead of the file specified by the `-cp` argument containing purely user-defined configuration properties.

The `-api` argument ensures interaction with the GPT-4 Model provided by OpenAI. The second stage is powered by LLM (Large Language Model); please ensure it is properly configured to activate this stage successfully.

For example, run the following command:

`python3 failure_diagnoser.py -cp {path_to_the_project}/benchmark/wordcount/may-fault-8/experimental/o-baseline-logs/application_1701142038763_0429/VSx1N.xml -af /{path_to_the_project}/benchmark/wordcount/may-fault-8/experimental/o-baseline-logs/application_1701142038763_0429/combined/container_1701142038763_0429_01_000001/parsed_output/anomaly_logs.csv -api <OpenAI_offerend_api>`

then, you will find the `RCConfig_Direct.csv` if any inferences occur in the *Direct Inference Phase* and `RCConfig_Indirect.csv` if any inferences occur in the *Indirect Inference Phase*. Besides, without `-rej` set, it will genrated a `fake_configuration.csv` file by default.

