import os
# print("sdfsdf")
# os.system("echo 'HELLO'")
os.system("sudo systemctl stop privoxy")
os.system('sudo mv /etc/privoxy/config /etc/privoxy/config.bak')

proxy = input("Paste your proxy: ")
pattern = "forward-socks4   / "

config_backup = open(r'/etc/privoxy/config.bak','r')  # open config_backup handle for read
# use r'', you don't need to replace '\' with '/'
# open config_backup handle for write, should give a different config_backup name from previous one
main_config = open('config', 'w')  

for line in config_backup:
    line = line.strip('\r\n')  # it's always a good behave to strip what you read from config_backups
    if pattern in line:
        line = "forward-socks4   /  " + str(proxy) + " ." # if match, replace line
    main_config.write(line + '\n')  # write every line

config_backup.close()  # don't forget to close config_backup handle
main_config.close()


os.system("sudo mv config /etc/privoxy/config")
os.system("sudo chown privoxy:root /etc/privoxy/config")
os.system("sudo systemctl restart privoxy")
# os.system("sudo systemctl status privoxy")

