import random
import smtplib
import ssl
from email.message import EmailMessage

chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!§$%&/()="


class Confirm:

    def confirm_pwd(self):
        for lk in range(1):
            self.password = ""
            for ts in range(0, 7):
                password_char = random.choice(chars)
                self.password = self.password + password_char
            print(self.password)
            return self.password

    def send_mail(self):
        email_sender = 'pappysouls@gmail.com'
        email_password = 'rjtislvcyoyxktvb'
        email_receiver = self.root.get_screen('signupscreen').ids.emailadd.text

        subject = 'Comd DB Confirmation Password'
        body = self.password

        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())


confirm = Confirm()
confirm.confirm_pwd()
confirm.send_mail()
