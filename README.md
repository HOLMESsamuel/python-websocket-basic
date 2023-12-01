### Python websocket basic

This project is a basic websocket running on python with fastAPI framework on uvicorn ASGI server.
In the front directory the is a vanilla vite.js frontend to demonstrate the websocket.
You can subscribe to a group of client with an id and share a common state represented by the toogle button.

## How to run

1. run command : pip install requirements.txt
2. run command : uvicorn main:app --reload
This starts the python API and reloads it if there is any change
3. cd to the front directory
4. run command : npm install
5. run command : npm run dev
6. go to localhost with designated port