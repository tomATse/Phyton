#!/usr/bin/env python
import snowflake.connector
import json,os,shutil
import time
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives import serialization

from datetime import datetime
st = datetime.today().strftime('%Y%m%d%H%M%S')

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
config_path = '\\'.join([ROOT_DIR, 'config.json'])

# read json file
with open(config_path) as config_file:
    config = json.load(config_file)
    config = config['config_data']
    
with open(config['PRIVATE_KEY_FILE'], "rb") as key:
    p_key= serialization.load_pem_private_key(
        key.read(),
        password=config['PRIVATE_KEY_PASSPHRASE'].encode(),
        backend=default_backend()
    )

pkb = p_key.private_bytes(
    encoding=serialization.Encoding.DER,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption())


input_path = config['input_path']
target_path = config['target_path']
if not os.path.isdir(target_path):
    os.makedirs(target_path)
error_path = config['error_path']
if not os.path.isdir(error_path):
    os.makedirs(error_path)
pattern = config['pattern']
file_format = config['file_format']


def load_sql_data(sql_in_path):
    # Read SQL files
    files = []
    try:
        for file in os.listdir(sql_in_path):
            if (file.endswith('.sql')):
                files.append(file)
            print("Required File exist..!")
    except FileNotFoundError:
        print("Required File doesn't exist..!")
    return files


# Connects to Snowflake
conn = snowflake.connector.connect(
    user=config['user'],
    private_key=pkb,
    account=config['account']
)
cst = conn.cursor()

# start point
try:
    cst.execute("USE ROLE " + config['role'])
    cst.execute("USE WAREHOUSE " + config['warehouse'])
    cst.execute("USE DATABASE " + config['database'])
    cst.execute("USE SCHEMA " + config['schema'])

    source_table = load_sql_data(input_path)

    # st_list = []
    for file in source_table:
        try:
            fd = open(input_path + file, 'r')
            sqlFile = fd.read()
            print("====================================================================")
            print("Data Download started for File :"+file+". " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            print("====================================================================")
            res = ""
            for sub in sqlFile:
                res = res + sub.replace("\n", "")
            cst.execute(res)
            res1 = res.replace(";", "")
            file_name = file.replace(".sql", "")
            stage_name = "stage_" + file_name
            cst.execute("create or replace stage " + "" + stage_name + "")
            print(cst.fetchall())
            cst.execute(
                "copy into @" + "" + stage_name + "" + "/ from (" + "" + res1 + "" + ") file_format = " + "" + file_format + "")
            print("Data for " +file+ " is copied into Stage " +stage_name+ ". " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            output_dir=target_path + file_name + "_" + str(st)
            os.mkdir(output_dir)
            cst.execute(
                "get @" + "" + stage_name + "" + "/ file://" + "" + output_dir + "" + " pattern=" + "" + pattern + "")
            #print(cst.fetchall())
            print("Data Downloaded for " + file + " in Dir "+output_dir+". " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        except Exception as e:
            shutil.copy2(os.path.join(input_path, file), error_path)
            print(file + " Failed to Download data." + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            print(e.with_traceback)
            continue
        fd.close()
finally:
    cst.close()
conn.close()

