
from DataStructures.Map.map_functions import hash_value, next_prime
from DataStructures.Map import map_entry as me
from DataStructures.List import array_list as lt
import random


def new_map(num_elements: int, load_factor: float, prime=109345121) -> dict:
    capacity = next_prime(num_elements // load_factor)

    scale = random.randint(1, prime - 1)
    shift = random.randint(0, prime - 1)

    table = [{
        "key": None,
        "value": None,
    }] * capacity

    current_factor = 0
    limit_factor = load_factor
    size = 0

    return {
        "prime": prime,
        "capacity": capacity,
        "scale": scale,
        "shift": shift,
        "table": table,
        "current_factor": current_factor,
        "limit_factor": limit_factor,
        "size": size
    }

def put(my_map: dict, key, value):
    if my_map["size"] / my_map["capacity"] >= my_map["limit_factor"]:
        rehash(my_map)

    hv = hash_value(my_map, key)
    ocupied, first_avail = find_slot(my_map, key, hv)
    
    if first_avail is not None:
        my_map["table"][first_avail] = {"key": key, "value": value}
        if not ocupied:
            my_map["size"] += 1
            my_map["current_factor"] = my_map["size"] / my_map["capacity"]

def contains(my_map, key):
    hv = hash_value(my_map, key)
    ocupied, first_avail = find_slot(my_map, key, hv)
    return ocupied

def get(my_map, key):
    hv = hash_value(my_map, key)
    ocupied, first_avail = find_slot(my_map, key, hv)
    val = None
    if ocupied:
        val = me.get_value(my_map["table"][first_avail])
    return val

def remove(my_map, key):
    hv = hash_value(my_map, key)
    ocupied, first_avail = find_slot(my_map, key, hv)
    val = None
    if ocupied:
        val = me.get_value(my_map["table"][first_avail])
        my_map["table"][first_avail] = ({
            "key": None,
            "value": None
        })
        my_map["size"] -= 1
    return val

def find_slot(my_map, key, hv):
    first_avail = None
    found = False
    ocupied = False
    while not found:
        if is_available(my_map["table"], hv):
            if first_avail is None:
                first_avail = hv
            entry = my_map["table"][hv]
            if me.get_key(entry) is None:
                found = True
        elif comparar(key, my_map["table"][hv]) == 0:
                first_avail = hv
                found = True
                ocupied = True
        hv = (hv + 1) % my_map["capacity"]
    return ocupied, first_avail

def is_available(table, pos):
    entry = table[pos]
    if me.get_key(entry) is None or me.get_key(entry) == "__EMPTY__":
        return True
    return False


def comparar (key, entry):

    if key == me.get_key(entry):
        return 0
    elif key > me.get_key(entry):
        return 1
    return -1


def size(my_map):
    return my_map["size"]

def is_empty(my_map):
    return size(my_map) == 0

def rehash(my_map):
    table_previa = my_map["table"]
    capacity = next_prime(2 * my_map["capacity"])

    my_map["table"] = [{
        "key": None,
        "value": None,
    }] * capacity
    my_map["capacity"] = capacity
    my_map["size"] = 0

    for entry in table_previa:
        if me.get_key(entry) is not None and me.get_key(entry) != "__EMPTY__":
            put(my_map, me.get_key(entry), me.get_value(entry))
    
    return my_map