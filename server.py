import socket #ספריה שמאפשרת ליצור SOCKETS
import threading #מאפשרת לבצע ריבוי משימות
# הגדרת כתובת ה-IP והפורט של השרת
IP = '127.0.0.1'
# הגדרת הפורט של השרת
PORT = 5555
# יצירת SOCKET מסוג TCP
#socket.AF_INET - מציין שה-SOCKET ישתמש בפרוטוקול IPv4
#socket.SOCK_STREAM - מציין שה-SOCKET ישתמש בפרוטוקול TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# קישור ה-SOCKET לכתובת IP ולפורט
server_socket.bind((IP, PORT))
# האזנה לכניסות נכנסות
server_socket.listen(5)
# מילון לשמירת הלקוחות המחוברים
clients = {}
def start_server():
    print(f"thr server listening to {IP}:{PORT}...")
    while True:
        # 1. קבלת חיבור חדש
        # הפקודה accept עוצרת ומחכה עד שמישהו יתחבר
        # כאשר מישהו מתחבר, היא מחזירה שני ערכים:
        # SOCKET חדש שמייצג את החיבור עם הלקוח
        # וכתובת ה-IP והפורט של הלקוח
        client_socket, client_address = server_socket.accept()
        print(f"new connection from {client_address}")

        # 2. יצירת Thread (תהליכון) עבור הלקוח
        # כאן אנחנו עומדים בדרישה של "5 לקוחות בו-זמנית"
        # אנחנו שולחים את הלקוח לפונקציה handle_client (שנכתוב בשלב 3)
        # יצירת פונקציה לטיפול בלקוח
        # הפונקציה תקבל את ה-SOCKET של הלקוח כפרמטר
        # הפונקציה תרוץ בתוך Thread נפרד
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

        print(f"number of active clients: {threading.active_count() - 1}")

# פונקציה לטיפול בלקוח
def handle_client(client_socket):
    try:
        #קבלת שם המשתמש (הודעה ראשונה מהלקוח)
        #recv(1024) השרת עוצר ומחכה לקבל נתונים מהלקוח
        #1024 זה גודל הבופר (כמה בתים לקרוא בכל פעם)
        #decode('utf-8') ממיר את הנתונים הבינאריים למחרוזת
        username = client_socket.recv(1024).decode('utf-8')
        # שמירת הלקוח במילון הלקוחות המחוברים
        clients[username] = client_socket
        print(f"the user {username} successfully connected.")
        # לולאה לטיפול בהודעות מהלקוח
        while True:
            # המתנה להודעה מהלקוח
            data = client_socket.recv(1024).decode('utf-8')
            # בדיקה אם הלקוח ניתק
            if not data:
                break
            # אם התקבלה הודעה, נטפל בה
            if ":" in data:
                # פיצול ההודעה לשם הנמען ולתוכן ההודעה
                #data.split(":", 1) מחלק את המחרוזת לשני חלקים בלבד
                # החלק הראשון הוא שם המשתמש של הנמען
                # החלק השני הוא ההודעה עצמה
                target_user, message = data.split(":", 1)
                
                # ניתוב ההודעה לנמען המתאים
                # בדיקה אם הנמען מחובר
                if target_user in clients:
                    # שליחת ההודעה לנמען
                    # קבלת ה-SOCKET של הנמען מהמילון
                    recipient_socket = clients[target_user]
                    # יצירת ההודעה המלאה עם שם השולח
                    full_message = f"message from {username}: {message}"
                    # שליחת ההודעה לנמען
                    recipient_socket.send(full_message.encode('utf-8'))
                # אם הנמען לא מחובר, נשלח הודעה לשולח
                else:
                    # שליחת הודעה לשולח שהנמען לא מחובר
                    client_socket.send(f"the user {target_user} is not connected.".encode('utf-8'))

    except:
        # טיפול בשגיאות תקשורת
        # כאן ניתן להוסיף קוד לטיפול בשגיאות
        pass
    finally:
        # ניקוי וסגירה בניתוק
        # הסרת הלקוח מהמילון
        if username in clients:
            # הסרת הלקוח מהמילון
            del clients[username]
        # סגירת ה-SOCKET של הלקוח
        client_socket.close()
        print(f"the connection with {username} has ended.")
        
# קריאה לפונקציה כדי שהשרת יתחיל לעבוד
# start_server()
