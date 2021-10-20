from my_module.db_manage import DB_Manager
import asyncio

host = "192.168.0.66"
port = "5321"

async def run_client(host: str, port: int, payload: dict):
    reader: asyncio.StreamReader
    writer: asyncio.StreamWriter
    reader, writer = await asyncio.open_connection(host, port)

    # Send data to WC-Robo
    print(f"[INFO] Sending data to {host}:{port}")
    print(f"       Payload:{payload}")
    writer.write(payload.encode())

    # Wait for response from WC-Robo
    resp = await reader.read(8)
    resp = resp.decode()

def test(a):
    print("hello")

if __name__ == "__main__":
    dbm = DB_Manager()
    dbm.startListen()
