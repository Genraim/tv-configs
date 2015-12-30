import urllib.request
import xml.dom.minidom

try:
    playlistvlc = urllib.request.urlopen("http://weburg.tv/playlist.vlc")
except IOError:
    print("URL error")
    input("Press key")
    exit()

vlcparse = xml.dom.minidom.parse(playlistvlc)
tracklist = vlcparse.getElementsByTagName("track")
grouplist = vlcparse.getElementsByTagName("vlc:item")
playlistm3u = open("../configs/playlist.m3u", "w")


def get_info_track(track_not_parsed, tag):
    return track_not_parsed.getElementsByTagName(tag)[0].childNodes[0].nodeValue


def get_track_id(elem):
    return int(get_info_track(elem, "vlc:id"))


def get_track_group(id):
    return grouplist[id-1].parentNode.getAttribute("title")


def convert_to_m3u(elem):
    try:
        message = "#EXTINF:0 group-title=\"" + get_track_group(get_track_id(elem)) + "\" tvg-logo=\"" + \
              get_info_track(elem, "image") + r'" aspect-ratio="16:9", ' + get_info_track(elem, "title") + "\n" + \
              get_info_track(elem, "location") + "\n"
    except IndexError:
        message = "#EXTINF:0 group-title=\"" + get_track_group(get_track_id(elem)) + "\", " + \
                  get_info_track(elem, "title") + "\n" + get_info_track(elem, "location") + "\n"
    return message


playlistm3u.write("#EXTM3U \n")
for item in tracklist:
    playlistm3u.write(convert_to_m3u(item))

playlistm3u.close()
