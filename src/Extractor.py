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
extract_type = config['BFExtract']['extract_type']
website = config['BFExtract']['website']
store_name = config['BFExtract']['store_name']
page_start = int(config['BFExtract']['page_start'])
page_end = int(config['BFExtract']['page_end'])

extract = None

if website == 'bfads':
    logging.info("Go Go Gadget bfads.net!")
    type_of_ad = config['BFAds']['type_of_ad']
    extract = tmpbfextract.ExtractBfads(store_name, type_of_ad)
elif website == 'gottadeal':
    logging.info("Go Go Gadget GottaDEAL!")
    extract = tmpbfextract.ExtractGottadeal(store_name)

if not extract:
    logging.info('Select a valid website in your config friend! Good-bye!')
    sys.exit(0)

logging.info("Extracting the images, please wait..")

image_url_list = extract.get_image_url_list(page_start, page_end)

if not image_url_list:
    logging.info('Aww, nothing for {} yet! Try again later my dude!'.format(
        store_name))
    sys.exit(0)

if extract_type == 'local':

    logging.info("Saving those puppies locally for you!")

    path = website = "{}\\{}".format(config['BFExtract']['local_path'], store_name)

    os.mkdir(path)

    page_number = 1

    for image_url in image_url_list:
        urllib.request.urlretrieve(
            image_url, "{}\\{}.jpg".format(path, page_number))
        page_number += 1

    logging.info("Donion Rings!")

elif extract_type == 'imgur':

    logging.info("Let's talk to imgur")

    imgur_url = config['imgur']['url']
    imgur_client_id = config['imgur']['client_id']
    album_title = config['imgur']['album_title']
    album_id = config['ContinueAlbum']['album_id']
    album_deletehash = config['ContinueAlbum']['album_deletehash']

    imgur_connection = tmpimgur.Connection(
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
