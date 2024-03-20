import sys
sys.path.insert(0, "..")
from opcua import Client
#from opcua import common
client = Client("opc.tcp://158.226.38.106:62541")
#client = Client("opc.tcp://admin@localhost:4840/freeopcua/server/") #connect using a user


try:
  client.connect()
  print("--- Connection succesfull ---\n")
  objects = client.getobjectsnode()
  children = objects.get_children()
  opc_test = children [2]
  print(f"""Parent Nodes on the server: {children}\n""")
#   test = client.getnode('ns=2;s=OpcTest_11')
#   print(f"""Nodes included in OPCTest11: {test.get_children()}\n""")
#   inttest = client.getnode('ns=2;s=OpcTest11.Int_test')
#   inttestvalue = inttest.getvalue()
#   type(inttestvalue)
#   print(f"""Int test: Value = {inttestvalue}; Type = {type(inttestvalue)}""")
#   doubletest = client.getnode('ns=2;s=OpcTest11.Double_test')
#   doubletestvalue = doubletest.getvalue()
#   print(f"""Double test: Value = {doubletestvalue}; Type = {type(doubletestvalue)}""")
#   bytetest = client.getnode('ns=2;s=OpcTest11.Double_test')
#   bytetestvalue = bytetest.getvalue()
#   print(f"""Byte test: Value = {bytetestvalue}; Type = {type(bytetestvalue)}""")
#   stringtest = client.getnode('ns=2;s=OpcTest11.Strg_test')
#   strgtestvalue = stringtest.getvalue()
#   print(f"""String test: Value = {strgtestvalue}; Type = {type(strgtestvalue)}""")
#   booltest = client.getnode('ns=2;s=OpcTest11.bool_test')
#   booltestvalue = booltest.getvalue()
#   print(f"""Bool test: Value = {booltestvalue}; Type = {type(booltestvalue)}""")
#   print(f"""\n--- Testing "MF0FeuchteH_conv" extraction ---""")
#   Feuchte1 = client.getnode('ns=2;s=OpcTest11.MF0FeuchteHconv') 
#   Feuchte1value = Feuchte1.getvalue()
#   print(f"""Feuchte test: Value = {Feuchte1value}; Type = {type(Feuchte1value)}""")
  print("\n--- Closing Connection ---")
  client.close_session()
except:
  print("An exception occurred")
  client.close_session()
