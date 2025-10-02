import tkinter as tk
from tkinter import messagebox

def open_email_draft_window(to_address="", subject="", body=""):
    """
    Opens a Tkinter window for drafting an email.
    The window is pre-populated with the provided arguments.
    """
    def send_email():
        # This is a placeholder for the actual email sending logic.
        # In a future step, this would use the Gmail API to send the email.
        recipient = entry_to.get()
        subject_line = entry_subject.get()
        email_body = text_body.get("1.0", tk.END)

        if not recipient or not subject_line:
            messagebox.showwarning("Warning", "Please fill in the 'To' and 'Subject' fields.")
            return

        print("--- Email Draft ---")
        print(f"To: {recipient}")
        print(f"Subject: {subject_line}")
        print(f"Body:\n{email_body}")

        messagebox.showinfo("Info", "This is a demo. Email sending logic has not been implemented yet.")
        root.destroy()

    root = tk.Tk()
    root.title("Draft New Email")

    # 'To' field
    tk.Label(root, text="To:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_to = tk.Entry(root, width=50)
    entry_to.grid(row=0, column=1, padx=5, pady=5)
    entry_to.insert(0, to_address)

    # 'Subject' field
    tk.Label(root, text="Subject:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entry_subject = tk.Entry(root, width=50)
    entry_subject.grid(row=1, column=1, padx=5, pady=5)
    entry_subject.insert(0, subject)

    # 'Body' text area
    tk.Label(root, text="Body:").grid(row=2, column=0, padx=5, pady=5, sticky="nw")
    text_body = tk.Text(root, width=60, height=15)
    text_body.grid(row=2, column=1, padx=5, pady=5)
    text_body.insert(tk.END, body)

    # 'Send' button
    send_button = tk.Button(root, text="Send Email", command=send_email)
    send_button.grid(row=3, column=1, padx=5, pady=10, sticky="e")

    root.mainloop()

if __name__ == '__main__':
    # For testing the GUI window directly
    open_email_draft_window(to_address="test@example.com", subject="Hello", body="This is a test email.")