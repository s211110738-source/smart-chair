import tkinter as tk
import paho.mqtt.client as mqtt
import threading

# --- CONFIGURATION ---
BROKER = "broker.emqx.io"
TOPIC = "insyirah/data"

class PhoneApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chair Monitor")
        # Set size to fit phone screen
        self.root.geometry("350x600") 
        self.root.configure(bg="#212121")

        # --- TITLE ---
        tk.Label(root, text="SMART CHAIR", font=("Roboto", 20, "bold"), 
                 bg="#212121", fg="#03DAC6").pack(pady=30)

        # --- WEIGHT SECTION ---
        self.frame_w = tk.Frame(root, bg="#333333", pady=20)
        self.frame_w.pack(fill="x", padx=20, pady=10)
        
        tk.Label(self.frame_w, text="WEIGHT (kg)", bg="#333333", fg="#B0B0B0").pack()
        self.lbl_weight = tk.Label(self.frame_w, text="0.0", 
                                   font=("Arial", 40, "bold"), bg="#333333", fg="white")
        self.lbl_weight.pack()

        # --- DISTANCE SECTION ---
        self.frame_d = tk.Frame(root, bg="#333333", pady=20)
        self.frame_d.pack(fill="x", padx=20, pady=10)

        tk.Label(self.frame_d, text="DISTANCE (cm)", bg="#333333", fg="#B0B0B0").pack()
        self.lbl_dist = tk.Label(self.frame_d, text="0", 
                                 font=("Arial", 40, "bold"), bg="#333333", fg="white")
        self.lbl_dist.pack()

        # --- STATUS INDICATOR ---
        self.lbl_status = tk.Label(root, text="CONNECTING...", 
                                   font=("Arial", 14, "bold"), bg="#CF6679", fg="black", height=3)
        self.lbl_status.pack(side="bottom", fill="x")

        # --- START MQTT ---
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        
        # Run network in background
        threading.Thread(target=self.start_mqtt, daemon=True).start()

    def start_mqtt(self):
        try:
            self.client.connect(BROKER, 1883, 60)
            self.client.loop_forever()
        except:
            pass

    def on_connect(self, client, userdata, flags, rc):
        self.client.subscribe(TOPIC)
        self.lbl_status.config(text="WAITING FOR DATA...", bg="#FF9800")

    def on_message(self, client, userdata, msg):
        try:
            # Decode "weight,distance"
            payload = msg.payload.decode()
            data = payload.split(",")
            weight = float(data[0]) / 1000.0 # Convert g to kg
            dist = int(data[1])

            # Update Screen
            self.lbl_weight.config(text=f"{weight:.2f}")
            self.lbl_dist.config(text=f"{dist}")

            # Logic
            if weight > 0.1: # Someone is sitting (100g)
                if dist < 20:
                    self.lbl_status.config(text="⚠️ BAD POSTURE", bg="#CF6679") # Red
                else:
                    self.lbl_status.config(text="✅ GOOD POSTURE", bg="#03DAC6") # Teal
            else:
                self.lbl_status.config(text="⚪ EMPTY", bg="#757575") # Grey

        except:
            print("Error parsing data")

# --- RUN ---
if __name__ == "__main__":
    root = tk.Tk()
    app = PhoneApp(root)
    root.mainloop()
