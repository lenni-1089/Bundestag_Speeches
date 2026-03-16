import requests
from bs4 import BeautifulSoup



BASE_URL = "https://www.bundestag.de/ajax/filterlist/de/services/opendata/1058442-1058442"

def discover_xml_urls(base_url:str) -> list[str]:

    # Task initiation
    # define initial offset (equal to page)
    offset = 0

    # configure initual paramter settings, only offset will be adjusted
    # for pagination
    params = { 'noFilterSet': 'true',
                    'offset': offset}
    
    # construct list to hold all urls
    all_urls = []

    # send paginated requests until no documents are returned 
    while True:
        print(f"Request: offset {offset}")

        # send request
        response = requests.get(base_url, params= params)
        # check for request success
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')


        # fetch metadata upon the first request
        if offset == 0:
        
            meta_info_attributs = soup.find("div", class_="meta-slider")

            nr_docs = meta_info_attributs.get("data-hits", None)
            next_offset = meta_info_attributs.get("data-nextoffset", None)

            if not nr_docs:
                print("No documents found in requests")
                # "return" or raising error when defined in function   


            print(f"{nr_docs} document urls found!")
            nr_docs = int(nr_docs)
    

        # get all doc urls for request
        page_url_elements = soup.find_all("a", class_="bt-link-dokument")

        if len(page_url_elements) == 0:
            print("No docs found, ending requests.")
            break
        
        # for each found doc element, check presence of href/link and if present add to list
        page_urls =[element.get("href") for element in page_url_elements if not element.get("href", None) == None]
        # add urls to global list
        all_urls.extend(page_urls)
        print(f"Nr. of urls found and added: {len(page_urls)}")
        

        # update offset parameter for next request
        offset += 10 
        params["offset"] = offset


    nr_documents_found = len(all_urls)

    print(f"A total nr. of {nr_documents_found} were found and extracted!")

    if nr_documents_found == nr_docs:
        print("We've found all documents!")
    else:
        print(f"We found {nr_documents_found} documents when we should've found {nr_docs}, please investigate")
        
    return all_urls
    





