# AutomatischeBrauanzeigeBeimZoll
This is for German home brewers. A python script that sends an email every January 1st to your customs office (as is the law here) to announce your beer brewing intentions for the coming year.
Since I tend to forget about this, I wanted to automate it :-).

1. This script uses the SendGrid API (https://sendgrid.com/). They offer a free account for up to 100 emails per day, so more than enough for our 1 email per year...

2. You need to create a single sender in SendGrid, use an email address that you control.
3. Authenticate your sender email address with SendGrid.
4. Create a full-access API key for your newly authenticated sender and save it in a text file so we can read it into Python.


The Python script in this repository is ready to be used, you just have to adapt the variables in between the triple comment blocks - things like sender, recipient, your name, Hobby-Brauer-Nr. etc.

**I recommend to do a dry run first (where you have the script send an email to yourself)before you start bombarding the customs office!!!**

-------------------
## Automating via crontab

To automate the sending of our customs email, we will create a cronjob on a Debian-based Raspberry Pi. Of course, the machine you will use to run this script on every January 1st actually needs to be on during that time ;-). If you run a different flavor of Linux the commands should still be the same.

1. Edit crontab by executing:
    ```
    crontab -e
    ```
2. Add the following line. This will inscruct cron to execute your script at 12 pm every January 1st.
    ```
    0 12 1 1 * /usr/bin/python3 /path/to/ZollEmail_git.py > /same/path/cron.log 2>&1
    ```
    
3. Save & exit

4. You can check whether your entry is now in crontab by executing:
    ```
    crontab -l
    ```
5. I recommend that you test your crontab setup before relying on it by having it call your initial test script which sends an email to yourself. For this you just need to adjust the path to your script and then tell cron to execute it every 5 minutes (relative to the full hour):
    ```
    */5 * * * * /usr/bin/python3 /path/to/ZollEmail_git_TEST.py > /same/path/cron.log 2>&1
    ```


