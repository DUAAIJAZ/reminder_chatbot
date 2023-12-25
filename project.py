import cProfile
import pstats
import unittest
from unittest.mock import patch
from datetime import datetime, timedelta
import time
import tkinter as tk
from tkinter import messagebox
from twilio.rest import Client

# Set your Twilio account credentials (replace with your actual credentials)
account_sid = 'your account sid'
auth_token = 'your auth token'
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
    time_str = time_entry.get()
    if not title or not time_str:
        messagebox.showerror("Error", "Please enter both title and time.")
        return

    time_obj = datetime.strptime(time_str, "%I:%M %p").time()
    current_time = datetime.now().time()

    # Check for valid time and schedule daily reminders
    if current_time < time_obj:
        reminder_time = datetime.combine(datetime.today(), time_obj)
        schedule_daily_reminders(title, reminder_time)
    else:
        reminder_time = datetime.combine(datetime.today() + timedelta(days=1), time_obj)
        schedule_daily_reminders(title, reminder_time)

# Function to schedule daily reminders
def schedule_daily_reminders(title, reminder_time):
    while datetime.now().time() < reminder_time.time():
        time.sleep(30)  # Check for reminder every 30 seconds

    send_whatsapp_message('your no here', f"Reminder: {title}")
    response = messagebox.askquestion("Task Completion", "Have you completed the task?")
    if response == 'yes':
        return

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

# Unit Test Class
class TestReminderApp(unittest.TestCase):
    def test_set_reminder(self):
        with patch("builtins.input", side_effect=["Test Title", ""]):
            root = tk.Tk()
            title_entry = tk.Entry(root)
            time_entry = tk.Entry(root)
            time_entry.insert(0, "")
            
            # Add an assertion to check if messagebox.showerror is called
            with patch.object(messagebox, 'showerror') as mock_showerror:
                set_reminder(title_entry, time_entry)
                mock_showerror.assert_called_once_with("Error", "Please enter both title and time.")

if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()
    main()
    profiler.disable()

    stats = pstats.Stats(profiler).sort_stats('cumulative')
    stats.print_stats()

