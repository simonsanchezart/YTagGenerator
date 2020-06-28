from requests import get
from pyinputplus import inputYesNo
from sys import exit

api_key = open("api.json", "r").read()

youtube_videos = []
def search_videos(term):
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=10&q={term}&relevanceLanguage=en&type=video&key={api_key}"
    r = get(url)
    content = r.json()

    videos = content["items"]
    for video in videos:
        video_id = video["id"]["videoId"]
        youtube_videos.append(video_id)


tags = []
def get_tags():
    for id in youtube_videos:
        url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={id}&key={api_key}"
        r = get(url)
        content = r.json()

        try:
            video_tags = content["items"][0]["snippet"]["tags"]
        except KeyError:
            continue
        for tag in video_tags:
            tags.append(tag)


sorted_tags = []
def sort_tags():
    global sorted_tags
    for i, tag in enumerate(tags):
        tags[i] = tag.lower()
    sorted_tags = sorted(tags, key=tags.count, reverse=True)
    sorted_tags = list(dict.fromkeys(sorted_tags))


final_tags = []
def trim_tags():
    global final_tags
    char_count = 0
    for tag in sorted_tags:
        char_count += len(tag) + 1
        if char_count < 500:
            final_tags.append(tag)
        else:
            break

def write_tags(term):
    with open(f"{term}.txt", "w") as f:
        for tag in final_tags:
            try:
                f.write(f"{tag},")
            except UnicodeEncodeError:
                continue


def main():
    search_term = input("Insert term: ")
    search_videos(search_term)
    get_tags()
    sort_tags()
    trim_tags()
    write_tags(search_term)

    another_search = inputYesNo(prompt="Would you like to search tags again? (y/n)\n")
    if another_search == "yes":
        del youtube_videos[:]
        del tags[:]
        del sorted_tags[:]
        del final_tags[:]
        main()
    else:
        exit()


main()
