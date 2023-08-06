import os
import re
import shutil
import sys
import time
import random

import youtube_dl
from internetarchive import get_item, upload
from TikTokApi import TikTokApi
from argparse import ArgumentParser


api = TikTokApi()


def getVersion():
    return '2021.01.20'

def parse_args():
    parser = ArgumentParser(description="An auto downloader and uploader for TikTok videos.")
    parser.add_argument("user")
    parser.add_argument(
        "--no-delete", action="store_false", help="don't delete files when done"
    )
    parser.add_argument(
        "--hashtag", action="store_true", help="download hashtag instead of username"
    )
    parser.add_argument(
        "--limit", help="set limit on amount of TikToks to download"
    )
    parser.add_argument(
        "--use-download-archive",
        action="store_true",
        help=(
            "record the video url to the download archive. "
            "This will download only videos not listed in the archive file. "
            "Record the IDs of all downloaded videos in it."
        ),
    )
    parser.add_argument(
        "--id", action="store_true", help="download this video ID"
    )
    parser.add_argument(
        "--liked", action="store_true", help="download the user's liked posts"
    )
    args = parser.parse_args()
    return args



def getUsernameVideos(username, limit):
    if limit is not None:
        count = int(limit)
    else:
        count = 9999
    tiktoks = api.byUsername(username, count=count)
    return tiktoks


def getHashtagVideos(hashtag, limit):
    if limit is not None:
        count = int(limit)
    else:
        count = 9999
    tiktoks = api.byHashtag(hashtag, count=count)
    return tiktoks


def getLikedVideos(username, limit):
    if limit is not None:
        count = int(limit)
    else:
        count = 999999
    tiktoks = api.userLikedbyUsername(username, count=count)
    return tiktoks


def downloadTikTok(username, tiktok, cwd, varTry, did):
    try:
        tiktokID = tiktok['id']
    except:
        try:
            tiktokID = tiktok['itemInfos']['id']
        except:
            tiktokID = tiktok['itemInfo']['itemStruct']['id']
    ydl_opts = {
        'writeinfojson': False,
        'writedescription': False,
        'write_all_thumbnails': False,
        'writeannotations': False,
        'allsubtitles': False,
        'ignoreerrors': True,
        'fixup': True,
        'quiet': True,
        'no_warnings': True,
        'restrictfilenames': True,
        'outtmpl': tiktokID + '.mp4',
    }

    os.chdir('E:/tiktok')

    if varTry % 3 != 0:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            # ydl.download([tiktok['itemInfo']['itemStruct']['video']['downloadAddr']])
            ydl.download(['https://www.tiktok.com/@' +
                          username + '/video/' + tiktokID])
    else:
        mp4 = open(tiktokID + '.mp4', "wb")
        mp4.write(api.get_Video_By_DownloadURL(
            tiktok['itemInfo']['itemStruct']['video']['downloadAddr'], custom_did=did))
        mp4.close()
        # shutil.rmtree('tmp')
    try:
        mp4 = open(tiktokID + '.mp4', "r", encoding="latin-1")
        # For some reason, ytdl sometimes downloads the HTML page instead of the video
        # this removes the HTML
        check = str(mp4.read())[:15]
        if (check == '<!DOCTYPE html>') or (check[:6] == '<HTML>'):
            mp4.close()
            os.remove(tiktokID + '.mp4')
        else:
            mp4.close()
    except FileNotFoundError:
        pass
    x = os.listdir()
    # for i in x:
    #    if i.endswith('.unknown_video'):
    #        base = os.path.splitext(i)[0]
    #        if os.path.exists(base + '.mp4'):
    #            os.remove(base + '.mp4')
    #        os.rename(i, base + '.mp4')


def uploadTikTok(username, tiktok, deletionStatus, file):

    if file is not None:
        file.write(str(tiktok))
        file.write('\n')


def downloadTikToks(username, tiktoks, file, downloadType, did):
    cwd = os.getcwd()
    try:
        lines = file.readlines()
        for x in range(0, len(lines)):
            lines[x] = lines[x].replace('\n', '')
    except:
        lines = ''
    ids = []
    for tiktok in tiktoks:
        if str(type(tiktok)) == '<class \'dict\'>':
            try:
                tiktok = tiktok['id']
            except KeyError:
                tiktok = tiktok['itemInfos']['id']
        if True:
            print(tiktok + "")
    return ids


def uploadTikToks(tiktoks, file, delete):
    for tiktok in tiktoks:
        uploadTikTok(getUsername(tiktok), tiktok, delete, file)


def doesIdExist(lines, tiktok):
    return tiktok in lines


def getUsername(tiktokId):
    thing = api.getTikTokById(tiktokId)
    try:
        return thing['itemInfo']['itemStruct']['author']['uniqueId']
    except:
        return None


def getTikTokObject(tiktokId, did):
    thing = api.getTikTokById(tiktokId, custom_did=did)
    return thing


def main():
    os.chdir(os.path.expanduser('E:/tiktok'))

    username = 'ftb68.5'
    delete = 0
    limit = 9999
    archive = True

    downloadType = ''
    if archive:
        try:
            file = open('archive.txt', 'r+')
        except FileNotFoundError:
            f = open('archive.txt', 'x')
            f.close()
            file = open('archive.txt', 'r+')
    else:
        file = None
    did = str(random.randint(10000, 999999999))
    
    downloadType = 'liked'
    tiktoks = getLikedVideos(username, limit)
    uploadTikToks(tiktoks, file, delete)

    try:
        file.close()
    except:
        pass
    print('')


if __name__ == "__main__":
    main()
