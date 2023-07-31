import sys
sys.path.append('../src')

from bt_tvh_pkg.btserve import server
host=input("Host: ")
print("Server starting . . .")
server(host)
