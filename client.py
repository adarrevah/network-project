import socket
import threading

# 1. הגדרות התחברות (חייב להתאים לשרת)
SERVER_IP = '127.0.0.1'
PORT = 5555

# יצירת ה-Socket והתחברות לשרת
#socket.AF_INET - מציין שה-SOCKET ישתמש בפרוטוקול IPv4
#socket.SOCK_STREAM - מציין שה-SOCKET ישתמש בפרוטוקול TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# התחברות לשרת
client_socket.connect((SERVER_IP, PORT))

# 3. הזדהות ראשונית - שליחת שם המשתמש
username = input("enter your username: ")
# שליחת שם המשתמש לשרת
client_socket.send(username.encode('utf-8'))

# פונקציה להאזנה להודעות נכנסות
def receive_messages():
    while True:
        try:
            # המתנה להודעה מהשרת
            message = client_socket.recv(1024).decode('utf-8')
            # בדיקה אם התקבלה הודעה
            if message:
                # הצגת ההודעה למשתמש
                print(f"\n{message}")
                # בקשה מהמשתמש להקליד הודעה חדשה
                print("enter message (recipient:message): ", end="")
            # אם לא התקבלה הודעה, נצא מהלולאה
            else:
                break
        # טיפול בשגיאות
        except:
            print("the connection to the server was lost.")
            client_socket.close()
            break

# הפעלת ה-Thread להאזנה
# זה מאפשר לקבל הודעות בזמן שאנחנו מקלידים הודעה אחרת
# יצירת Thread להאזנה להודעות נכנסות
#target=receive_messages - מצביע על הפונקציה שתורץ בתוך ה-Thread
receive_thread = threading.Thread(target=receive_messages)
# התחלת ה-Thread
receive_thread.start()

# לולאת שליחת הודעות
print("you are connected to the chat! to send a message, use the format: recipient:message")
# שליחת הודעות לשרת
while True:
    # קריאת הודעה מהמשתמש
    msg = input("enter message (recipient:message): ")
    # בדיקה אם ההודעה לא ריקה
    if msg:
        # שליחת ההודעה לשרת
        client_socket.send(msg.encode('utf-8'))