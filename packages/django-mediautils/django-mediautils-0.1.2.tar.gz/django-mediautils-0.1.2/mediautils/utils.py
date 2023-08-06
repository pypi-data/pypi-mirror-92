# -*- coding: utf-8 -*-
import json
from uuid import uuid4
import mimetypes
import cv2
import os
import sys
import shutil
import magic
import random
#import magic
from PIL import Image, ImageDraw, ImageFont
from resizeimage import resizeimage

from django.conf import settings
import numpy
import logging
import hashlib
import traceback

from django.core.files.base import ContentFile
from django.core.files import File

TEMP_FILE_DIR = '/tmp/'

def hide_faces(img_file):
    """ Hide faces """
    cascades = [
            'haarcascade_frontalface_default.xml',
            'haarcascade_profileface.xml',
        ]
    casc_dir = ''.join([settings.BASE_DIR, '/perfil/cv_cascades/'])
    for casc in cascades:
        cascade_path = ''.join([casc_dir, casc])
        #blur_faces(img_file, cascade_path)
        try:
            blur_faces(img_file, cascade_path)
        except Exception as e:
            errolog = logging.getLogger('django')
            errolog.error(e)

def blur_faces(image_path, cascade_path):
    """ blur faces on an image """
    # Create the haar cascade
    face_cascade = cv2.CascadeClassifier(cascade_path)
    # Read the image
    image = cv2.imread(image_path)
    result_image = image.copy() # <<<<<<<<<<
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Detect faces in the image
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
        #flags = cv2.CV_HAAR_SCALE_IMAGE
    )
    #print("Found {0} faces!".format(len(faces)))
    # Blur the faces    
    for f in faces:
        # Get the origin co-ordinates and the length and width till where the face extends
        x, y, w, h = [ v for v in f ]
        # get the rectangle img around all the faces
        sub_face = image[y:y+h, x:x+w]
        # apply a gaussian blur on this new recangle image
        sub_face = cv2.GaussianBlur(sub_face,(91, 91), 30)
        # merge this blurry rectangle to our final image
        result_image[y:y+sub_face.shape[0], x:x+sub_face.shape[1]] = sub_face
        # grava soh a cara
        #face_file_name = "./face_" + str(y) + ".jpg"
        #cv2.imwrite(face_file_name, sub_face)
    cv2.imwrite(image_path, result_image)    
    return len(faces)

def cropa_imagem(img_file, larger=480, smaller=360, quality=1):#3x4 # 
    #if quality > 1:
    larger *= quality
    smaller *= quality
    cropamap = {
        'landscape': [larger, smaller],
        'portrait':  [smaller, larger],
        }
    try:
        orient = get_img_orientation(img_file)
        # converte pra jpg
        img = Image.open(img_file)
        img = img.convert('RGBA')
        background = Image.new("RGBA", img.size, "WHITE")
        background.paste(img, (0, 0), img) 
        img = background.convert('RGB')
        img.save(img_file, "JPEG", optimize=True, quality=80)

        fd_img = open(img_file, 'rb')
        img = Image.open(fd_img)
        img.thumbnail(cropamap[orient], Image.ANTIALIAS)
        img.save(img_file, "JPEG", optimize=True, quality=80)
        fd_img.close()
        ret = cropamap[orient]
    except Exception as e:
        ret = 'landscape'
        logging.error(e)
        #print (traceback.format_exc())
        if 'test' in sys.argv:
            raise e
        #raise
    return ret

#gif 
# how to crop gif https://stackoverflow.com/questions/9988517/resize-gif-animation-pil-imagemagick-python

def cropa_video(video_file, larger=320, smaller=240, quality=1):
    #if quality > 1:
    larger *= quality
    smaller *= quality
    #cropamap = {
        #'landscape': [larger, smaller],
        #'portrait':  [smaller, larger],
        #}
    try: #python2
        random_hex = uuid4().get_hex()
    except:
        random_hex = uuid4().hex
    file_temp = '/tmp/'+random_hex+'.mp4'
    # -vf scale=720:-2
    #opts = ' - vf scale='+str(larger)+':-2 '
    try:
        #+ ' -s '+str(larger) +'x'+ str(smaller)+' '
        #+ ' -c:v libx264 -preset slow -an -b:v 370K '
        #+ ' -c:a aac -movflags +faststart '
        #+ ''' -vf "scale='min('''+str(larger) +''',iw)':'min('''+str(smaller) +''',ih)'" '''
        cmd = ('/usr/bin/ffmpeg -hide_banner -loglevel error -i '
                    + video_file
                    + ' -vf scale='+str(larger)+':-2 '
                    + file_temp)
        #print(cmd)
        os.system(cmd)
        if os.path.isfile(file_temp):
            shutil.move(file_temp, video_file)
            #print('sucessful crop ', file_temp)
            return True
    except Exception as e:
        ret = 'landscape'
        logging.error(e)
        #print (traceback.format_exc())
        #raise
    return False
    #return ret

