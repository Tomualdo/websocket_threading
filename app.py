import threading
import websocket, json, time

class CoinbaseWebsocket(threading.Thread):
    def __init__(self):
        # websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp("wss://ws-feed.exchange.coinbase.com",
                                on_message = self.on_message,
                                on_error = self.on_error,
                                on_close = self.on_close,
                                on_open = self.on_open)
        
        self.product_list = []
        threading.Thread.__init__(self)
        

    def set_products(self, product_list: list):
        self.product_list = list(product_list)

    def on_open(self, ws):
        print("opened connection")
        subscribe_message = {
        "type": "subscribe",
        "channels":[ 
            {
                "name": "ticker",
                "product_ids":
                
                    self.product_list,
                
                }]}

        self.ws.send(json.dumps(subscribe_message))
    
    def on_message(self, ws, message):
        print(message)
                
    def on_error(self, ws, mes):
        print("Error:", mes)

    def on_close(self, ws, close_status_code, close_msg):
        print(f"### closed ### {close_status_code} {close_msg} {ws}")
    
    def run(self):
        self.ws.run_forever()
    
    def is_connected(self):
        return self.ws.sock.connected

    def terminate(self):
        self.ws.sock.close()
    

threads = []
t1 = CoinbaseWebsocket()
t1.set_products(["ADA-EUR", "BTC-EUR"])

t2 = CoinbaseWebsocket()
t2.set_products(["DOT-EUR", "XTZ-EUR"])

t3 = CoinbaseWebsocket()
t3.set_products(["OMG-EUR"])

threads.append(t1)
threads.append(t2)
threads.append(t3)


for thread in threads:
    thread.daemon = True
    thread.start()


time.sleep(10)
print(f"Terminating: {t1._name}")
t1.terminate()
time.sleep(10)














# for thread in threads:
#     while thread.is_connected():
#         time.sleep(2)
#         print(f"SOCKET IST: {thread._name}")
        # thread.join()
# except KeyboardInterrupt:
    # for thread in threads:
        # thread.close()
        # thread.kill()


