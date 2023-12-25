import cProfile
import pstats
from datetime import datetime, timedelta, time
import time
import tkinter as tk
from tkinter import messagebox
from twilio.rest import Client  # Imported Client from twilio.rest

# Set your Twilio account credentials (replace with your actual credentials)
account_sid = 'AC1d0795857f033d1afb36a36f75108b23'
auth_token = '2e2d5c0ec42725704ece7747b8603adc'
client = Client(account_sid, auth_token)

# Function to send a WhatsApp message using Twilio
def send_whatsapp_message(to, body):
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=body,
        to='whatsapp:' + to
    )
    print("Message sent successfully!")

# Function to set a reminder
def set_reminder(title_entry, time_entry):
    title = title_entry.get()
    time_str = time_entry.get()  # Access both entries through arguments
    time_obj = datetime.strptime(time_str, "%I:%M %p").time()  # Extract time component
    current_time = datetime.now().time()  # Get current time

    # Check for valid time and schedule daily reminders
    if current_time < time_obj:
        reminder_time = datetime.combine(datetime.today(), time_obj)
        schedule_daily_reminders(title, reminder_time)
    else:
        reminder_time = datetime.combine(datetime.today() + timedelta(days=1), time_obj)
        schedule_daily_reminders(title, reminder_time)

# Function to schedule daily reminders
def schedule_daily_reminders(title, reminder_time):
    while True:
        current_time = datetime.now().time()
        if current_time >= reminder_time.time():
            send_whatsapp_message('+923201240820', f"Reminder: {title}")
            response = messagebox.askquestion("Task Completion", "Have you completed the task?")
            if response == 'yes':
                break

        time.sleep(30)  # Check for reminder every 30 seconds

        # Calculate next reminder time for the following day
        reminder_time += timedelta(days=1)

# Main function
def main():
    # Create Tkinter window
    root = tk.Tk()
    root.title("Reminder App")

    # Create and place widgets in the window
    title_label = tk.Label(root, text="Enter the title of the reminder:")
    title_label.pack()

    title_entry = tk.Entry(root)
    title_entry.pack()

    time_label = tk.Label(root, text="Enter the time for the reminder (HH:MM AM/PM):")
    time_label.pack()

    time_entry = tk.Entry(root)
    time_entry.pack()

    set_reminder_button = tk.Button(root, text="Set Reminder", command=lambda: set_reminder(title_entry, time_entry))
    set_reminder_button.pack()

    exit_button = tk.Button(root, text="Exit", command=root.destroy)
    exit_button.pack()

    # Run Tkinter main loop
    root.mainloop()

if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()
    main()
    profiler.disable()

    stats = pstats.Stats(profiler).sort_stats('cumulative')
    stats.print_stats()