def rotate_image(img_file, direct='left'):
    """ rotate image """
    if direct=='left':
        angle = 90
    else:
        angle = -90
    fd_img = open(img_file, 'rb')
    img = Image.open(fd_img)
    rot = img.rotate(angle, expand=1, resample=Image.BICUBIC)
    fd_img.close()
    rot.save(img_file)
    
    
def get_img_orientation(img_file):
    """ Get the orientation of image """
    try:
        img = cv2.imread(img_file)
        height, width, channels = img.shape
        h, w = img.shape[:2]
        if h > w:
            return 'portrait'
        else:
            return 'landscape'
    except:
        return 'portrait'
        #print (traceback.format_exc())

# 65536
def md5sum(filename, blocksize=65536):
    """ Get md5sum from file """
    hashe = hashlib.md5()
    with open(filename, "rb") as f:
        for block in iter(lambda: f.read(blocksize), b""):
            hashe.update(block)
        f.close()
    return hashe.hexdigest()


def convert_tojpeg(arquivo_temp):
    """ convert image to jpeg """
    try:
        img = Image.open(arquivo_temp)
        img = img.convert('RGBA')
        background = Image.new("RGBA", img.size, "WHITE")
        background.paste(img, (0, 0), img) 
        img = background.convert('RGB')
        img.save(arquivo_temp, "JPEG", optimize=True, quality=80)
    except Exception as e:
        print('ERROR: convert_tojpeg', e)

def handle_upload_file(file_post=None,
                     Model=None,
                     #description=None,
                     #title=None,
                     extra_args={},
                     #thread=None,
                     #postage_type=None,
                     quality=1):
    """ handle a file upload """
    retorno = None
    #print ('postage_type', postage_type)
    # Crio um arquivo temporario
    try: #python2
        random_hex = uuid4().get_hex()
    except:
        random_hex = uuid4().hex
    # Save temp file in /tmp/
    arquivo_temp = TEMP_FILE_DIR + random_hex
    with open(arquivo_temp, 'wb') as temp_file:
        for chunk in file_post.chunks():
            temp_file.write(chunk)
        temp_file.close()
    extension = mimetypes.guess_extension(file_post.content_type, strict=True)
    if extension == 'jpe':
        # guess_extension eh bugado
        extension = 'jpg'
    if not extension:
        extension = ''
    # Calculo o md5 do arquivo pra decidir o nome q ele vai ter
    md5_hash = md5sum(arquivo_temp)
    filename = ''.join([md5_hash, extension])
    # renomeia o temp com a extensao
    arquivo_temp_ext = ''.join([arquivo_temp, extension])
    os.rename(arquivo_temp, arquivo_temp_ext)
    arquivo_temp = arquivo_temp_ext
    # Ate aqui, tenho um arquivo no tmp com nome md5.extensao
    # print ('file ', arquivo_temp)
    mime = magic.Magic(mime=True)
    mime_type = mime.from_file(arquivo_temp)
    # print(' mimes tites  ', mime_type)
    if not mime_type:
        mime_type = []

    retorno = handle_generic_file(arquivo_temp,
                                file_post,
                                filename,
                                quality=quality,
                                Model=Model,
                                extra_args=extra_args,
                                md5_hash=md5_hash)
    return retorno

def handle_generic_file(arquivo_temp,
                        file_post,
                        filename,
                        quality=1,
                        Model=None,
                        extra_args={},
                        md5_hash=None):
    if not Model:
        # hack for the sake of legacy
        from mediautils.models import Media
        Model = Media
    """ handle a generic file uplod and format it accordint to it's needs """
    #print('handle_generic_file', extra_args, Model)
    media = Model(**extra_args)
    mime = magic.Magic(mime=True)
    mime_type = mime.from_file(arquivo_temp)
    if 'image/gif' in mime_type:
        tipo = 'gif'
    elif 'image' in mime_type:
        tipo = 'image'
    elif 'video' in mime_type:
        tipo = 'video'
    elif 'audio' in mime_type:
        tipo = 'audio'
    elif 'application/octet-stream' in mime_type:
        tipo = 'gif'
    else:
        tipo = 'file'
    tipos_extensions = {
        'image': ['.jpg', '.jpg'],
        'gif': ['.gif', '.jpg'],
        }
    if tipo in tipos_extensions.keys():
        mainext, thumbext = tipos_extensions.get(tipo, ['.jpg', '.jpg'])
        fname_spl = filename.split('.')
        if len(fname_spl) > 0:
            first_name = fname_spl[0]
            filename = first_name+mainext
            thumbname = first_name+thumbext
        else:
            filename = filename+mainext
            thumbname = filename+thumbext
    else:
        thumbname = filename
    # 1 trata nome, isso tem q ser de acordo com tipo
    media.md5_hash = md5_hash
    media.content_type = mime_type
    if (('image/gif' in mime_type) or
        ('application/octet-stream' in mime_type)):
        arruma_gif(arquivo_temp)
    elif 'image' in mime_type:
        convert_tojpeg(arquivo_temp)
    foto_file = open(arquivo_temp, 'rb')
    media.media_file.save(filename, File(foto_file))
    foto_file.close()
    # thumbnail De acordo com o tipo de arquivo
    if tipo in ['image', 'gif']:
        thumb_file = open(arquivo_temp, 'rb')
        media.media_thumbnail.save(thumbname, File(thumb_file))
        thumb_file.close()
        # Cropa a imagem do thumbnail
        cropa_imagem(media.media_thumbnail.path, quality=quality)
    elif tipo == 'video':
        media.save()
        get_thumb_from_video(media)
    media.save()
    # Deleta o arq temporario
    os.remove(arquivo_temp)
    return media

