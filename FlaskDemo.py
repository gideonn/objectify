####### Author: Abhishek Srivastava ######

from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, IMAGES
import os

import argparse
import base64
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from google.cloud import translate
from gtts import gTTS

import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

app = Flask(__name__,static_url_path='/static')
photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/images'
app.config['UPLOAD_FOLDER'] = 'static/images'
configure_uploads(app,photos)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
###

def identifyandtranslate(photo_file,filename,lang):
    """Run a label request on a single image"""

    # [START authenticate]
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('vision', 'v1', credentials=credentials)
    # [END authenticate]

    # [START construct_request]
    with open(photo_file, 'rb') as image:
        image_content = base64.b64encode(image.read())
        service_request = service.images().annotate(body={
            'requests': [{
                'image': {
                    'content': image_content.decode('UTF-8')
                },
                'features': [{
                    'type': 'LABEL_DETECTION',
                    'maxResults': 1
                }]
            }]
        })
        # [END construct_request]

        # [START parse_response]
        response = service_request.execute()
        label = response['responses'][0]['labelAnnotations'][0]['description']
        print('Found label: %s for %s' % (label, photo_file))
        # [END parse_response]

        #Call translator API for translation to intended language
        print("Converting to language: " + str(lang))
        # Instantiates a client
        translate_client = translate.Client()

        # The text to translate
        text = label
        # The target language
        target = lang

        # Translates some text into Russian
        translation = translate_client.translate(
            text,
            target_language=target)

        print(u'Text: {}'.format(text))
        print(u'Translation: {}'.format(translation['translatedText']))
        translated_text = translation['translatedText']

        #Covert text to voice
        tts = gTTS(text=translated_text, lang=lang)
        tts.save(photo_file + ".mp3")

        #Overlay translation here
        font1 = ImageFont.truetype("static/fonts/GOTHIC.TTF", 60)
        font2 = ImageFont.truetype("static/fonts/NotoSansUI-Regular.ttf", 60)
        if(lang == "hi"):
            font2 = ImageFont.truetype("static/fonts/hindi.ttf", 60)
        elif lang == "zh-CN" or lang == "zh-TW":
            font2 = ImageFont.truetype("static/fonts/simsun.ttc", 60)
        tcolor = (0, 0, 0)
        text_pos = (50, 50)

        img = Image.open(photo_file)
        draw = ImageDraw.Draw(img)
        draw.text(text_pos, text, fill=(255,255,255,128), font=font1)
        del draw

        img.save(photo_file)

        text_pos = (50, 150)
        draw = ImageDraw.Draw(img)
        draw.text(text_pos, translated_text, fill=(255,255,255,128), font=font2)
        del draw

        img.save(photo_file)

        return(translated_text)

###

@app.route('/')
# @app.route('/<name>')
def main_page():
    return render_template('/index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        lang = request.form.get('select')
        print(filename)
        print(request.form.get('select'))
        # return 'file uploaded successfully'
        #Call identifyandtranslate here
        full_path = os.path.abspath(str("static/images/" + filename))
        transtext = identifyandtranslate(full_path, filename, lang)

    return render_template('uploadResults.html', filename=filename, full_path="static/images/" + filename, transtext = transtext)


if __name__ == '__main__':
    app.run()
