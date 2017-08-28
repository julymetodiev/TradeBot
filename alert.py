import boto.ses
import datetime
import config

def get_utc_time_with_offset(offset=0):
    date = datetime.datetime.utcnow()
    H = [i for i in range(24)]*2
    hour = H[date.hour+24+offset]
    time = str(hour).zfill(2) + ":" + str(date.minute).zfill(2)
    return time


def get_utc_time():
    return get_utc_time_with_offset()


def get_pacific_time():
   return get_utc_time_with_offset(-7)
    

def get_email_recipients_from_file(fname="email_list.txt"):
    recipients = []
    try:
        f = open(fname, 'r')
        for line in f:
            recipients.append(line)
    except IOError:
        print("Email recipient file not valid. Defaulting to backup email address.")
        recipients.append(config.BACKUP_EMAIL_ADDRESS)
    return recipients


def send_email_alert(header, body):
    conn = boto.ses.connect_to_region('us-west-2')
    conn.send_email(
            config.SENDER_EMAIL_ADDRESS,
            header,
            body + " (Executed at " + get_pacific_time() + " PST, " + get_utc_time() + " UTC)",
            get_email_recipients_from_file())


if __name__ == "__main__":
    send_email_alert("Trade alert!", "Bought Bitcoin.")