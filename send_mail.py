import smtplib
from email.mime.text import MIMEText

def send_mail(voter, pollsite, rating, comments):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = '5e49e1f73e9542'
    password = '2754d3d3de6975'
    message = f"<h3>New Feedback Submission</h3><ul><li>Voter: {voter}</li><li>Voting Site: {pollsite}</li><li>Rating: {rating}</li><li>Comments: {comments}</li>"
    
    sender_email = 'email@example.com'
    receiver_email = 'email2@example.com'
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'Voting Site Feedback'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    #Send email
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())