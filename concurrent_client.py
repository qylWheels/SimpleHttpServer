import concurrent.futures
import requests
import time

def send_request(n):
    _ = requests.get('http://localhost:8910/hello')
    print(f'thread {n} received a response from server')

start = time.time()

with concurrent.futures.ThreadPoolExecutor(16) as executor:
    requests_number_list = [i for i in range(100)]
    executor.map(send_request, requests_number_list)
    executor.shutdown()

end = time.time()
print(f'time elapsed: {end - start:.2f}s')
