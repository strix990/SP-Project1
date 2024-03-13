import timeit
import secrets
from cryptography.hazmat.primitives import hashes

def Rlist():
    lista = [0 for _ in range(7)]
    for i in range(1,8,1):
        lista[i-1] = secrets.token_bytes(8**i)
    return lista

def Main():
    digest = hashes.Hash(hashes.SHA256()) #Creates a SHA-256 hash object
    data_list = Rlist()
    for i in data_list:
        hash_list_time = [0 for _ in range(10)]
        hash_mean_time = 0
        for x in range(10):
            start = timeit.default_timer()
            digest.update(i)
            hash_list_time[x] = timeit.default_timer() - start
            hash_mean_time += hash_list_time[x]
        hash_mean_time = hash_mean_time/10
        hash_string = "{:.10f}".format(hash_mean_time)        
        print("Mean time for 10 instances of a " + str(len(i)) + " bytes file: " + hash_string)
Main()
