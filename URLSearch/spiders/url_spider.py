import scrapy
import tldextract

from URLs.URLs import URLs


class URLSearchSpider(scrapy.Spider):
    name = "url_spider"

    def start_requests(self):
        urls = URLs
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def is_interesting(self, link, link_text, footer_links,domain):

        if link_text != None:
            link_text = link_text.lower()

        # Keywords to search for in the URL's text and URL
        keywords = ['sustainability', 'report']

        if link is None or link in footer_links:
            return False
        
        #Checking if domain is subdomain of main parent
        if domain not in link:
            return False
            
        # Checking only for .pdf files. Can be modified for any other inputs
        elif link.endswith('.pdf'):
            for k in keywords:
                if k in link_text or k in link:
                    return True
        elif link_text is None:
            return False
        else:
            return False

    def remove_duplicates(self, to_save):
        return [dict(t) for t in {tuple(d.items()) for d in to_save}]

    def is_blacklisted(self, domain):
        # Blacklisted URLs that generally increase the time for execution
        blacklisted = ['google', 'facebook', 'instagram', 'twitter',
                       'youtube', 'linkedin', 'pinterest', 'reddit', 'tumblr',
                       'wikipedia', 'amazon', 'flickr', 'imdb', 'apple', 'bing',
                       'yahoo','msn','meta','medium','iso']
        return domain in blacklisted

    def is_relative(self, link):
        if link is None:
            return False
        if link.startswith('/'):
            return True
        return False

    def parse(self, response):
        try:
            anchors = response.css('a')
        except:
            anchors = []
        try:
            footer_links = response.css('footer a::attr(href)').getall()
        except:
            footer_links = []
        full_footer_links = []
        for link in footer_links:
            if self.is_relative(link):
                full_footer_links.append(response.urljoin(link))
            else:
                full_footer_links.append(link)
        to_follow = []
        to_save = []
        domain = tldextract.extract(response.request.url).domain
        if self.is_blacklisted(domain):
            return None
        for a in anchors:
            link = a.css('::attr(href)').get()
            link_text = a.css('::text').get()
            if self.is_relative(link):
                link = response.urljoin(link)

            if self.is_interesting(link, link_text, full_footer_links,domain):
                to_save.append({
                    'link': link,
                    'link_text': link_text,
                    'source': response.request.url,
                })
            elif link is not None and 'mailto' not in link and tldextract.extract(link).domain == domain and not self.is_blacklisted(tldextract.extract(link).domain):
                to_follow.append(link)

        for i in self.remove_duplicates(to_save):
            yield i
        for i in to_follow:
            yield response.follow(i, callback=self.parse)

        self.log(f'Done')
