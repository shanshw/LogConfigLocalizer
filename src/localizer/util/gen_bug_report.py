import os
import csv
import argparse
import sys

def gen_head():
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Diagnosis Report</title>
    </head>
    <body>
        <h1 style="font-weight: bold;">Diagnosis Report</h1>
        <p id="creationTime"></p>
        <div id="reportContainer"></div>
        <script>
            var creationTime = new Date();
            var options = {{ year: 'numeric', month: '2-digit', day: '2-digit' }};
            document.getElementById("creationTime").textContent = "Created on " + creationTime.toLocaleDateString('en-US', options);
            var reportContainer = document.getElementById("reportContainer");
    """
    return html_code

def gen_end(html_code):
    html_code += """
    </script>
    </body>
    </html>
    """
    return html_code
    
def gen_body(html_code,data):
    if len(data) == 0:
        html_code += f"""
        var reportContainer = document.getElementById("reportContainer");
        var pElement = document.createElement("p");
        pElement.textContent = "Identified as Configuration-Error-Free.";
        pElement.style.backgroundColor = "#FFE4C4";
        pElement.style.textAlign = "center";
        pElement.style.fontWeight = "bold"; 
        reportContainer.appendChild(pElement);
        """
    else:
        for i, item in enumerate(data, start=1):
            html_code += f"""
                var reportItem{i} = document.createElement("div");
                reportItem{i}.innerHTML = `
                    <strong>[No.{i}]</strong>
                    <ul>
                        <li style="background-color: #FFE4C4;">option: <strong>{item["option"]}</strong>;</li>
                        <li style="background-color: #7AC5CD;">value: <strong>{item["value"]}</strong>;</li>
                        <li style="background-color: #7CCD7C;">log: <strong>{item["log"]}</strong>;</li>
                        <li style="background-color: #87CEFF;">explanation: <strong>{item["explanation"]}</strong>;</li>
                    </ul>
                `;
                reportContainer.appendChild(reportItem{i});
            """
    return html_code                         

def wirte_html(html_code,file_name):
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(html_code)

def get_recconfig(filename):

    data = []
    with open(filename, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for row in csvreader:
            name, value, log, explanation = row
            possibility = 1
            data.append({"option":name,"value":value,"log":log, "possibility":possibility, "explanation":explanation})
    return data

def main(filename,if_anomaly):
    data = []
    print(if_anomaly)
    if if_anomaly==True:
        data = get_recconfig(filename)
    head = gen_head()
    h_b = gen_body(head,data)
    html_code = gen_end(h_b)
    print(filename)
    wirte_html(html_code,os.path.join(os.path.dirname(filename),'diagnose report.html'))
    print("finish writing html")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-rc",help="rcconfig file path")
    parser.add_argument("-anomaly",help="if the log file is of anomaly or not")
    args = parser.parse_args()
    if args.rc == None:
        print("file path should not be empty")
        sys.exit(1)
    else:
        rcconfig_path = args.rc
        if args.anomaly=="True":
            main(rcconfig_path,True)
        else:
            main(rcconfig_path,False)
