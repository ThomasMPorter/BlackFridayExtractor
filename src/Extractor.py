import configparser
import logging
import os
import sys
import urllib.request

import tmpbfextract
import tmpimgur

#----------------------------
# Set to your cfg file
cfg_file = 'src/local.cfg'
#----------------------------

FORMAT = '[%(levelname)s] %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)


logging.info("Reticulating Splines")

config = configparser.ConfigParser()
config.read(cfg_file)
source = config['BFExtract']['source']
destination = config['BFExtract']['destination']
page_start = int(config['BFExtract']['page_start'])
page_end = int(config['BFExtract']['page_end'])

extract = None

if source == 'BFAds':
    logging.info("Go Go Gadget BFAds!")
    type_of_ad = config['BFAds']['type_of_ad']
    store_name = config['BFAds']['store_name']
    extract = tmpbfextract.ExtractBfads(store_name, type_of_ad)
elif source == 'BlackFriday':
    logging.info("Go Go Gadget BlackFriday!")
    type_of_ad = config['BlackFriday']['type_of_ad']
    store_name = config['BlackFriday']['store_name']
    extract = tmpbfextract.ExtractBlackfriday(store_name, type_of_ad)
elif source == 'GottaDEAL':
    logging.info("Go Go Gadget GottaDEAL!")
    store_name = config['GottaDEAL']['store_name']
    extract = tmpbfextract.ExtractGottadeal(store_name)

if not extract:
    logging.info('Select a valid source in your config friend! Good-bye!')
    sys.exit(0)

logging.info("Extracting the images, please wait..")

image_url_list, album_title = extract.get_image_url_list(page_start, page_end)

if not album_title:
    logging.info("Yipes! Couldn't get the album title! Bye-Bye for now!")
    sys.exit(0)

if not image_url_list:
    logging.info(
        'Aww, nothing for %s yet! Try again later my dude!',
        store_name)
    sys.exit(0)

if destination == 'local':

    logging.info("Saving those puppies locally for you!")

    path=source="{}\\{}".format(config['BFExtract']['local_path'], store_name)

    os.mkdir(path)

    page_number=1

    for image_url in image_url_list:
        urllib.request.urlretrieve(
            image_url, "{}\\{}.jpg".format(path, page_number))
        page_number += 1

    logging.info("Donion Rings!")

elif destination == 'imgur':

    logging.info("Let's talk to imgur")

    imgur_url=config['imgur']['url']
    imgur_client_id=config['imgur']['client_id']
    album_id=config['imgur']['album_id']
    album_deletehash=config['imgur']['album_deletehash']

    imgur_connection=tmpimgur.Connection(
        imgur_url,
        imgur_client_id)

    imgur_album = None

    if album_id and album_deletehash:

        logging.info("Using Existing Album")

        try:
            imgur_album = imgur_connection.get_album(album_id)
            imgur_album.set_album_deletehash(album_deletehash)
        except ValueError as ex:
            logging.error(
                'Whoa, issue getting album! id: %s; message: %s',
                album_id,
                ex)
            sys.exit(0)

        imgur_album.set_album_deletehash = album_deletehash

    else:

        logging.info("Making spanking new album")

        imgur_album = imgur_connection.create_album(album_title)
        f = open("{}\\ImgurAlbum.csv".format(config['BFExtract']['local_path']), "a")
        f.write(
            "{},{},{}".format(
                imgur_album.album_id,
                imgur_album.album_deletehash,
                imgur_album.album_title))

    if not imgur_album:
        logging.info('Could not make/get the imgur album bud! Good-Bye!')
        sys.exit(0)

    logging.info("Adding the images")

    for image_url in image_url_list:
        try:
            imgur_album.upload_image(image_url)
        except ValueError as ex:
            logging.error(
                'Whoa, issue uploading! url: %s; deletehash: %s; message: %s',
                image_url,
                imgur_album.album_deletehash,
                ex)
            sys.exit(0)

    logging.info('Done! Url: %s; Deletehash: %s', imgur_album.album_url,
                 imgur_album.album_deletehash)
