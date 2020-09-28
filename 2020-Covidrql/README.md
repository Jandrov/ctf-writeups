# Write-up Covid rql

* [Crypto - Codebook](#crypto---codebook)
* [Stego - Keep Trying](#stego---keeptrying)

This was a <a href="http://155.138.239.104:8000/">short CTF</a> that one teammate told me about, as the prize for the winner was one year of VIP in HTB. It was late here in Spain but I decided to take part in the competition. It turned out to be interesting and I ended up 2nd with 800 points, just 100 points behind the winner. Only a few people solved some challenges: I started with Stego one but after getting stacked at some point, I changed to *Codebook* one and solved it. I was 3rd after 2 people that solved Stego one (it had more points). After that, this was the sequence...

<p align="center">
  <img src="imgs/result1.jpg">
</p>

I solved *babystack* 10 minutes before the deadline and I was in the first position! But it didn't last so long...

<p align="center">
  <img src="imgs/result2.jpg">
</p>

5 minutes after that, *th3d00msl4y3r* uploaded another flag and defeated me.  I was only one step away in the stego challenge from getting the prize! :( 

To sum up, I could solve a couple challenges and almost a third one, so I will try to share what I got. The writeup for *pwn* challenge might be done in the future if my teammate <a href="https://github.com/Zarkrosh">Zarkrosh</a> helps me, as he is the expert in the topic and helped me with the script. Then, I am writing about a *Crypto* challenge and the *stego* one I almost finished.

## Crypto - Codebook

Files: <a href="challs/codebook.py">codebook.py</a>

<p align="center">
  <img src="imgs/codebook_task.PNG">
</p>

From this challenge we get a server to connect by *netcat* and the Python script file that is running on that server. First thing I do is connect and try to test briefly how it works:

<p align="center">
  <img src="imgs/codebook1.PNG">
</p>

I see that server sends me an encrypted passphrase, asks me for something to decrypt and eventually asks me for the passphrase. I also notice that there is a timeout, so a script will need to be written. This is the moment when I start looking into the Python script and I see that the behaviour is:
1. Set timeout of 2 seconds and generate random key of 16 bytes
1. Generate passphrase of 32 random letters (upper or lower case)
1. Encrypt (with AES ECB and previous generated key) not only the passphrase but also *"Passphrase  is  "* right before it (the length of this prepended string is exactly **16 bytes**, what will be useful). Then send this encoded in hex
1. Receive our message to decrypt, but only allowing messages with length up to 64 bytes
1. Decrypt with AES ECB and the same key than before what we sent and then send it us back
1. Receive the passphrase we write and compare it with the originally generated one:
	1. If they match, we get the flag
	1. Otherwise, we get an error message and connection is closed

It was pretty clear for me that I needed to send their own encrypted message back in order to get the clear passphrase, but unfortunately it is longer than 64 bytes because of that prepended string (it has 96 bytes). Then, the challenge was just to **extract the correct bytes from the encrypted passphrase, send those back, receive the clear passphrase, send it back to the server and get the flag**. Why is this so simple? Because of <a href="https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Electronic_codebook_(ECB)">how ECB works</a>. 

<p align="center">
  <img src="imgs/codebook2.PNG">
</p>

It splits the message into blocks of 16 bytes and then encrypt each of them using the same key (for example, if you encrypt 32 characters "a", you would see twice the same encrypted message, as the first 16 "a" and the second 16 "a" were encrypted in the same way). Then, if we were so lucky that the prepended message was 16 (32 in hexadecimal) bytes long... Oh, wait, it was just like that! So we have everything we need to write the script and get our first flag (During the process mentioned before, we also need to receive the bytes that the server sends us like *"Decrypted message: "* just to ignore them).

Writing the script <a href="challs/solve.py">solve.py</a> didn't take me too long using *pwntools*, as it was only 10 lines of code and the only difficulty was seeing where to split the extracted strings. Once I had it, I got the flag.
 
<p align="center">
  <img src="imgs/codebook_solution.PNG">
</p>

**FLAG{ECB_IS_NOT_SECURE}**


## Stego - Keep Trying

Files: <a href="challs/photo.zip">photo.zip</a>

<p align="center">
  <img src="imgs/stego_task.PNG">
</p>

> Do you like stego. I hope that. You already know what to do.
> When you find the flag, use the following format: FLAG{INSERTFLAGHERE}"

I need to say that this challenge was the longest in stego I've ever had, but well, kind of entertaining though :)

We get a zip file that firstly I check with `7z l photo.zip` and then I extract with `7z x photo.zip`. Whatever decompressing tool is valid. I also checked if the zip had a comment with `zipnote photo.zip`, but nothing was found. 

<p align="center">
  <img src="imgs/stego1.PNG">
</p>

I get an image, so let's open it.

<p align="center">
  <img src="challs/photo.jpg">
</p>

There is a text that looks encrypted with just a rotation cipher. I write it on <a href="https://gchq.github.io/CyberChef/#recipe=ROT13(true,true,11)&input=QXAgcmFwa3QgdGhpcCB1Z3RjaXQgcCBpamggZHlkaA">Cyberchef</a> and it is decrypted with **ROT11** as *La clave esta frente a tus ojos* (in English *The key is in front of your eyes*). It made me think that there was a password protected file inside the image. But what was the password?

If we see the image, it shows a map of a region of the *<a href="https://en.wikipedia.org/wiki/Beleriand">Middle-earth</a>*, from *The Lord of the Rings* (I am not into LOTR, but I just googled the first name I saw on the map). Nothing seems clear, so I guessed that one of those names would be the password. I wasn't sure how to automate the process, so I just tried each name until I found that the password was **TALATH**. 

<p align="center">
  <img src="imgs/stego2.PNG">
</p>

I said "each name" because unfortunately I think I tried almost each of them before this one, I don't know why I chose that order... We get a text file and luckily this time I didn't waste a minute as I recognized the steganography technique at first glance: <a href="https://dl.packetstormsecurity.net/crypt/snow/description.html">**SNOW**</a>. It is easy to notice if you see the tabs and spaces on each line (just for the record, I also checked where that text came from and it was from *A Clockwork Orange* in Spanish).

<p align="center">
  <img src="imgs/stego3.PNG">
</p>

I extract the hidden text with **stegsnow** as you can see for example <a href="https://delightlylinux.wordpress.com/2016/12/14/hide-text-in-text-files-using-stegsnow/">here</a>:

<p align="center">
  <img src="imgs/stego4.PNG">
</p>

It is a <a href="https://github.com/uroven4/random">GitHub repository</a>, so let's check it. This is where the challenged started to have some parts of OSINT. There are 4 "hello world" files that doesn't seem to have anything interesting, so I check the commits and I find a couple with useful information. First one shows a link to an <a href="https://www.flickr.com/photos/189491566@N04/50160413911/">image on Flickr</a> and second one gives a future advice: 

> I come from the future to give you an advice.
> When you finish your journey, you must reduce the distances of what you are looking for.

<p align="center">
  <img src="imgs/stego5.PNG">
  <img src="imgs/stego6.PNG">
</p>