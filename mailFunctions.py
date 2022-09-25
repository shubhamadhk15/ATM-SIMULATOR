import smtplib

# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)

# start TLS for security
s.starttls()

# Authentication
s.login("ankityadav64872@gmail.com", "Ankit@123")

# message to be sent
message = "Hii, just for test"

# sending the mail
s.sendmail("ankityadav64872@gmail.com", "ankit6686482@gmail.com", message)

# terminating the session
s.quit()
