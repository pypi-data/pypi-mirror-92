import os
import magic
from django.conf import settings
from mediautils.utils import (cropa_imagem, cropa_video,
                              get_thumb_from_video, watermarks)

def _still_trying(post):
    """ Checks that the task that formats the media is still running
    """
    post.format_tries += 1
    #post.save()
    if post.format_tries > 5:
        # ja ta tentando tempo demais, zera ele
        post.formated = False
        post.format_tries = 0
        post.save()
        return True
    elif post.format_tries > 1:
        # maior q 1 mas nao > 5, nao faz nada, continua tentando
        post.format_tries += 1
        post.save()
        return True
    return False


def formata_all_media(Model=None):
    """ Manipulate media files as needed
    """
    wsize = 480
    hsize = 360
    watermark = getattr(settings, 'MEDIAUTILS_WATERMARK', None)
    watermark_finger = getattr(settings, 'MEDIAUTILS_WATERMARK_FINGER', False)
    #color = (160, 160, 160)
    mime = magic.Magic(mime=True)
    lista_video = Model.objects.filter(formated=False,
                                       content_type__contains='video/')
    for video in lista_video:
        if _still_trying(video):
            #print ("_still_trying video ", video.id)
            continue
        #print ("formatando video ", video.id)
        video.formated = cropa_video(video.media_file.path,
                                     larger=wsize, smaller=hsize)
        get_thumb_from_video(video)
        video.content_type = mime.from_file(video.media_file.path)
        video.save()

    ## Fotos, cropa todas as imagens
    lista_post = Model.objects.exclude(content_type='image/gif').filter(formated=False, content_type__contains='image/')
    for post in lista_post:
        if _still_trying(post):
            #print ("_still_trying foto ", post.id)
            continue
        #print ("formatando foto ", post.id)
        if post.media_file:
            cropa_imagem(post.media_file.path, quality=2)
        if post.media_thumbnail:
            cropa_imagem(post.media_thumbnail.path, quality=1)
        post.formated = True
        post.save()
        if watermark:
            if watermark_finger:
                water_text = ' '.join([watermark, post.md5_hash[0:8]])
            else:
                water_text = watermark
            watermarks(post.media_file.path, water_text)
            watermarks(post.media_thumbnail.path, water_text)
    ## Arruma os gifs bichados
    #lista_post = Photo.objects.filter(formated=False, content_type__contains='octet-stream')
    #print(lista_post)
    #for post in lista_post:
        #if _still_trying(post):
            #continue
        ##cropa_imagem(post.media_file.path, quality=2)
        ##cropa_imagem(post.media_thumbnail.path, quality=1)
        #arruma_gif(post.media_file.path)
        #post.formated = True
        #post.save()
    # agora os gifs
    lista_post = Model.objects.filter(formated=False, content_type='image/gif')
    for post in lista_post:
        if _still_trying(post):
            continue
        if post.content_type != 'image/gif':
            #print(post.content_type)
            cropa_imagem(post.media_file.path, quality=2)
        cropa_imagem(post.media_thumbnail.path, quality=1)
        post.formated = True
        post.save()

    lista_post = Model.objects.filter(formated=False).exclude(content_type__contains=['image/', 'video/'])
    for post in lista_post:
        if _still_trying(post):
            continue
        os.system('/usr/bin/clamscan --remove=yes '+post.media_file.path)
        # TODO melhorar isso aqui (vai demorar)
        if not os.path.isfile(post.media_file.path):
            #return False
            post.delete()
        else:
            post.formated = True
            post.save()

def watermark_past_images(Model=None):
    """ adds a watermark to already stored images
    """
    lista_post = Model.objects.exclude(content_type='image/gif').filter(
                            formated=False, content_type__contains='image/')
    watermark = getattr(settings, 'MEDIAUTILS_WATERMARK', None)
    watermark_finger = getattr(settings, 'MEDIAUTILS_WATERMARK_FINGER', False)
    if watermark:
        for post in lista_post:
            #print(post.id)
            if watermark_finger:
                water_text = ' '.join([watermark, post.md5_hash[0:8]])
            else:
                water_text = watermark
            watermarks(post.media_file.path, water_text)
            watermarks(post.media_thumbnail.path, water_text)

