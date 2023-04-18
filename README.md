# Distinctiveness and Complexity
### My project, QR Letter, is completely different from the Newtwork and Commerce project.
### While the CS50 lectures have enormously influenced my computer science journey, I have discovered the possibility and ability of the QR code usage myself. 
### I firslty tried to display the URL itself which lands on the letter page, but I thought "Hmm, if you open the webpage via URLs anyway, what is the advantage or uniqueness of the QR code?"
### So I started searching about QR codes ability to display the letter content on the mobile screen like 
 - How much data it can have 
 - What if the user write a 1000 + char letter 
 - If it display image
 - If dataframes  such as pandas work better for the structure 
 - If the huge data can be compressed and still display the same data after the compressed data be stored
 and so on..

 ### The conclusion is
### **Not much data**.

 ### Although you can technically store the data into the QR code but when it generates the code, the QR bar codes become really crowded and the scanner can not read the code.  
<br>

 ### You can store the image data but when you scan the QR code, it appears as binary (numeric letters).  
<br>

 ### I kind of made the structure of the letter in Line 30 in views.py in a very authentic way but it turned out to be the best way I could ever discover after tried with pandas but the dataframes have more complex data to be stored so it would have taken more effort to accomplish that way, and the QR code would get crowded.
 ### The maximum char limit was 250 on my end which my 2019 cell phone can read from the 13 inch screen, but just in case, I set the limit to 220.

 ### It was pretty impressive I finally made the letter message appear on the smartphone itself, I even did not expect that way.   
 <br>

 ### This time it is a letter themed app, because I happened to come up with the idea of **raining** + **thunder** + **letter**that's from the ending of ***Back to the Future 2*** and could not stop going this way and designing the background with the CSS animation and the vintage-like font and its atmospher. 
 <br>

 ### However, from now on, it can be utilized in many ways like a pet shop or a veterinary clinic which clients can store the animal data, owners' addresses and print out the QR code and tag it to the animals, so that the doctors can get to know the info or strayed pets can be found sooner.
<br>

### As this project is focused on the QR code discovery per se, and its extraordinary artistic design, I declare my capstone project, QR Letter, is completely distinctive from the CS50w course projects. 
<br>

## What the Pages Contains
<br>

### Register/ Login / Logout
- I now implemented the *forgot password* feature.
I added its routes on the project's urls.py, made corresponding templates.  
The reset email (develpement) is sent to the terminal window, you can access the link, then change the password
<br>

### All Letters Page
- All the letters which users have sent are displayed  but not disclosed. Users can like/ unlike the letter, and open it being excited. If the letter has a gifted image, it displays. Now you can scan the QR code and see who is revealing the secret!
<br>

### Make Profile/ Profile Pages
- You can create your profile, and if you alrady have it, it rejects you after the submission. You can keep the image blank.

- In the profile page, you can follow/ unfollow the other users. It shows the categories and the QR code which the user has sent.

### QR Letter
- Click the title, it leads you to the write letter/ index page.
You can give it a title and body which will be displayed on the QR code scanner, and an image gift, select a category from Bucket List, Romance, Hip-Hop like lyrics, and diary.

### Category/ Category Detail Page
- It shows the category list. You can go to the desired category detail page where you can click each letter to display the QR code.

### Backup Data
- I am very having fun to discover possibilities on the back end. I came up with the idea like "What if the client wanted to back up data?" I made the backup view and used jason as a backup formant and used JavaScript to give a user a confirmation alert whether they really want to download or not. If the do, it downlads as a JSON file and will be stored in your local computer. 
- For this feature, I just discovered the ability for backup and its usage in the future as it could be very controversial if I really implement this in the production for this kind of app. Ha!

### Mobile Responsive
This web app is mobile responsive as I manipulate it in CSS which has the media only attribute and JavaScript.


## Additional Information
- The python qrcode library installation has been tricky on mac on my end. If so, please try it with Homebrew.