# MassFacebookGroupPoster

Mass Facebook group poster is a program that will post any message you want to any amount of groups you wish to post too.

This program will run in the open background, allowing you to do anything while the program is running.

### Before Launching Program:
Make sure you use the command `pip install -r requirements.txt` in terminal first.

Before launching the program, you must change the emailText and passwordText values in the program, to allow the program to login on the Facebook website with your email and password.

The emailText variable is located on line 194, and you must input your email inbetween the double quotation marks.

The passwordText variable is located on line 195, and you must input your password inbetween the double quotation marks.

### How to Add Groups:
In the groups folder, create any 'name.list' file, the extension must be .list or the program will not find it. You can create multiple of these files, based on group category, name, anything you would like. In these files you must paste the full facebook group link with a new line separating them. I have provided a couple files in the groups folder to use as a reference.

### How to Edit Post Message:
To edit your post message, type what you want to post into the file 'postText.txt'. Spaces, special chars, newlines are all okay, write the message as your normally would on Facebook. Emojis are the exception, as they do not work with the program.

### How to Launch:
Make sure 'groups' folder, 'postText.txt' file, and 'chromedriver.exe' file are all in the same dir as 'MFGP.py'. To launch the program, just double click 'MFGP.py' or use the command `python MFGP.py` in terminal.

### How to Use:
When in the menu, where the printed text that says 'Available Group Files to Pick:' and such. You are to enter the number assigned to the file listed right of the number.

If you want to remove a group you added for posting, type in ':r1' without the quotes, and 1 being the number assigned to the left of the file name.

If you want to select all files, type in ':a' without the quotes.

Once you have selected the group files you want for posting type in ':p' without the quotes to begin posting.
