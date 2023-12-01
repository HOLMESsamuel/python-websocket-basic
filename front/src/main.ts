class WebSocketClient {
  private ws: WebSocket | null = null;
  private toggleButton: HTMLButtonElement;

  constructor(toggleButton: HTMLButtonElement) {
      this.toggleButton = toggleButton;
  }

  public connect(clientId: string): void {
      this.ws = new WebSocket(`ws://localhost:8000/ws/${clientId}`);

      this.ws.onopen = () => {
          console.log("WebSocket connected");
      };

      this.ws.onmessage = (event) => {
          const data = JSON.parse(event.data);
          console.log("Received:", data);
          this.updateToggleButton(data.state);
      };

      this.ws.onerror = (error) => {
          console.error("WebSocket error:", error);
      };

      this.ws.onclose = () => {
          console.log("WebSocket connection closed");
      };
  }

  private updateToggleButton(state: boolean): void {
      this.toggleButton.textContent = state ? "On" : "Off";
      this.toggleButton.style.display = "";
  }

  public toggleState(): void {
      const currentState = this.toggleButton.textContent === "On";
      const newState = !currentState;
      this.ws?.send(JSON.stringify({ state: newState }));
  }
}

const clientIdInput = document.getElementById("ws-id") as HTMLInputElement;
const connectButton = document.getElementById("connect-btn") as HTMLButtonElement;
const toggleButton = document.getElementById("toggle-btn") as HTMLButtonElement;

const wsClient = new WebSocketClient(toggleButton);

connectButton.addEventListener("click", () => {
  const clientId = clientIdInput.value.trim();
  if (clientId) {
      wsClient.connect(clientId);
  } else {
      console.error("Please enter a WebSocket ID");
  }
});

toggleButton.addEventListener("click", () => {
  wsClient.toggleState();
});

