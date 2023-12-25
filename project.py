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
account_sid = 'ur auth sid'
auth_token = 'ur auth token'
client = Client(account_sid, auth_token)

def send_whatsapp_message(to, body):
    '''
    Sends a WhatsApp message using Twilio.

    Args:
        to (str): The recipient's phone number.
        body (str): The message body.
    '''
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=body,
        to='whatsapp:' + to
    )
    print("Message sent successfully!")

def set_reminder(title_entry, time_entry):
    '''
    Sets a reminder based on user input.

    Args:
        title_entry (tk.Entry): The entry field for the reminder title.
        time_entry (tk.Entry): The entry field for the reminder time.
    '''
    title = title_entry.get()
    time_str = time_entry.get()
    if not title or not time_str:
        messagebox.showerror("Error", "Please enter both title and time.")
        return

    time_obj = datetime.strptime(time_str, "%I:%M %p").time()
    current_time = datetime.now().time()

    if current_time < time_obj:
        reminder_time = datetime.combine(datetime.today(), time_obj)
        schedule_daily_reminders(title, reminder_time)
    else:
        reminder_time = datetime.combine(datetime.today() + timedelta(days=1), time_obj)
        schedule_daily_reminders(title, reminder_time)

def schedule_daily_reminders(title, reminder_time):
    '''
    Schedules daily reminders.

    Args:
        title (str): The reminder title.
        reminder_time (datetime): The reminder time.
    '''
    delta_time = (reminder_time - datetime.now()).total_seconds()
    if delta_time > 0:
        time.sleep(delta_time)
        send_whatsapp_message('add yr number', f"Reminder: {title}")
        response = messagebox.askquestion("Task Completion", "Have you completed the task?")
        if response == 'yes':
            return

def main():
    '''
    Creates the main Tkinter window and sets up the reminder app.
    '''
    root = tk.Tk()
    root.title("Reminder App")

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

    root.mainloop()

class TestReminderApp(unittest.TestCase):
    def test_set_reminder(self):
        '''
        Tests the set_reminder function with empty user input.
        '''
        with patch("builtins.input", side_effect=["Test Title", ""]):
            root = tk.Tk()
            title_entry = tk.Entry(root)
            time_entry = tk.Entry(root)
            time_entry.insert(0, "")
            
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

