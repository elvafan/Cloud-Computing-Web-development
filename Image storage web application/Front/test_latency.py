import datetime
import requests
import matplotlib.pyplot as plt
import random
uploadurl = "http://localhost:5000/api/upload"
readurl = "http://localhost:5000/api/key/"
configurl = "http://localhost:5000/update_config"

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

# 5050
requests_handled_x = [*range(20)]

requests.post(configurl, data={"cachesize": 0, "policy": "random"})
latency = []
timestamp = []
requests_handled = 0
for i in range(10):
    start = datetime.datetime.now()
    k = random.randint(0, 9)
    put(k)
    finish = datetime.datetime.now()
    latency.append((finish - start).total_seconds())
    timestamp.append(finish)
    print((finish - start).total_seconds())

    start = datetime.datetime.now()
    k = random.randint(0, 9)
    get(k)
    finish = datetime.datetime.now()
    latency.append((finish - start).total_seconds())
    timestamp.append(finish)
    print((finish - start).total_seconds())


plt.plot(requests_handled_x, latency, label = "No Cache")

requests.post(configurl, data={"cachesize": 0.05, "policy": "random"})
latency = []
timestamp = []

for i in range(10):
    start = datetime.datetime.now()
    k = random.randint(0, 9)
    put(k)
    finish = datetime.datetime.now()
    latency.append((finish - start).total_seconds())
    timestamp.append(finish)
    print((finish - start).total_seconds())
    start = datetime.datetime.now()
    k = random.randint(0, 9)
    get(k)
    finish = datetime.datetime.now()
    latency.append((finish - start).total_seconds())
    timestamp.append(finish)
    print((finish - start).total_seconds())
plt.plot(requests_handled_x, latency, label = "Random")

requests.post(configurl, data={"cachesize": 0.05, "policy": "LRU"})
latency = []
timestamp = []

for i in range(10):
    start = datetime.datetime.now()
    k = random.randint(0, 9)
    put(k)
    finish = datetime.datetime.now()
    latency.append((finish - start).total_seconds())
    timestamp.append(finish)

    start = datetime.datetime.now()
    k = random.randint(0, 9)
    get(k)
    finish = datetime.datetime.now()
    latency.append((finish - start).total_seconds())
    timestamp.append(finish)


plt.plot(requests_handled_x, latency, label = "LRU")
plt.legend()
plt.title('Latency for 20 requests with 50w50r')
plt.xlabel("Requests handled")
plt.ylabel("Latency")
plt.savefig("50-50latency.png")

# 80w20r

plt.clf()

def write80read20():
    latency = []
    for k in range(4):
        start = datetime.datetime.now()
        k = random.randint(0, 9)
        put(k)
        finish = datetime.datetime.now()
        latency.append((finish - start).total_seconds())
        timestamp.append(finish)

        start = datetime.datetime.now()
        k = random.randint(0, 9)
        put(k)
        finish = datetime.datetime.now()
        latency.append((finish - start).total_seconds())
        timestamp.append(finish)

        start = datetime.datetime.now()
        k = random.randint(0, 9)
        put(k)
        finish = datetime.datetime.now()
        latency.append((finish - start).total_seconds())
        timestamp.append(finish)

        start = datetime.datetime.now()
        k = random.randint(0, 9)
        put(k)
        finish = datetime.datetime.now()
        latency.append((finish - start).total_seconds())
        timestamp.append(finish)

        start = datetime.datetime.now()
        k = random.randint(0, 9)
        get(k)
        finish = datetime.datetime.now()
        latency.append((finish - start).total_seconds())
        timestamp.append(finish)
    return latency

requests.post(configurl, data={"cachesize": 0, "policy": "random"})
latency = write80read20()
plt.plot(requests_handled_x, latency, label = "No Cache")

requests.post(configurl, data={"cachesize": 0.05, "policy": "random"})
latency = write80read20()
plt.plot(requests_handled_x, latency, label = "Random")

requests.post(configurl, data={"cachesize": 0.05, "policy": "LRU"})
latency = write80read20()
plt.plot(requests_handled_x, latency, label = "LRU")
plt.legend()
plt.title('Latency for 20 requests with 80w20r')
plt.xlabel("Requests handled")
plt.ylabel("Latency")
plt.savefig("80w-20rlatency.png")

# 80r20w

timestamp = []

def read80write20():
    latency = []
    for k in range(4):
        start = datetime.datetime.now()
        k = random.randint(0, 9)
        put(k)
        finish = datetime.datetime.now()
        latency.append((finish - start).total_seconds())
        timestamp.append(finish)

        start = datetime.datetime.now()
        k = random.randint(0, 9)
        get(k)
        finish = datetime.datetime.now()
        latency.append((finish - start).total_seconds())
        timestamp.append(finish)

        start = datetime.datetime.now()
        k = random.randint(0, 9)
        get(k)
        finish = datetime.datetime.now()
        latency.append((finish - start).total_seconds())
        timestamp.append(finish)

        start = datetime.datetime.now()
        k = random.randint(0, 9)
        get(k)
        finish = datetime.datetime.now()
        latency.append((finish - start).total_seconds())
        timestamp.append(finish)

        start = datetime.datetime.now()
        k = random.randint(0, 9)
        get(k)
        finish = datetime.datetime.now()
        latency.append((finish - start).total_seconds())
        timestamp.append(finish)
    return latency
plt.clf()
requests.post(configurl, data={"cachesize": 0, "policy": "random"})
latency = read80write20()
plt.plot(requests_handled_x, latency, label = "No Cache")

requests.post(configurl, data={"cachesize": 0.05, "policy": "random"})
latency = read80write20()
plt.plot(requests_handled_x, latency, label = "Random")

requests.post(configurl, data={"cachesize": 0.05, "policy": "LRU"})
latency = read80write20()
plt.plot(requests_handled_x, latency, label = "LRU")
plt.legend()
plt.title('Latency for 20 requests with 20w80r')
plt.xlabel("Requests handled")
plt.ylabel("Latency")
plt.savefig("80r-20wlatency.png")
