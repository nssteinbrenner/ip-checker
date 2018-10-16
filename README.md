# ip-checker
Checks to see if my public IP has changed

Connects to my pfSense router vs SSH and checks to see if my public IP has changed. Sends a text and an e-mail if it has. Useful for when I want to connect to my home network via VPN.

Utilizes a config file, format is below. Be sure to note the spaces, as they are important for reading the file.

username: {router ssh username}                                                                                                                                                                                                                               
password: {router ssh password}                                                                                                                                                                                                                   
emailpass: {password for mailfrom addr}                                                                                                                                                                                                            
hostname: {hostname of router}                                                                                                                                                                                                                          
to: {text addr, eg 123123123@vtext.com} {email addr}                                                                                                                                                                                            
from: {mailfrom addr}                                                                                                                                                                                               
port: {port on router to connect to}
