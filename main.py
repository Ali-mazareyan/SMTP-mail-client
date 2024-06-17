from socket import *
from base64 import *
import ssl

userEmail = '*****************'
userPassword = '**********'
userDestinationEmails = input("Please enter your destination emails separated with comma: ")
userDestinationEmails = map(lambda x: x.strip() , userDestinationEmails.split(","))
userSubject = input("Enter Subject: ")
userBody = input("Enter Message: ")
attachment_file = "1111.jpg"
user_ask = input("Do you want to send any attachments? (yes or no): ")

# Read the attachment file data
if user_ask == 'yes':
    with open(attachment_file, 'rb') as attachment:
        attachment_data = attachment.read()
else:
    attachment_data = None

# The message body should not have a period at the beginning. The message should end with a single period on a line by itself.
msg = '{}\r\nEmail by Ali mazareyan'.format(userBody)
endmsg = "\r\n.\r\n"

mailserver = 'smtp.gmail.com'
mailPort = 587

for email in userDestinationEmails:
    # Create socket called clientSocket and establish a TCP connection with mailserver
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((mailserver, mailPort))

    recv = clientSocket.recv(1024).decode()
    print(recv)
    if recv[:3] != '220':
        print('220 reply not received from server.')

    heloCommand = 'HELO Ali\r\n'
    clientSocket.send(heloCommand.encode())
    recv1 = clientSocket.recv(1024).decode()
    print(recv1)
    if recv1[:3] != '250':
        print('250 reply not received from server.')

    # Send STARTTLS command and print server response.
    starttlsCommand = "STARTTLS\r\n".encode()
    clientSocket.send(starttlsCommand)
    recv2 = clientSocket.recv(1024)
    print(recv2)

    # Upgrade the socket to use SSL/TLS
    context = ssl.create_default_context()
    sslClientSocket = context.wrap_socket(clientSocket, server_hostname=mailserver)

    # Encode the email and password using base64
    emailA = b64encode(userEmail.encode())
    emailP = b64encode(userPassword.encode())

    authorizationCMD = "AUTH LOGIN\r\n"
    sslClientSocket.send(authorizationCMD.encode())
    recv3 = sslClientSocket.recv(1024)
    print(recv3)

    # Send the encoded email and print server response.
    sslClientSocket.send(emailA + "\r\n".encode())
    recv4 = sslClientSocket.recv(1024)
    print(recv4)

    # Send the encoded password and print server response.
    sslClientSocket.send(emailP + "\r\n".encode())
    recv5 = sslClientSocket.recv(1024)
    print(recv5)

    # Send MAIL FROM command and print server response.
    mailFrom = "MAIL FROM: <{}>\r\n".format(userEmail)
    sslClientSocket.send(mailFrom.encode())
    recv6 = sslClientSocket.recv(1024)
    print(recv6)

    rcptto = "RCPT TO: <{}>\r\n".format(email)
    sslClientSocket.send(rcptto.encode())
    recv7 = sslClientSocket.recv(1024)
    print(recv7)

    # Send DATA command and print server response.
    dataCMD = "DATA\r\n"
    sslClientSocket.send(dataCMD.encode())
    recv8 = sslClientSocket.recv(1024)
    print(recv8)

    # Send email headers
    emailHeaders = f"From: {userEmail}\r\nTo: {email}\r\nSubject: {userSubject}\r\nMIME-Version: 1.0\r\nContent-Type: multipart/mixed; boundary=myboundary\r\n\r\n"
    sslClientSocket.send(emailHeaders.encode())

    # Send email body
    sslClientSocket.send(("\r\n--myboundary\r\nContent-Type: text/plain; charset=UTF-8\r\n\r\n" + msg).encode())

    # Send attachment data
    if attachment_data:
        attachment = f"\r\n--myboundary\r\nContent-Disposition: attachment; filename={attachment_file}\r\nContent-Type: application/pdf\r\nContent-Transfer-Encoding: base64\r\n\r\n"
        sslClientSocket.send(attachment.encode())
        sslClientSocket.send(b64encode(attachment_data))
    
    # End email
    sslClientSocket.send(endmsg.encode())
    recv9 = sslClientSocket.recv(1024).decode()
    print(recv9)

    # Send QUIT command and print server response.
    quitCMD = "QUIT\r\n"
    sslClientSocket.send(quitCMD.encode())
    recv10 = sslClientSocket.recv(1024)
    print(recv10)

    sslClientSocket.close()