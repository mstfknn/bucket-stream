import logging
from certstream.core import CertStreamClient
import time
import threading

logging.basicConfig(level=logging.INFO)

def process(message, context):
    print("SUCCESS: Mesaj alındı!")

print("Test basliyor (wss://certstream.calidog.io)...")
try:
    client = CertStreamClient(process, "wss://certstream.calidog.io", skip_heartbeats=True)
    # run_forever metodu bloklayıcı olduğu için thread içinde çalıştırıyoruz
    t = threading.Thread(target=client.run_forever)
    t.daemon = True
    t.start()
    
    # 10 saniye bekle
    start_time = time.time()
    while time.time() - start_time < 10:
        time.sleep(1)
        
except Exception as e:
    print(f"Hata: {e}")

print("Test bitti.")

