import pandas as pd

from config import Config
from etl import Etl

config = Config()
etl = Etl(config.DB_URI)

dfs = {}

for source in config.SOURCES:
    ### Extraction
    etl.download_category_data(source['category'], source['link'])
    ### Transformation
    dfs[source['category']] = etl.transform_source_data(source['category'])

df_main = pd.concat(dfs, join='inner', ignore_index=True)
df_cinemas = dfs['salas_de_cine']

report_main, report_cinemas = etl.build_sumarized_reports(df_main, df_cinemas)

### Load
etl.insert_df_into_table(df_main.drop(columns=['fuente']), 'main')
etl.insert_df_into_table(report_main, 'main_info')
etl.insert_df_into_table(report_cinemas, 'cinemas_info')