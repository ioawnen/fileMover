"""Handles all the email shittery"""
import smtplib
from pushbullet import Pushbullet

#EMAIL
EMAIL_USERNAME = ""
EMAIL_PASSWORD = ""
EMAIL_SMTP = ""
EMAIL_PORT = 0
EMAIL_FROM = EMAIL_USERNAME
EMAIL_RECEPIENTS = [""]

#PUSHBULLET
PUSHBULLET_API_KEY = "v1hmVjM2E3vpL3dYWxcITXvaLPVrJsvY9sujBZBedFvJ6"

def sendEmail(subject, body, username = EMAIL_USERNAME, password = EMAIL_PASSWORD, smtp = EMAIL_SMTP, port = EMAIL_PORT, email_from = EMAIL_FROM, recepients = EMAIL_RECEPIENTS):
	# Prepare actual message
	message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
	""" % (email_from, ", ".join(recepients), subject, body)
	try:
		#server = smtplib.SMTP(SERVER)
		server = smtplib.SMTP(smtp, port) #or port 465 doesn't seem to work!
		server.ehlo()
		server.starttls()
		server.login(username, password)
		server.sendmail(email_from, recepients, message)
		#server.quit()
		server.close()
		print('\nSENDING NOTIFICATION EMAIL TO '+str(recepients))
	except Exception as ex:
		print(ex)


def sendPushbulletNotification(title, body, api_key = PUSHBULLET_API_KEY):

	pb = Pushbullet(api_key)
	push = pb.push_note(str(title), str(body))
