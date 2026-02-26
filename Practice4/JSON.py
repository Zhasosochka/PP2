import json
with open('Practice4/sample-data.json') as f:
    data = json.load(f)

print("Interface Status")
print("=" * 90)
print(f"{'DN':<50} {'Description':<20} {'Speed':<10} {'MTU':<10}")
print("-" * 90)


for item in data["imdata"]: # Loop through the "imdata" list. each 'item' is a dictionary
    a = item["l1PhysIf"]["attributes"]

    dn = a["dn"] # Retrieving values using keys from the dictionary
    descr = a["descr"]
    speed = a["speed"]
    mtu = a["mtu"]
    print(f"{dn:<50} {descr:<20}  {speed:<10}  {mtu:<10}")