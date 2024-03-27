# Installiation
To use this project, ensure you have Python 3 installed. 

Once you've set up the Python 3 environment, run the following command to install the required dependencies:

`pip3 install -r requirements.txt`

# Start 
Localizer contains two stages, the *Anomaly Identification Stage* and the *Anomaly Inference Stage*. 

To start the first stage, please use this command:

`python3 anomaly_identifier.py -fp xxxx -mp xxxx`

The `-fp` arg refers to the directory of the parsed results of fault-free logs.

The `-mp` arg refers to the directory of theh parsed results of may-fault logs.

For example, 