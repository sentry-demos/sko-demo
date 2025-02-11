import random

def initialize_environment():
    return {
        "server_load": random.choice(["low", "medium", "high"]),
        "network_latency": random.randint(10, 100),  # in milliseconds
        "error_rate": random.uniform(0, 0.1),         # error rate as a fraction
    }

def update_environment(env):
    env["server_load"] = random.choice(["low", "medium", "high"])
    env["network_latency"] = random.randint(10, 150)
    env["error_rate"] = random.uniform(0, 0.15)
    
    return env 