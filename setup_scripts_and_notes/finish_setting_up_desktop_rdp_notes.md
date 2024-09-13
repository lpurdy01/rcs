Run 'install_desktop_env.sh'

You have to register port 3389 as an allowed incoming port on azure.

Setup a PW for azureuser: 'sudo passwd azureuser'

Add a xfce session to the you .xsession file: 'echo "xfce4-session" >~/.xsession'

Restart xrdp `sudo systemctl restart xrdp`

You should now be able to login using RDP to the server.

