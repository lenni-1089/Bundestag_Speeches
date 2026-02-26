import requests
import pandas as pd
import xml.etree.ElementTree as ET
import os
from pprint import pprint




def get_session_info(root)->dict:

    if root.tag =="dbtplenarprotokoll" and root.attrib:
        plenary_session_metadata = root.attrib

    return {
            "issn_id" : plenary_session_metadata["issn"],
            "legaslative_period" : plenary_session_metadata["wahlperiode"],
            "session_nr" : plenary_session_metadata["sitzung-nr"],
            "session_date" : plenary_session_metadata["sitzung-datum"],
            "session_start_time" : plenary_session_metadata["sitzung-start-uhrzeit"],
            "session_end_time" : plenary_session_metadata["sitzung-ende-uhrzeit"],
            "next_session_date" : plenary_session_metadata["sitzung-naechste-datum"],
            }

def get_agenda_info(agenda_item) -> dict:
    agenda_name = agenda_item.get("top-id")
    agenda_titles = [title_element.text.strip() for title_element in agenda_item.findall(".//p[@klasse = 'T_fett']")]

    if len(agenda_titles) > 1:
        agenda_title = " / ".join(agenda_titles)
    elif agenda_titles:
        agenda_title = agenda_titles[0].strip()
    else:
        agenda_title = None

    agenda_subtitles = [subtitle_element.text.strip() for subtitle_element in
                        agenda_item.findall(".//p[@klasse = 'T_NaS']")]
    if len(agenda_subtitles) > 1:
        agenda_subtitle = " ".join(agenda_subtitles)
    elif agenda_subtitles:
        agenda_subtitle = agenda_subtitles[0].strip()
    else:
        agenda_subtitle = None

    agenda_doc_elements = agenda_item.findall(".//p[@klasse = 'T_Drs']/a")

    if agenda_doc_elements:
        agenda_doc_urls = [doc_element.get("href") for doc_element in agenda_doc_elements]
    else:
        agenda_doc_urls = None



    return {
            "agenda_name": agenda_name,
            "agenda_title": agenda_title,
            "agenda_subtitle": agenda_subtitle,
            "agenda_docs": agenda_doc_urls ,
            }

def get_text(element, xpath:str):
    """Safely extract text from an xml element"""
    found = element.find(xpath)

    return found.text.strip() if found is not None and found.text else None

def get_speaker_info(speech_raw) -> dict:
    """
    Expects a speech as an xml element, extracts all speaker attributes and returns them as a dictionary.
    :param speech_raw: xml speech element
    :return: dictionary with extracted speaker attributes
    """
    redner = speech_raw.find(".//redner")
    speaker_id = redner.get("id") if redner is not None else None

    return {
            "speaker_id" : speaker_id,
            "name" : get_text(speech_raw, ".//vorname"),
            "lastname" : get_text(speech_raw,".//nachname"),
            "role" : get_text(speech_raw,".//rolle_lang"),
            "party_affiliation" : get_text(speech_raw,".//fraktion"),
            }

def get_speech_content(speech_raw)-> dict:
    """
    :param speech_raw: xml speech element
    :return: dictionary with whole speech as one string, and comments as a dict with index positions within speeech
    """
    speech_chunks =[]
    comments = []

    speech_id = speech_raw.get("id")

    position = 1
    for idx, element in enumerate(speech_raw):
        # each speech is ended by remarks by the president (either warning
        # speaking time is up and/or announcing the next speaker)
        # this shows itself by a name tag followed by a paragrpah of class "J_1"
        if element.tag == "name":
            continue
        if  element.get("klasse") == "J_1" and idx > 0 and speech_raw[idx -1].tag == "name":
            continue
        elif element.tag == "p" and element.text:
            speech_chunks.append(element.text)
            position += (len(element.text) + 1)
        elif element.tag == "kommentar" and element.text:
            comments.append({"index_position": position,
                                "comment_text": element.text})
    speech_string = " ".join(speech_chunks)

    return {"speech_id": speech_id, "speech": speech_string, "comments": comments}


def session_extraction(xml_filepath:str)-> pd.DataFrame:

    tree = ET.parse(xml_filepath)
    root = tree.getroot()
    session_info = get_session_info(root)
    rows = []

    agenda_root= root.find("sitzungsverlauf")
    agenda_items = [item for item in agenda_root if item.tag != "sitzungsbeginn" and item.tag != "sitzungsende"]

    for item in agenda_items:
        agenda_info = get_agenda_info(item)
        for speech in item.findall("rede"):
            row = {**session_info,
                   **agenda_info,
                   **get_speaker_info(speech),
                   **get_speech_content(speech)}
            rows.append(row)

    columns = [
        # Session level
        "issn_id",
        "legaslative_period",
        "session_nr",
        "session_date",
        "session_start_time",
        "session_end_time",
        "next_session_date",
        # Agenda level
        "agenda_name",
        "agenda_title",
        "agenda_subtitle",
        "agenda_docs",
        # Speaker level
        "speaker_id",
        "name",
        "lastname",
        "role",
        "party_affiliation",
        # Speech level
        "speech_id",
        "speech",
        "comments",
    ]


    session_df = pd.DataFrame(data=rows, columns=columns)

    output_path = f"./csv_files/{session_info["legaslative_period"]}_{session_info["session_nr"]}.csv"


    return session_df



if __name__ == "__main__":
    import sys
    file_path = sys.argv[1]
    session_extraction(filepath= file_path)






