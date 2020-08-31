import threading

class MacGenerator():
   def __init__(self):
        self.mac_value = 1
        self.lock = threading.Lock()


   def format_mac(self,mac):
      # convert mac in canonical form (eg. 00:80:41:ae:fd:7e)
      mac = ":".join(["%s" % (mac[i:i+2]) for i in range(0, 12, 2)])

      return mac



   def increment(self):
      self.lock.acquire()
      self.mac_value += 1
      
      mac = "{:012X}".format(int("0", 16) + self.mac_value)

      self.lock.release()
        
      return mac 
