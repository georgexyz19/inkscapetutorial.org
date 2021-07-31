title: Get Started
slug: get-started
date: 2021-07-26 12:51
modified: 2021-07-26 12:51
category: inkscape
chapter: 1
note: record a case of linux mint crash

Last night my main computer with Linux Mint 20 crashed and I was really worried
that I might lose the files I had been working on.  After many google searches,
I found a solution and knew why it happened.  

The computer did not respond to mouse or keyboard input so I had to hold down
the power key for a few seconds to shut it off.  When the computer restarted,
it showed the Linux Mint login screen but the system did not let me log in. I
tried a few times entering my password and also tried to restart the computer,
but still could not log in. 

After some google searches, I found this online post

[(SOLVED) Cannot Login (login loop)](https://forums.linuxmint.com/viewtopic.php?f=57&t=261704)

I followed the answer by Lohengrines, did the following steps, and logged 
into the system.

1. In login screen, switch to terminal by pressing "Ctrl + Alt + F2"
2. Run the command `sudo tune2fs -m0 /dev/sda2`
3. Switch back to login screen "Ctrl + Alt + F7"
4. Login with user name and password


