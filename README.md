# MassFacebookGroupPoster v2.0.0

MassFacebookGroupPoster is a powerful program that simplifies and automates posting messages to multiple Facebook groups. With this tool, you can efficiently manage and automate your group postings, saving you time and effort.

## Preparing to Use the Program

Before running the program, please follow these steps:

1. **Install Required Dependencies:**
    Ensure you have the necessary Python packages installed by running the following command in your terminal:
    'pip install -r requirements.txt'

2. **Configure Your Facebook Login Credentials:**
Open the txt file named "UP.txt" and input your email and password there, please to not remove the comma. The format must be like "asd@gmail.com, qwerty123" (without the quotations) for the program to read the file properly.

## Adding Facebook Groups

You can specify the Facebook groups you want to post to by creating '.list' files in the 'groups' directory. Each '.list' file can contain multiple group URLs, with each URL on a new line. The 'groups' folder is provided with example group list files for reference.

## Editing the Post Message

To customize the post message, open the 'postText.txt' file and write your desired message. You can include spaces, special characters, and newlines as you normally would on Facebook. Please note that emojis are not supported by the program.

## Adding an Image to Your Post

To include an image in your post, click on the button that says "Add Image" and navigate to the image you want to add, select it and then click the open button on the bottom right of the explorer window. Be aware that when using an image, the program uses the computers clipboard, so do not copy anything while the program is running because it will then post what you newly copied to the system clipboard.

## How to Launch

To run the program, ensure that the 'groups' folder and 'postText.txt' file are all located in the same directory as 'MFGP.py'. Double-click 'MFGP.py' or use the command `python MFGP.py` in the terminal to start running the program.

## How to Use

When the program menu appears, select groups by clicking on the grey arrow pointing down on the right side of the GUI, and then clicking the "Add Group" button.

- To remove a group, select the group in the grey box by using the grey arrow on the right side of the GUI and clicking the "Remove Group" Button.
- To select all groups, click the "Add All Groups" button.
- To deselect all groups, click the "Remove All Groups" button.
- To remove the image selected, click the "Remove Image" button.

If you changed the group list files whle the program is running please click the button that says "Refresh Group File Selection List" to refresh the group files list and their contents in the program.

Once you have selected the group files, and an image if you want to add an image to the post, click the button that says "Start Posting" at the bottom of the GUI to begin posting.

### Enjoy using MassFacebookGroupPoster to streamline your Facebook group postings!
