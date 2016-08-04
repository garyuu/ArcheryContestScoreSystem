import mqtt_client
import tcp_server
import Thread

def mqtt_thread_function():
    

def tcp_thread_function():


tcp_thread = Thread(target = mqtt_thread_function, args = [])
tcp_thread.start()
mqtt_thread = Thread(target = mqtt_thread_function, args = [])
