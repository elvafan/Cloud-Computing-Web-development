import datetime
import requests
import base64
import random
import matplotlib.pyplot as plt
uploadurl = "http://localhost:5000/api/upload"
readurl = "http://localhost:5000/api/key/"
configurl = "http://localhost:5002/update_manager_config"
incre_node_url = "http://localhost:5002/manual_mode_increment"
decre_node_url = "http://localhost:5002/manual_mode_decrement"

img = 'random.jpg'
#data = open(img, 'rb').read()
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}


start = datetime.datetime.now()

# TODO: Update this

#############################################
# Throughput
#############################################
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
def thoughput5050():
    throughputstart = datetime.datetime.now()
    requests_handled = 0
    throughput = []
    times = []
    while True:

        now = datetime.datetime.now()
        if (now - throughputstart).total_seconds() > 60:
            break
        i = random.randint(0, 9)
        put(i)
        requests_handled += 1
        throughput.append(requests_handled)
        times.append((now - throughputstart).total_seconds())

        now = datetime.datetime.now()
        if (now - throughputstart).total_seconds() > 60:
            break
        i = random.randint(0,9)
        get(i)
        requests_handled += 1
        throughput.append(requests_handled)
        times.append((now - throughputstart).total_seconds())


    requests.post(decre_node_url)

    while True:

        now = datetime.datetime.now()
        if (now - throughputstart).total_seconds() > 120:
            break
        i = random.randint(0, 9)
        put(i)
        requests_handled += 1
        throughput.append(requests_handled)
        times.append((now - throughputstart).total_seconds())

        now = datetime.datetime.now()
        if (now - throughputstart).total_seconds() > 120:
            break
        i = random.randint(0,9)
        get(i)
        requests_handled += 1
        throughput.append(requests_handled)
        times.append((now - throughputstart).total_seconds())


    requests.post(decre_node_url)

    while True:

        now = datetime.datetime.now()
        if (now - throughputstart).total_seconds() > 180:
            break
        i = random.randint(0, 9)
        put(i)
        requests_handled += 1
        throughput.append(requests_handled)
        times.append((now - throughputstart).total_seconds())

        now = datetime.datetime.now()
        if (now - throughputstart).total_seconds() > 180:
            break
        i = random.randint(0,9)
        get(i)
        requests_handled += 1
        throughput.append(requests_handled)
        times.append((now - throughputstart).total_seconds())


    requests.post(decre_node_url)

    while True:

        now = datetime.datetime.now()
        if (now - throughputstart).total_seconds() > 240:
            break
        i = random.randint(0, 9)
        put(i)
        requests_handled += 1
        throughput.append(requests_handled)
        times.append((now - throughputstart).total_seconds())

        now = datetime.datetime.now()
        if (now - throughputstart).total_seconds() > 240:
            break
        i = random.randint(0,9)
        get(i)
        requests_handled += 1
        throughput.append(requests_handled)
        times.append((now - throughputstart).total_seconds())


    requests.post(decre_node_url)

    while True:

        now = datetime.datetime.now()
        if (now - throughputstart).total_seconds() > 300:
            break
        i = random.randint(0, 9)
        put(i)
        requests_handled += 1
        throughput.append(requests_handled)
        times.append((now - throughputstart).total_seconds())

        now = datetime.datetime.now()
        if (now - throughputstart).total_seconds() > 300:
            break
        i = random.randint(0,9)
        get(i)
        requests_handled += 1
        throughput.append(requests_handled)
        times.append((now - throughputstart).total_seconds())
    
    return times, throughput, requests_handled

plt.clf()
requests.post(configurl, data={"cachesize": 0.05, "policy": "random"})
times, throughput , requests_handled= thoughput5050()
plt.plot(times, throughput)


plt.title('Thoughput in 5 mins with increasing from 4 to 8')
plt.xlabel("time")
plt.ylabel("Requests handled")
plt.savefig("50-50thoughput.png")
print("50 50 throughput in 5 mins finished: ", requests_handled)