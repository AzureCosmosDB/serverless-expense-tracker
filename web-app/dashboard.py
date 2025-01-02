import streamlit as st
import asyncio
import websockets

async def listen_notifications():
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            st.sidebar.write(message)

st.title("Smart Expense Tracker")
st.sidebar.subheader("Live Notifications")
if st.button("Connect to Notifications"):
    asyncio.run(listen_notifications())
