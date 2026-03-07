import pandas as pd
from pandas import DataFrame
import re


def clean_text(text: str) -> str:

    text = text.replace("\xa0", " ")
    text = text.replace("\u202f", " ")
    text = text.replace("\u2001", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def clean_comments(comments_list: list)-> list:
    # each comment is a list of dictionaries
    # containing the index position of a comments as the key
    # the comment itself as the value
    if not isinstance(comments_list, list):
        return comments_list

    for comment_dict in comments_list:

        if not isinstance(comment_dict,dict):
            return comment_dict
        comment_text = comment_dict["comment_text"]
        cleaned_comment_text = clean_text(comment_text)
        comment_dict["comment_text"] = cleaned_comment_text
    return comments_list


def cleaning_raw_speeches(dataframe: pd.DataFrame) -> pd.DataFrame:

    df = dataframe.copy()
    # defining all string columns for text cleaning
    string_columns = ['agenda_name',
                      'agenda_title',
                      'agenda_subtitle',
                      'name', 'lastname',
                      'role',
                      'party_affiliation',
                      'speech']

    # apply text cleaning to all string columns
    df[string_columns] = df[string_columns].map(clean_text, na_action="ignore")
    # apply text cleaning to comments, as they are nested in dictionaries
    # requires dedicated function for access
    df["comments"] = df["comments"].map(clean_comments, na_action="ignore")

    # type casting
    # cast session dates from string to dates
    df["session_date"] = pd.to_datetime(df["session_date"], format= "%d.%m.%Y").dt.date
    # ensuring speaker ids are strings not ints
    df["speaker_id"] = df["speaker_id"].astype(str)
    # casting legislative period and session nr to int
    df["legaslative_period"] = df["legaslative_period"].astype("int32")
    df["session_nr"] = df["session_nr"].astype("int32")

    return df