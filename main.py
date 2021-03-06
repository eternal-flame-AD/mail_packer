import mailhandler
import fileoper
import config
import ziphandler
import os


def check_new_mail():
    getter = mailhandler.EmailGetter(
        config.imap_host,
        config.mail_username,
        config.mail_passwd
    )
    return getter.iter_unseen()


def zip_file(folder, fn):
    zipfile = ziphandler.ZipHandler(fn)
    for fn_to_zip in os.listdir(folder):
        zipfile.append_file(folder + '/' + fn_to_zip)
    zipfile.close()


def send_zip(fn):
    email = mailhandler.EmailToSend(config.outsubject,
                                    config.sender,
                                    config.out_email_address)
    email.attach_file(fn, open(fn, mode="rb").read())
    sender = mailhandler.EmailSender(
        config.smtp_host,
        config.mail_username,
        config.mail_passwd,
    )
    sender.sendmail(email)


def send_report(to, origin):
    email = mailhandler.EmailToSend("Forward report for " + origin,
                                    config.sender,
                                    to)
    text = "Your file has been sucessfully forwarded.\r\n"
    text += "Original subject:" + origin + "\r\n"
    text += "Target:" + config.out_email_address + "\r\n"
    text += "Size: %.2f M\r\n" % (os.path.getsize(config.zipname)/1024/1024)
    text += "Here's a brief list of files forwarded: \r\n"
    zipfile = ziphandler.ZipHandler(config.zipname, mode="r")
    for f in zipfile.list_file():
        text += "\t{0} {1} {2}\r\n".format(f.filename,
                                           f.file_size,
                                           f.compress_size)
    zipfile.close()
    del zipfile
    email.attach_text(text)
    sender = mailhandler.EmailSender(
        config.smtp_host,
        config.mail_username,
        config.mail_passwd,
    )
    sender.sendmail(email)


def mail_valid(mail):
    if not (mail.sender in config.valid_sender):
        return False
    if not (mail.subject.startswith(config.valid_prefix)):
        return False
    return True


def main():
    for mail in check_new_mail():
        if mail_valid(mail):
            print("found:", mail.sender, mail.subject)
            folder = './mails/' + fileoper.randname() + "/"
            for fn, data in mail.iter_attachment():
                fileoper.write_file(folder + fn, data)
            zip_file(folder, config.zipname)
            send_zip(config.zipname)
            send_report(mail.sender, mail.subject)
            fileoper.delete_file_folder(folder)
            fileoper.delete_file(config.zipname)


main()