def arruma_gif(arquivo_temp):
    """ arruma os gifs q vieram com mime 'application/octet-stream'
    """
    mime = magic.Magic(mime=True)
    mime_type = mime.from_file(arquivo_temp)
    if not mime_type:
        mime_type = []
    if ('application/octet-stream' in mime_type):
        # se for octet stream, tem q converter ele pra gif
        os.system('convert '+arquivo_temp+ ' ' + arquivo_temp+'.gif')
        if os.path.isfile(arquivo_temp+'.gif'):
            shutil.move(arquivo_temp+'.gif', arquivo_temp)
    
def get_thumb_from_video(video):
    
    try: #python2
        random_hex = uuid4().get_hex()
    except:
        random_hex = uuid4().hex
    thumbnail_temp = '/tmp/'+random_hex+'.jpg'
    
    cmd = ('/usr/bin/ffmpeg -hide_banner -loglevel panic -y -ss 1 -i '
                + video.media_file.path
                + ' -frames:v 1 -s 400x300 '
                + thumbnail_temp)
    os.system(cmd)
    if os.path.isfile(thumbnail_temp):
        #thumbnail
        thumb_file = open(thumbnail_temp, 'rb')
        video.media_thumbnail.save(os.path.basename(video.media_file.name), File(thumb_file))
        thumb_file.close()
        os.remove(thumbnail_temp)

def make_random_image(owner=None, thread=None):
    filename = random_image()
    arquivo_temp = '/tmp/'+filename
    
    foto = Media()
    foto.owner = owner
    foto.thread = thread
    # pega mime, 
    mime = magic.Magic(mime=True)
    mime_type = mime.from_file(arquivo_temp)
    
    foto_file = open(arquivo_temp, 'rb')
    foto.media_file.save(filename, File(foto_file))
    foto.media_thumbnail.save(filename, File(foto_file))
    foto_file.close()
    
    foto.description = 'default image'
    
    foto.text = 'default image'
    foto.text_original = 'default image'
    
    foto.title = 'default image'
    foto.content_type = mime_type
    foto.postage_type = 'avatar-p'
    foto.save()
    os.remove(arquivo_temp)
    return foto

def random_image():
    methods = [
            Image.AFFINE,
            Image.NEAREST,
            Image.BILINEAR,
            Image.BICUBIC,
            Image.LANCZOS, 
            Image.BOX,
            Image.HAMMING,
            ]
    r_method = random.choice(methods)
    r_size = random.randrange(3, 6, 2)
    r_color = random.randint(3, 4)
    imarray = numpy.random.rand(r_size, r_size, 3) * 255
    im = Image.fromarray(imarray.astype('uint8')).convert('RGB')
    im = im.resize((125,125), Image.BOX)
    random_name = uuid4().hex + '.jpg'
    im = im.convert('RGB')
    im.save('/tmp/'+random_name, "JPEG", optimize=True, quality=80)
    return random_name


def add_watermark(img_path,
                  text,
                  position=(0, 0),
                  color=(160, 160, 160),
                  font_type="Pillow/Tests/fonts/FreeMono.ttf",
                  font_size=12):
    """ adds a single watermark to the image """
    worked = False
    try:
        img = Image.open(img_path)
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(font_type, font_size)
        draw.text(position,text,fill=color,font=font)
        worked = True
    except:
        worked = False
    if worked:
        img.save(img_path)
        return img

def watermarks(img_path, text, color=(160, 160, 160)):
    """ adds a multiple watermarks to the image """
    #img = add_watermark(img_path, text, position=(10, 10), color=color)
    #idx = step
    try:
        img_handle = cv2.imread(img_path)
        if img_handle is not None:
            height, width, channels = img_handle.shape
            h, w = img_handle.shape[:2]
            offset = 40
            h_steps = int((h-offset) / 3)
            w_steps = int((w-offset) / 3)
            hrange = range(10,(h-offset), h_steps)
            wrange = range(10,(w-offset), w_steps)
            for pos in zip(wrange, hrange):
                img = add_watermark(img_path, text, position=pos, color=color)
    except:
        pass
    #else:
        #print('cant open image ', img_path)
  
        
        
        
    #img.show()
