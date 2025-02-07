from fastapi import WebSocket
from core.llm_integration import EnterpriseLLMEngine

class WSConnectionManager:
    def __init__(self):
        self.active_connections = []
        
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        
    async def stream_response(self, query: str):
        llm = EnterpriseLLMEngine()
        for token in llm.stream(query):
            for connection in self.active_connections:
                await connection.send_text(token)

manager = WSConnectionManager()

async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            query = await websocket.receive_text()
            await manager.stream_response(query)
    except:
        manager.disconnect(websocket)
