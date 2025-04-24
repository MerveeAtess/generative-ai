# Video- Ses İşlemlerinin Yapıldığı Aşama

import scrapetube
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders import YoutubeAudioLoader
from langchain_community.document_loaders.parsers import OpenAIWhisperParser
import os
from dotenv import load_dotenv
from youtubevideo import YoutubeVideo #sınıfı alma


load_dotenv()

my_key_openai = os.getenv("openai_apikey")

#1 Transkripsiyon - videoyu metne çevirme url adresi ile
def get_video_transcript(url):

    target_dir = "./audios/"
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    loader = GenericLoader(
        YoutubeAudioLoader(urls=[url], save_dir=target_dir),
        OpenAIWhisperParser(api_key=my_key_openai)
    )

    video_transcript_docs = loader.load()
    return video_transcript_docs

# 2 Youtube Araması- url yerine arama yapmak 
# girilen anahtar kelimelere göre videoları getirir

def get_videos_for_search_term(search_term, video_count=1, sorting_criteria="relevance"):
    convert_sorting_option = {
                                "En İlgili": "relevance",
                                "Tarihe Göre": "upload_date",
                                "İzlenme Sayısı":"view_count", 
                                "Beğeni Sayısı":"rating"
                            }

    videos = scrapetube.get_search(query=search_term, limit=video_count, sort_by=convert_sorting_option[sorting_criteria])
    videolist = list(videos)

    youtube_videos = []

    for video in videolist:
        new_video = YoutubeVideo(
            video_id = video["videoId"], #hangi söz dizimine göre
            video_title=video["title"]["runs"][0]["text"],#başlığa göre belirtme
            video_url = "https://www.youtube.com/watch?v=" + video["videoId"],#web adresini belirtmek için
            channel_name= video["longBylineText"]["runs"][0]["text"],
            duration= video["lengthText"]["accessibility"]["accessibilityData"]["label"],
            publish_date = video["publishedTimeText"]["simpleText"] #yayın tarihi
        )
        youtube_videos.append(new_video)

    return youtube_videos

