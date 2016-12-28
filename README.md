![enter image description here](https://i.imgur.com/TtgGMEE.png)

Overview
===================
Have you ever traveled to a country and you didn't know the local language ? 
There's some object right in front of you but you don't know what it's called, in the local language.
For example, Beer is called Cerveza in Spanish. How'd a Japanese person know that ? 
What if you could have an assistant that can translate things that you see and speak it out for you?

Presenting **Objectify!**

All you need to do is :- 
 1. click on upload 
 2. select the image from gallery/take a snap from mobile
 3. select the language you want the object in image to be translated
    to 
 and, that's it.

The app will speak out aloud the translation with the converted text written on the image itself.
Works fine on cell phones too.
The app takes in language and image as an input, identifies an object in the image, and then translates and speaks out the object in translated language alongwith overlaying translated text onto the original image.


----------


## Demo:
You can see the app live here: https://goo.gl/DQcB0z

----------
## Installation:

The app is written in Python3.
Check the requirements.txt to know which additional packages are needed.
I'm listing the major ones here:

    - flask 
    - flask_uploads 
    - google-api-python-client 
    - google-cloud-core
    - google-cloud-translate 
    - gTTS 
    - pillow

I used Apache for hosting the app on EC2 instance - Objectify! (https://goo.gl/DQcB0z). 
As with any other apache backed web app, you need a .wsgi file and a .conf file.
I've added the working versions in the source, you're free to modify them for your own apps.

     1. Clone the repo to /var/www/objectify 
     2. Install the dependencies listed in requirements.txt 
     3. Copy the .conf file to /etc/apache2/sites-available/ directory 
     4. Keep the .wsgi in your app directory (in the same folder as your .py) 
     5. Generate your ServiceAccount.json from Google Cloud console and place the json
        file in some directory. You'll also need to export a variable
        GOOGLE_APPLICATION_CREDENTIALS with the path of this json file to
        make the Google API calls.
     6. Run the apache server! I had hosted this app on Amazon EC2.

All css files are in static/css, in case you want to tinker with those.

I'd love to have an android app having the same functionality but with much better UX.
