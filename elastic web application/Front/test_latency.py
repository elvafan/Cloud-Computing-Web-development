import datetime
import requests
import matplotlib.pyplot as plt
import random
import time
uploadurl = "http://localhost:5000/api/upload"
readurl = "http://localhost:5000/api/key/"
configurl = "http://localhost:5002/update_manager_config"
incre_node_url = "http://localhost:5002/manual_mode_increment"
decre_node_url = "http://localhost:5002/manual_mode_decrement"

# TODO: Update following code

img = 'random.jpg'
#data = open(img, 'rb').read()
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

def get(i):
    i_read = readurl + str(i)
    requests.post(i_read)

def put(i):
    data = {"key": i}
    files = {
        'file': (img, open(img, 'rb'), "image/jpg"),
    }
    requests.post(uploadurl, data=data, files=files)

def run_tests():
    latency = []
    timestamp = []
    requests_handled = 0
    for node_decre in range(4):
        for i in range(10):
            print("Test: ", requests_handled)
            start = datetime.datetime.now()
            k = random.randint(0, 9)
            put(k)
            finish = datetime.datetime.now()
            latency.append((finish - start).total_seconds())
            timestamp.append(finish)
            print((finish - start))
            requests_handled += 1

            print("Test: ", requests_handled)
            start = datetime.datetime.now()
            k = random.randint(0, 9)
            get(k)
            finish = datetime.datetime.now()
            latency.append((finish - start).total_seconds())
            timestamp.append(finish)
            print((finish - start))
            requests_handled += 1
        requests.post(incre_node_url)
    return latency, timestamp, requests_handled


# 5050


requests.post(configurl, data={"cachesize": 0.05, "policy": "random"}) # 50 KB

latency, timestamp, requests_handled = run_tests()
requests_handled_x = [*range(requests_handled)]

plt.plot(requests_handled_x, latency)

plt.title('Latency for incresing from 4 to 8')
plt.xlabel("Requests handled")
plt.ylabel("Latency")
plt.savefig("50-50latency.png")
