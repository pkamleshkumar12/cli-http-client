import os
import pandas as pd
from mdutils.mdutils import MdUtils
import simplejson
import sys

if __name__ == "__main__":
    try:
        args = sys.argv
        file_name = args[1]
        dir_name = args[2]
        system_name = args[3]
        print("excel file name:", args[1])
        print("directory name to export:", args[2])

    except IndexError as e:
        print(e)
        print("Hint: python ConfigGen.py <excel-file-to-process> <directory-to-export-configs> <system-name")
        print("Example: python ConfigGen.py EBS_interface_master_list.xlsx generatedConfigs ebs")
        sys.exit(-1)

    t = ('excels', file_name)
    excel_path = os.path.sep.join(t)
    df = pd.read_excel(excel_path, index_col=None)

    # Removing empty spaces
    df['interface'] = df['interface'].apply(lambda x: x.strip() if isinstance(x, str) else x)
    df['version'] = df['version'].apply(lambda x: x.strip() if isinstance(x, str) else x)
    df['uc'] = df['uc'].apply(lambda x: x.strip() if isinstance(x, str) else x)
    df['RequestQuery'] = df['RequestQuery'].apply(lambda x: x.strip() if isinstance(x, str) else x)
    df['RequestBody'] = df['RequestBody'].apply(lambda x: x.strip() if isinstance(x, str) else x)
    df['PathVariable'] = df['PathVariable'].apply(lambda x: x.strip() if isinstance(x, str) else x)
    df['Header'] = df['Header'].apply(lambda x: x.strip() if isinstance(x, str) else x)
    df['Auth.json'] = df['Auth.json'].apply(lambda x: x.strip() if isinstance(x, str) else x)
    df['baseUrl'] = df['baseUrl'].apply(lambda x: x.strip() if isinstance(x, str) else x)


def create_directory(interface, version, uc):
    path = os.path.join(dir_name, system_name, interface, version, uc)
    os.makedirs(path)


def write_json_file(file_path, content):
    try:
        with open(file_path, "w") as dataFile:
            dataFile.write(simplejson.dumps(simplejson.loads(content), indent=4, sort_keys=True))
            dataFile.close()
    except FileExistsError as fee:
        print(fee)
    except Exception as ex:
        print(ex)


def create_request_query(interface, version, uc, content_string):
    file_path = os.path.join(dir_name, system_name, interface, version, uc, "RequestQuery.json")
    write_json_file(file_path, content_string)


def create_request_body(interface, version, uc, content_string):
    file_path = os.path.join(dir_name, system_name, interface, version, uc, "RequestBody.json")
    write_json_file(file_path, content_string)


def create_path_variable(interface, version, uc, content_string):
    file_path = os.path.join(dir_name, system_name, interface, version, uc, "PathVariable.json")
    write_json_file(file_path, content_string)


def create_header(interface, version, uc, content_string):
    file_path = os.path.join(dir_name, system_name, interface, version, uc, "Header.json")
    write_json_file(file_path, content_string)


def create_auth_json(interface, version, uc, content_string):
    file_path = os.path.join(dir_name, system_name, interface, version, uc, "Auth.json")
    write_json_file(file_path, content_string)


def create_path_json(interface, baseUrl):
    file_path = os.path.join(dir_name, system_name, interface, "path.json")
    content_string = '{"baseUrl": "' + baseUrl + '"}'
    write_json_file(file_path, content_string)


for index, row in df.iterrows():
    try:
        interface = row['interface']
        version = row['version']
        uc = row['uc']
        create_directory(interface, version, uc)
        create_request_query(interface, version, uc, row['RequestQuery'])
        create_request_body(interface, version, uc, row['RequestBody'])
        create_path_variable(interface, version, uc, row['PathVariable'])
        create_header(interface, version, uc, row['Header'])
        create_auth_json(interface, version, uc, row['Auth.json'])
        create_path_json(interface, row['baseUrl'])
        uc_title = " To execute " + row['interface'] + "Use Case UC01"
    except FileExistsError as e:
        print(e)
    except Exception as e:
        print(e)

read_me_template = """

## Directory structure (Sample)
    .
    ├── data
    │   ├── CC
    │   │   ├── validateBRN
    │   │   │   ├── v1                          # Version 1
    │   │   │   │   ├── UC01                    # Use case 01
    │   │   │   │   │   ├── Body.json
    │   │   │   │   │   ├── Auth.json
    │   │   │   │   │   ├── Query.json
    │   │   │   │   │   ├── Header.json
    │   │   │   │   │   └── Docs.json
    │   │   │   │   ├── UC02                    # Use case 02
    │   │   │   │   └── UC03                    # Use case 03
    │   │   │   └── v2
    │   │   │       ├── UC01
    │   │   │       └── UC02
    │   │   ├── getCustomerDetaills
    │   │   └── README.md                       # Only system related information (CC)
    │   └── SL
    │       ├── getContractDetails
    │       │   └── v1                          # Version
    │       │       └── UC01                    # Use case 01
    │       └── README.md                       # Only system related information (SL)
    ├── docs                                    # Documentation files (Shall be all in markdown)
    │   └── README.md                           # Holds information about systems
    ├── tests                                   # Test Cases
    └── requirements.txt                        # Dependencies



"""

# md file generation
t = (dir_name, system_name, 'README.md')
md_file_path = os.path.sep.join(t)

mdFile = MdUtils(file_name=md_file_path, title='Documentation')
mdFile.new_paragraph(read_me_template)
mdFile.write('  \n')
mdFile.write('  \n')
desc_str = "Description: "
cmd_str = "Command: "
sep = ""
df1 = pd.read_excel(excel_path, index_col=None, engine='openpyxl')
df1.head()

for index, row in df1.iterrows():
    mdFile.write("\n")
    uc_title = " To execute " + row['interface'] + "Use Case UC01"
    mdFile.write("**Command**: python CliHTTPClient.py {} -sn={} -in={} -vn={} -uc={} -env=SIT"
                 .format(row['method'],
                         system_name,
                         row['interface'],
                         row['version'],
                         row['uc']))
    mdFile.write("\n")
    mdFile.write("\n**Description**: {}".format(row['description']))
    mdFile.write("\n")
    mdFile.write("\n")
    mdFile.write("--------------------------------------------------------------------------------------------")

mdFile.create_md_file()
