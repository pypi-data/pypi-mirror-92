import os
import time
import re
import requests


class VimeoScraper:
    '''
    Scraping Vimeo videos
    Args:
        out_path:  [Optional] str, Path to output directory. If unspecified, current directory will be used
    '''
    def __init__(self, out_path=None):
        if out_path is not None:
            assert os.path.isdir(out_path), "Invalid output directory"
        self.out_path = out_path

    def scrape(self, url, quality, proxies=None):
        '''
        Scraper function for Vimeo
        Args:
            url: URL of vimeo video to be scraped
            quality: Output video resolution
            proxies: dict, A dictionary containing proxy information
        '''
        video_id = url.split('/')[-1]
        quality = quality
        try:
            page = requests.get(f'https://player.vimeo.com/video/{video_id}/config?default_to_hd=1', proxies=proxies)
        except Exception:
            raise ValueError("Invalid video URL")

        json_contents = page.json()
        title = json_contents['video']['title']
        file_dicts = json_contents['request']['files']['progressive']
        available_res = [d['quality'] for d in file_dicts]
        if quality in available_res:
            for d in file_dicts:
                if d['quality'] == quality:
                    print('-' * 75)
                    print("Starting download")
                    start_time = time.time()
                    title = re.sub(r'''[\W_]+''', '', title)
                    with open(
                            f"{self.out_path}/{title}-{quality}.mp4" if self.out_path else f"{title}-{quality}.mp4",
                            'wb+') as f:
                        video_stuff = requests.get(d['url']).content
                        f.write(video_stuff)
                        print(f"Download completed in {time.time() - start_time}s")
                        print('-' * 75)
        else:
            raise ValueError(
                f"{quality} is not available for this video. {','.join(available_res)} resolutions are available")
