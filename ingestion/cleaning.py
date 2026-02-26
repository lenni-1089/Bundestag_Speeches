import pandas as pd
import pandera as pa
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

    raw_df = dataframe
    # apply text cleaning with map(), to all string columns
    string_columns = ['agenda_name',
                      'agenda_title',
                      'agenda_subtitle',
                      'name', 'lastname',
                      'role',
                      'party_affiliation',
                      'speech']

    df_text_cleaned = raw_df.copy()
    df_text_cleaned[string_columns] = df_text_cleaned[string_columns].map(clean_text, na_action="ignore")
    df_text_comments_cleaned = df_text_cleaned.copy()
    df_text_comments_cleaned["comments"] = df_text_cleaned["comments"].map(clean_comments, na_action="ignore")

    # manually convert dtypes, mainly ints and datetime
    df_text_clean_dtypes_adjusted = df_text_comments_cleaned.copy()

    df_text_clean_dtypes_adjusted["session_date"] = pd.to_datetime(df_text_clean_dtypes_adjusted["session_date"], format= "%d.%m.%Y")
    df_text_clean_dtypes_adjusted["speaker_id"] = df_text_clean_dtypes_adjusted["speaker_id"].astype(str)
    df_text_clean_dtypes_adjusted["legaslative_period"] = df_text_clean_dtypes_adjusted["legaslative_period"].astype(int)
    df_text_clean_dtypes_adjusted["session_nr"] = df_text_clean_dtypes_adjusted["session_nr"].astype(int)


    return df_text_clean_dtypes_adjusted