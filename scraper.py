import scraperwiki
import requests
import lxml.html

def scrape_ads(): 
    ads = [] 
    for i in range(1,10):
        print '%s Ads scrapes, Scraping Page %s' % (len(ads), i)
        r = requests.get('https://www.airbnb.co.uk/s/singapore?page=%s' % i, verify=False)
        if r.status_code==200:
            dom = lxml.html.fromstring(r.text)

    
            targetList = dom.cssselect('li.listing-outer')
            if len(targetList):
                # Great! This page contains ads to scrape.

                for listing in targetList:
                    ad = {
                        'name': get_element_or_none(listing, 'a.listing-name').replace(',',''),
                        'url': get_element_or_none(listing, 'a.listing-name', 'href')#,
                        #'reviewCount': get_element_or_none(results, '.reviews-bubble')
                    }
                    print ad['name']
                    #print 'https://www.airbnb.co.uk'+ad['url']
                    r2 = requests.get('https://www.airbnb.co.uk'+ad['url'], verify=False)
                    dom2 = lxml.html.fromstring(r2.text)
                    ad['price per night'] = get_element_or_none(dom2, '#price_amount')
                    ad['adress'] = get_element_or_none(dom2, 'span#display-address').replace(',','')
                    ad['user'] = get_element_or_none(dom2, '#user a')
                    ad['user profile'] = get_element_or_none(dom2, '#user a', 'href')
                    ad['image'] = get_element_or_none(dom2, '.media-photo img', 'src')
                    if len(dom2.cssselect('.star-rating')):
                        ad['rating'] = dom2.cssselect('.star-rating meta[itemprop="ratingValue"]')[0].get('content')
                    else:
                        ad['rating'] = ''
                    ads.append(ad)
                scraperwiki.sqlite.save(['url'], ads)
            else:
                break

# A handy function to get text or attributes out of HTML elements
def get_element_or_none(context, css, attribute=None):
    try:
        element = context.cssselect(css)[0]
    except:
        return None
    else:
        if attribute:
            return element.get(attribute)
        else:
            return element.text_content().strip()

def get_overall_star(context):
    for i in range (0,11):
        if context.cssselect('#guest_satisfaction .star_%s' % i):
            return str(i)
        else:
            continue

def get_specific_star(context):
    for i in range (0,11):
        if context.cssselect('.hosting-star-rating .star_%s' % i):
            return str(i)
        else:
            continue



scrape_ads()