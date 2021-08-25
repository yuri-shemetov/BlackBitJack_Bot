import smtplib
from email.mime.multipart import MIMEMultipart                          # Многокомпонентный объект
from email.mime.text import MIMEText                                    # Текст/HTML
from email.mime.image import MIMEImage                                  # Изображения
from . my_local_settings import ADDR_FROM, PASSWORD_FOR_EMAIL
from datetime import datetime
import email, imaplib

def get_new_email(servername='imap.yandex.ru'):
    subject = 'Your SSL Certificate'
    mail = imaplib.IMAP4_SSL(servername)
    mail.login(ADDR_FROM, PASSWORD_FOR_EMAIL)
    mail.list()
    mail.select('INBOX')
    (status, data) = mail.search(None, 'UNSEEN')
    money = 0

    if data != [b'']:
        for num in data[0].split():
            status, email_data = mail.fetch(num, '(RFC822)')
            raw_email = email_data[0][1]
            raw_email_string = raw_email.decode('utf-8')
            email_message = email.message_from_string(raw_email_string)

            # Header Details
            date_tuple = email.utils.parsedate_tz(email_message['Date'])
            if date_tuple:
                local_date = datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
                local_message_date = "%s" % (str(local_date.strftime("%a, %d %b %Y %H:%M:%S")))
            email_from = str(email.header.make_header(email.header.decode_header(email_message['From'])))
            email_to = str(email.header.make_header(email.header.decode_header(email_message['To'])))
            subject = str(email.header.make_header(email.header.decode_header(email_message['Subject'])))

            if subject == 'SMS to E-Mail, Отправитель: Reshenie':                              #<--- replace the text
                # Body details
                for part in email_message.walk():
                    if part.get_content_type() == "text/plain" or part.get_content_type() == "text/html":
                        body = part.get_payload(decode=True)
                        file_name = "message/email_" + str(num) + ".txt"
                        output_file = open(file_name, 'w', encoding='utf-8')
                        output_file.write("From: %s\nTo: %s\nDate: %s\nSubject: %s\n\nBody: \n\n%s" % (
                            email_from, email_to, local_message_date, subject, body.decode('utf-8')))
                        output_file.close()
                        
                        try:
                            with open(file_name) as f_obj:
                                contents = f_obj.read()
                                words = contents.split()
                                i = 0
                                for word in words:
                                    i += 1
                                    if word == 'CREDIT':                                          #<--- replace the text
                                        money = words[i]
                                        return money[:]
                        except:
                            return money
                    else:
                        continue
            else:
                return money
    else:
        return money

    mail.close()


"""def send_email(username, lastname, path_jpg):
    addr_from = ADDR_FROM                                                # Адресат
    addr_to = ADDR_TO                                                    # Получатель
    password = PASSWORD_FOR_EMAIL                                        # Пароль

    msg = MIMEMultipart()                                                # Создаем сообщение
    msg['From'] = addr_from                                              # Адресат
    msg['To'] = addr_to                                                  # Получатель
    msg['Subject'] = str(
        datetime.now().strftime('%d/%m/%y-%H:%M:%S')
        ) + ' получен чек проверки перевода'                             # Тема сообщения

    body = 'Получен чек от ' + username + ' ' + lastname                 # Add photo
    with open(path_jpg, 'rb') as fp:
        file = MIMEImage(fp.read())
        fp.close()
    file.add_header(
        'Content-Disposition', 'attachment',
        filename=username + '_' + lastname
        )

    msg.attach(MIMEText(body, 'plain'))                                  # Добавляем в сообщение текст
    msg.attach(file)

    server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)                     # Создаем объект SMTP
    #server.starttls()                                                   # Начинаем шифрованный обмен по TLS
    server.login(addr_from, password)                                    # Получаем доступ
    server.send_message(msg)                                             # Отправляем сообщение
    server.quit()                                                        # Выходим
"""