import iperf3
import sys

client = iperf3.Client()
client.server_hostname = '213.87.200.65'
client.port = 63400
client.json_output = True
client.reverse = sys.argv[1]
client.bandwidth = sys.argv[2]
client.duration = sys.argv[3]
