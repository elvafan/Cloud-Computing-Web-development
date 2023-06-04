import datetime
import requests
import base64
import random
import matplotlib.pyplot as plt
uploadurl = "http://localhost:5000/api/upload"
readurl = "http://localhost:5000/api/key/"
configurl = "http://localhost:5000/update_config"

img = 'random.jpg'
#data = open(img, 'rb').read()
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}


start = datetime.datetime.now()

#

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
    return times, throughput, requests_handled

plt.clf()
requests.post(configurl, data={"cachesize": 0, "policy": "random"})
times, throughput , requests_handled= thoughput5050()
plt.plot(times, throughput, label = "No Cache")
requests.post(configurl, data={"cachesize": 0.05, "policy": "random"})
times, throughput , requests_handled= thoughput5050()
plt.plot(times, throughput, label = "Random")
requests.post(configurl, data={"cachesize": 0.05, "policy": "LRU"})
times, throughput , requests_handled= thoughput5050()
plt.plot(times, throughput, label = "LRU")


plt.title('Thoughput in 1 mins with 50w50r')
plt.xlabel("time")
plt.ylabel("Requests handled")
plt.legend()
plt.savefig("50-50thoughput.png")
print("50 50 throughput in 1  mins finished: ", requests_handled)

# 20w80r
def w20r80():
    throughput = []
    times = []
    throughputstart = datetime.datetime.now()
    requests_handled = 0
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
        i = random.randint(0, 9)
        get(i)
        requests_handled += 1
        throughput.append(requests_handled)
        times.append((now - throughputstart).total_seconds())

        now = datetime.datetime.now()
        if (now - throughputstart).total_seconds() > 60:
            break
        i = random.randint(0, 9)
        get(i)
        requests_handled += 1
        throughput.append(requests_handled)
        times.append((now - throughputstart).total_seconds())

        now = datetime.datetime.now()
        if (now - throughputstart).total_seconds() > 60:
            break
        i = random.randint(0, 9)
        get(i)
        requests_handled += 1
        throughput.append(requests_handled)
        times.append((now - throughputstart).total_seconds())

        now = datetime.datetime.now()
        if (now - throughputstart).total_seconds() > 60:
            break
        i = random.randint(0, 9)
        get(i)
        requests_handled += 1
        throughput.append(requests_handled)
        times.append((now - throughputstart).total_seconds())
        return times, throughput, requests_handled

plt.clf()
requests.post(configurl, data={"cachesize": 0, "policy": "random"})
times, throughput , requests_handled= w20r80()
plt.plot(times, throughput, label = "No Cache")
requests.post(configurl, data={"cachesize": 0.05, "policy": "random"})
times, throughput , requests_handled= w20r80()
plt.plot(times, throughput, label = "Random")
requests.post(configurl, data={"cachesize": 0.05, "policy": "LRU"})
times, throughput , requests_handled= w20r80()
plt.plot(times, throughput, label = "LRU")
plt.title('Thoughput in 1 mins with 20w80r')
plt.xlabel("time")
plt.ylabel("Requests handled")
plt.legend()
plt.savefig("20w-80rthoughput.png")

print("20w 80r throughput in 1 mins finished: ", requests_handled)

# 20r80w
def r20w80():
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
        i = random.randint(0, 9)
        put(i)
        requests_handled += 1
        throughput.append(requests_handled)
        times.append((now - throughputstart).total_seconds())

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
        i = random.randint(0, 9)
        put(i)
        requests_handled += 1
        throughput.append(requests_handled)
        times.append((now - throughputstart).total_seconds())

        now = datetime.datetime.now()
        if (now - throughputstart).total_seconds() > 60:
            break
        i = random.randint(0, 9)
        get(i)
        requests_handled += 1
        throughput.append(requests_handled)
        times.append((now - throughputstart).total_seconds())
        return times, throughput, requests_handled

plt.clf()
requests.post(configurl, data={"cachesize": 0, "policy": "random"})
times, throughput , requests_handled= r20w80()
plt.plot(times, throughput, label = "No Cache")
requests.post(configurl, data={"cachesize": 0.05, "policy": "random"})
times, throughput , requests_handled= r20w80()
plt.plot(times, throughput, label = "Random")
requests.post(configurl, data={"cachesize": 0.05, "policy": "LRU"})
times, throughput , requests_handled= r20w80()
plt.plot(times, throughput, label = "LRU")
plt.title('Thoughput in 1 mins with 80w20r')
plt.xlabel("time")
plt.legend()
plt.ylabel("Requests handled")
plt.savefig("80w-20rthoughput.png")

print("20r 80w throughput in 1 mins: finished", requests_handled)