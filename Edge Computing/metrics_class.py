import time
from statistics import mean, stdev
import requests

class LatencyMeasurement:
    def __init__(self):
        self.latencies = {
            'end_to_end': [],
            'processing': [],
            'network': []
        }

    def measure_end_to_end_latency(self, start_time):
        end_time = time.time()
        latency = (end_time - start_time) * 1000  # Convert to milliseconds
        self.latencies['end_to_end'].append(latency)
        return latency

    def measure_processing_latency(self, func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            latency = (end_time - start_time) * 1000  
            self.latencies['processing'].append(latency)
            return result
        return wrapper

    def measure_network_latency(self, url):
        start_time = time.time()
        response = requests.get(url)
        end_time = time.time()
        latency = (end_time - start_time) * 1000  
        self.latencies['network'].append(latency)
        return latency

    def get_latency_stats(self, latency_type):
        latencies = self.latencies[latency_type]
        if not latencies:
            return None
        return {
            'min': min(latencies),
            'max': max(latencies),
            'avg': mean(latencies),
            'std_dev': stdev(latencies) if len(latencies) > 1 else 0
        }

