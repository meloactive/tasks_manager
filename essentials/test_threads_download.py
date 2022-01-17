import pandas as pd
import requests
import sys, time, io
import threading

def speed_test(size=1, ipv="ipv4", port=80, http='socks4://123.49.53.170:5678',https='socks4://123.49.53.170:5678'):
    
    if size == 1024:
        size = "1GB"
    else:
        size = f"{size}MB"

    url = f"http://{ipv}.download.thinkbroadband.com:{port}/{size}.zip"
    speed = 0

    with io.BytesIO() as f:
        start = time.time()
        r = requests.get(url, proxies=dict(http=http, https=https), stream=True)
        total_length = r.headers.get('content-length')
        dl = 0
        if total_length is None: # no content length header
            f.write(r.content)
        else:
            for chunk in r.iter_content(1024):
                dl += len(chunk)
                f.write(chunk)
                done = int(30 * dl / int(total_length))
                # sys.stdout.write("\r[%s%s] %s Mbps" % ('=' * done, ' ' * (30-done), dl//(time.time() - start) / 100000))
                speed = dl//(time.time() - start) / 100000 / 8

    # print( f"\n{size} = {(time.time() - start):.2f} seconds")
    with open('test.txt', "a") as tests:
        tests.write(http + " : " + str(speed))
    return print(http + " : " + str(speed))


# speed_test(size=5, ipv="ipv4", port=80, http="")

def for_thread_request(http='socks4://123.49.53.170:5678', https='socks4://123.49.53.170:5678'):
    try:
        conn_timeout = 6
        read_timeout = 60
        timeouts = (conn_timeout, read_timeout)
        resp = requests.get('http://ifconfig.me', proxies=dict(http=http, https=https, timeout=timeouts))
        if resp.status_code == 200:
            print ('OK!')
            print(resp.content)
            speed_test(size=1, ipv="ipv4", port=80, http=http , https=https)
        else:
            print ('Boo!')
    except requests.exceptions.RequestException as err:
        # print ("OOps: Something Else",err)
        pass
    except requests.exceptions.HTTPError as errh:
        # print ("Http Error:",errh)
        pass
    except requests.exceptions.ConnectionError as errc:
        pass
        # print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        pass
        # print ("Timeout Error:",errt)
    # return print(resp.status_code)


url = 'http://proxydb.net/?protocol=socks4&country=BD'

tables = pd.read_html(requests.get(url,
                                   headers={'User-agent': 'Mozilla/5.0'}).text,)
# print(len(tables))
for d in tables:
    print(len(d['Proxy'][0]))
    for i in range(len(d['Proxy'][0])-7):
    # for i in range(15):    
        print("so it was like that: " + d['Proxy'][i])
        try:
            t1 = threading.Thread(target=for_thread_request, args=('socks4://' + d['Proxy'][i],'socks4://' + d['Proxy'][i]))
            t1.start()
            # t2 = threading.Thread(target=speed_test, args=(1, "ipv4", 80, 'socks4://' + d['Proxy'][i],'socks4://' + d['Proxy'][i]))
            # t2.start()
            # t1.join()
            # resp = requests.get('http://ifconfig.me', proxies=dict(http='socks4://' + d['Proxy'][i], https='socks4://' + d['Proxy'][i]))
            # if resp.status_code == 200:
            #     print ('OK!')
            #     # print(resp.content)
            # else:
            #     print ('Boo!')
        except requests.exceptions.RequestException as err:
            print ("OOps: Something Else",err)
        except requests.exceptions.HTTPError as errh:
            print ("Http Error:",errh)
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:",errc)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:",errt)     


                           
