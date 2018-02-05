import ftplib
import configparser

#setup URL and username
ftpURL = "nwdropbox.centralus.cloudapp.azure.com"
username = "iotftp"

#proxy info (only needed if running on enterprise network)
session = ftplib.FTP()
session.connect("localhost",3128)


print("made it here")
#read config file containing password
configs = configparser.ConfigParser()
configs.read("C:/ws/filescripts/config.ini")
passwd = destination_dir = configs.get("Passwords", "iotftp")
session = ftplib.FTP(ftpURL,username,passwd)

#start session
msg = session.login(username+"@"+ftpURL,passwd)

print(msg)