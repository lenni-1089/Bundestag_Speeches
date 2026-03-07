# For data validation we can make use of pandera, which lets us define schema's
# as objects (dict like) or classes.
# Data validation can mainly be used in two occasions, inline and to validate function in- and outputs.
# Inline can be thought of as single validation at a specific point in time or step of the process,
# for example at important checkpoints in a processing pipeline.
# The other case proves useful when a function requires inputs in a specific structure
# to work, similar to type hints, we can pass inputs through a pandera schema validation and ensure the function
# is only run when the input adheres to the required structure and properties or is transformed until it does before
# being passed as input. The same goes for function outputs, they also can be validated before being returned.

# In our case we want a checkpoint validation, as our goal is to validate our extracted speeches dataframe of a session
# before saving it as a file. Thus we refer to an inline validation. As noted earlier: we can define this schema
# as an object (dict like) or a class, classes are preferred when objects are passed between multiple system components
# but generally both ways of defining schemas are equivalent. We will make use of the object definition
# as this extends most naturally to how we worked so far (with objects like dicts and not classes).

# Before defining a schema it makes sense to remind ourselves of what a schema is. A schema defines
# the structure and properties of a tablelike object, like a dataframe. A table consists of columns and rows. Columns
# define constraints on the data they can hold, mainly the type of data (bool, string, int, float, object etc.)
# and can hold additional rules like if values can be empty/nullable, if values need to be unique,
# if values need to be of a certain category, are expected to fall in a certain range and so forth.
# Those constraints basically enforce/encode the assumptions/logic about the data properties we expect.

# In terms of defining an object based pandera schema, we define an DataframeSchema object that takes a dictionary as input.
# This dict lets us define which columns to expect, as keys, and which constraints to check values of that columns against,
# as values.
import pandera.pandas as pa
from typing import Dict, List

bronze_schema = pa.DataFrameSchema(
    {
        'issn_id': pa.Column(str, nullable=False) , # document identifier string,
                                                    # not null (not unique as all speeches of same session)
        'legaslative_period': pa.Column("int32",nullable= False, checks=pa.Check.ge(20)), # not null serves as an ordinal attribute,
                                                                                       # not an identifier only thats why int, we only fetch data from legalstive period 20 onwards
        'session_nr': pa.Column("int32",nullable=False, checks=pa.Check.gt(0)),  # same as legaslative period, but greater than 0
        'session_date': pa.Column(object, nullable=False),
        'session_start_time': pa.Column(str, nullable=True),
        'session_end_time': pa.Column(str, nullable=True),
        'next_session_date': pa.Column(str, nullable=True),
        'agenda_name': pa.Column(str, nullable=False),
        'agenda_title': pa.Column(str, nullable=True),
        'agenda_subtitle': pa.Column(str, nullable=True),
        'agenda_docs':pa.Column(List[str], nullable=True), ## OBJECT CHECK list of strings
        'speaker_id': pa.Column(str, nullable=False),
        'name': pa.Column(str, nullable=False, checks=pa.Check.str_length(min_value=2)),
        'lastname': pa.Column(str, nullable=False, checks=pa.Check.str_length(min_value=2)),
        'role':pa.Column(str, nullable=True),
        'party_affiliation':pa.Column(str, nullable=True, checks=pa.Check.str_length(min_value=2)),
        'speech_id':pa.Column(str, nullable=False),
        'speech': pa.Column(str, nullable=False, checks=pa.Check.str_length(min_value=10)),
        'comments': pa.Column(List[Dict], nullable=False), ### OBJECT CHECK list of dicts
        },
    strict=True,
    coerce=True,
)



from pyspark.sql.types import (
    StructType, StructField, StringType, IntegerType,
    DateType, TimestampType, ArrayType
)

silver_staging_spark_schema = StructType([
            # session level
            StructField("issn_id", StringType(), False),
            StructField("legaslative_period", IntegerType(), False),
            StructField("session_nr", IntegerType(), False),
            StructField("session_date", DateType(), False),
            StructField("session_start_time", StringType(), True),
            StructField("session_end_time", StringType(), True),
            StructField("next_session_date", StringType(), True),
            # agenda level
            StructField("agenda_name", StringType(), False),
            StructField("agenda_title", StringType(), True),
            StructField("agenda_subtitle", StringType(), True),
            StructField("agenda_docs", ArrayType(StringType()), False),
            # speaker level
            StructField("speaker_id", StringType(), False),
            StructField("name", StringType(), False),
            StructField("lastname", StringType(), False),
            StructField("role", StringType(), True),
            StructField("party_affiliation", StringType(), True),
            # speech level
            StructField("speech_id", StringType(), False),
            StructField("speech", StringType(), False),
            StructField("comments", ArrayType(
                StructType([
                    StructField("index_position", IntegerType(), True),
                    StructField("comment_text", StringType(), True),
                ])
            ), False),
            StructField("source_path", StringType(), False)
])



