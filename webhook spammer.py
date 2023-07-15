import requests
import PySimpleGUI as sg
import emoji

def send_message(webhook_url, message, num_times, mention_everyone):
    for _ in range(num_times):
        if mention_everyone:
            message_with_mention = "@everyone " + message
        else:
            message_with_mention = message
        
        payload = {"content": message_with_mention}
        response = requests.post(webhook_url, json=payload)
        if response.status_code != 204:
            window["-OUTPUT-"].update(f"RATE LIMITED")
            break
    else:
        window["-OUTPUT-"].update("Message sent successfully!")

def delete_webhook(webhook_url):
    response = requests.delete(webhook_url)
    if response.status_code != 204:
        window["-OUTPUT-"].update(f"Failed to delete webhook. Error code: {response.status_code}")
    else:
        window["-OUTPUT-"].update("Webhook deleted successfully!")

# GUI layout
layout = [
    [sg.Text("Discord Webhook URL:")],
    [sg.Input(key="-WEBHOOK-")],
    [sg.Text("Message:")],
    [sg.Input(key="-MESSAGE-")],
    [sg.Text("Number of Times:")],
    [sg.Input(key="-NUM_TIMES-")],
    [sg.Checkbox("Mention @everyone", default=False, key="-MENTION_EVERYONE-")],
    [sg.Button("Send"), sg.Button("Delete")],
    [sg.Text(size=(50, 1), key="-OUTPUT-")]
]

# Create the window
window = sg.Window("Discord Webhook Sender", layout)

# Event loop
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    if event == "Send":
        webhook_url = values["-WEBHOOK-"]
        message = values["-MESSAGE-"]
        num_times = int(values["-NUM_TIMES-"])
        mention_everyone = values["-MENTION_EVERYONE-"]
        send_message(webhook_url, message, num_times, mention_everyone)
    if event == "Delete":
        webhook_url = values["-WEBHOOK-"]
        delete_webhook(webhook_url)

window.close()
