import pandas as pd
import os

def save_speeches_to_parquet(validated_dataframe: pd.DataFrame, output_path:str):

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    if os.path.exists(output_path):
        raise FileExistsError(f"File already exists: {output_path}")

    validated_dataframe.to_parquet(output_path,
                                    engine='pyarrow',
                                    compression='snappy',
                                    index=False)
    print(f"Saved to: {output_path}")

    return output_path