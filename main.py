from fastapi import FastAPI, WebSocket
from typing import Dict, List

app = FastAPI()

# Dictionary mapping group IDs to lists of WebSocket connections
connected_groups: Dict[str, List[WebSocket]] = {}

# Dictionary to store the state for each group
group_states: Dict[str, bool] = {}


@app.websocket("/ws/{group_id}")
async def websocket_endpoint(websocket: WebSocket, group_id: str):
    await websocket.accept()

    # Initialize the list and state for new group IDs
    if group_id not in connected_groups:
        connected_groups[group_id] = []
        group_states[group_id] = False  # Default state, can be changed

    # Add the current websocket to the list of connected clients for this group
    connected_groups[group_id].append(websocket)

    # Send the current state to the newly connected client
    await websocket.send_json({"state": group_states[group_id]})

    try:
        while True:
            # Wait for a message from the client
            data = await websocket.receive_json()
            if "state" in data:
                # Update the state for the group and broadcast it
                group_states[group_id] = data["state"]
                await broadcast_state(group_id, group_states[group_id])
    except Exception as e:
        print(e)
        pass
    finally:
        # Remove client from the list upon disconnection
        connected_groups[group_id].remove(websocket)
        if not connected_groups[group_id]:
            # Remove the group_id key if no more connected clients
            del connected_groups[group_id]
            del group_states[group_id]  # Also remove the state for the group


async def broadcast_state(group_id: str, state: bool):
    # Broadcast the current state to all connected clients in the same group
    for client in connected_groups.get(group_id, []):
        try:
            await client.send_json({"state": state})
        except Exception:
            # Handle failed send (e.g., client disconnected)
            pass


@app.get("/")
def read_root():
    return {"Hello": "World"}
