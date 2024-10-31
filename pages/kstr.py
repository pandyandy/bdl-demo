import streamlit as st
import pandas as pd 
import os
from keboola_streamlit import KeboolaStreamlit
from kbcstorage.client import Files

class KeboolaStreamlitRaw(KeboolaStreamlit):

    def write_table_raw(self, table_id: str, df: pd.DataFrame, is_incremental: bool = False):
        """
        Load data into an existing table.

        Args:
            table_id (str): The ID of the table to load data into.
            df (pd.DataFrame): The DataFrame containing the data to be loaded.
            is_incremental (bool): Whether to load incrementally (do not truncate the table). Defaults to False.
            endpoint (str): The endpoint for loading data.
        """
        client = self.__client
        csv_path = f'{table_id}.csv.gz'
        try:
            df.to_csv(csv_path, index=False, compression='gzip')
            
            files = Files(self.root_url, self.token)
            file_id = files.upload_file(file_path=csv_path, tags=['file-import'],
                                        do_notify=False, is_public=False)
            
            job = client.tables.load_raw(table_id=table_id, data_file_id=file_id, is_incremental=is_incremental)
            job_id = job['id']
            self.create_event(
                jobId=job_id, 
                message='Streamlit App Write Table', 
                endpoint='/v2/storage/tables/table_id/import-async',
                data=df
            )
        except Exception as e:
            st.error(f'Data upload failed with: {str(e)}')
        finally:
            if os.path.exists(csv_path):
                os.remove(csv_path)
        return job_id