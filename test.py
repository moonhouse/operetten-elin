from anyio import connect_tcp, run

def decode(messages):
    for message in messages:
        first_digit = [47<x<58 or x==13 for x in message].index(True)
        command=message[0:first_digit].decode()
        payload = message[first_digit:]

        match command:
            case 'FL':
                display = ""
                try:
                    display = bytes.fromhex(bytes(payload).decode()).decode('latin-1')
                except ValueError as err:
                    print(f"Error decoding display data {err}")
                    print(message)
                print(f"[DISP] {display}")
            case 'VOL':
                print(f"Volume set {payload}")
            case 'VU':
                print(f"Volume increased")
            case 'VD':
                print(f"Volume decreased")
            case 'AST': 
                last_as = payload
            case 'RGC':
                last_rg = payload
            case 'MUT':
                print(f"Volume muted status {payload}")
            case 'KOF':
                print("KOF")
            case 'CLRLC': 
                print("CLRLC") #Clear last command?
            case 'GCH': # New block in stream?
                print(payload)
            case 'GDH': # New block in stream?
                print(payload)
            case 'GEH': # New ID3 data in stream?
                id = int(payload[0:5])
                data = payload[5:].decode("utf-8")
                mapping = {1020: "Title", 4022: "Station", 5024: "Genre", 6026: "Format", 7029: "Bitrate"}
                if id in mapping:
                    print(f"{mapping[id]}: {data}")
                else:
                    print(f"{id}: {data}")
#                     2023: "98:17"
# 3021: ""
# 4022: "Radio Wix"
# 5024: "Pop"
# 6026: "mp3"
# 7029: "128kbps"
# 8031: "0"
# 9034: "0:00"
                #GEH01020"Hammarkinds_OK"
            case _:
                print("Unknown command")
                print(message, flush=True)

async def main():
    async with await connect_tcp('192.168.1.112', 8102) as client:
        while True:
            response = await client.receive()
            messages = response.split(b'\r\n')
            messages.remove(b'')
            decode(messages)

run(main)

#b'FL027420596F75204B6E6F7720202020\r\nRGC111110113001111112111111101201\r\n'

# GBH09
# GCH02010100000000200""
# GDH000010000100001
# GEH01020"djpacemaker - aug-19-2022"
# GEH02023"0:00"
# GEH03021""
# GEH04022"Radio Wix"
# GEH05024"Pop"
# GEH06026"mp3"
# GEH07029"128kbps"
# GEH08031"0"
# GEH09034"0:00"
# GHH00

# b'GBH09\r\n'
# Unknown command
# b'GCH02010100000000200""\r\nGDH000010000100001\r\nGEH01020"Johnny Cash - Look For Me"\r\nGEH02023"30:12"\r\nGEH03021""\r\nGEH04022"Radio Wix"\r\nGEH05024"Pop"\r\nGEH06026"mp3"\r\nGEH07029"128kbps"\r\nGEH08031"0"\r\nGEH09034"0:00"\r\nGHH00\r\n'
# [DISP] John
