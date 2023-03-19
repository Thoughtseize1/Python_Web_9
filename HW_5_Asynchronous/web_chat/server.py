import asyncio
import logging
import re
from datetime import date

import websockets
import names
from websockets import WebSocketServerProtocol, WebSocketProtocolError
from websockets.exceptions import ConnectionClosedOK

from functions import make_urls_for_days, get_exchange, get_once_exchange, log_exchange_command

logging.basicConfig(level=logging.INFO)

TODAY_EXCHANGE_LINK = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'
TODAY_DATE = date.today().strftime("%d.%m.%Y")


class Server:
    clients = set()

    async def register(self, ws: WebSocketServerProtocol):
        ws.name = names.get_full_name()
        self.clients.add(ws)
        logging.info(f"{ws.remote_address} connects")

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logging.info(f"{ws.remote_address} disconnects")

    async def send_to_clients(self, message: str):
        if self.clients:
            [await client.send(message) for client in self.clients]

    async def send_to_client(self, message: str, ws: WebSocketServerProtocol):
        await ws.send(message)

    async def ws_handler(self, ws: WebSocketServerProtocol):
        await self.register(ws)
        try:
            await self.distrubute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)

    async def distrubute(self, ws: WebSocketServerProtocol):
        async for message in ws:
            if message.lower() == "exchange":
                result = await get_once_exchange()
                await self.send_to_client(f"Exchange rate for today: {TODAY_DATE}", ws)
                await log_exchange_command(ws.name)
                await self.send_to_client(result, ws)
            elif message.lower().startswith("exchange") and re.search(r'\d', message):
                days = message.split()[1]
                links = make_urls_for_days(int(days))
                results = await get_exchange(links)
                # await self.send_to_clients(r)
                for m in results:
                    await self.send_to_client(m, ws)
                await log_exchange_command(ws.name)
            else:
                await self.send_to_clients(f"{ws.name}: {message}")


async def main():
    server = Server()
    async with websockets.serve(server.ws_handler, "localhost", 8080):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
