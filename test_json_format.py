import json
machine = input("Machine ID:")
position = input("Position ID:")
response = {
    "machine": machine,
    "command": "response",
    "status": True,
}
sleep = {
    "machine": machine,
    "command": "sleep",
}
force = {
    "machine": machine,
    "command": "force",
}
sendwave = {
    "machine": machine,
    "command": "sendwave",
    "position": position,
    "wave": 3,
    "shots": 6,
    "num_players": 3,
    "players": ["1A", "10B", "3C"],
    "scores": [100, 20, 225],
}
print("Response =>\n{}\n".format(json.dumps(response)))
print("Sleep =>\n{}\n".format(json.dumps(sleep)))
print("Force =>\n{}\n".format(json.dumps(force)))
print("Sendwave =>\n{}\n".format(json.dumps(sendwave)))

