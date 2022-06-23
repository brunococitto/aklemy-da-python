import os
import locale
import requests
import pandas as pd
import numpy as np
from logger import log
from datetime import datetime
from unidecode import unidecode
from sqlalchemy import create_engine

from utils import to_snake_case, get_date_from_name

# Set locale to get month names in correct language
locale.setlocale(locale.LC_ALL, 'es_ES.utf-8')

class Etl:
    """"""

    def __init__(self, DB_URI=""):
        self.DB_URI = DB_URI

    def download_category_data(self, category:str, link:str):
        """
            Determine filename and create folders if not already exist
            Download data from provided link using request
            Dump downloaded data into previously determined filename

            args:
                - category: string containing category name
                - link: string containing data source link
        """
        # Build filename using current date and category
        folder = datetime.now().strftime('%Y-%B')
        file = f"{category}-{datetime.now().strftime('%d-%m-%Y')}"
        path = f"data/{category}/{folder}/{file}.csv"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        try:
            with open(path, 'wb+') as file:
                log.info(f"Downloading {category} data from {link}")
                
                req = requests.get(link, stream=True)
                
                log.info(f"Successfuly downloaded {category} data, now dumping it into {path}")
                
                for chunk in req.iter_content(chunk_size=128):
                    file.write(chunk)
                file.close()
                
                log.info(f"Successfuly dumped downloaded data for {category}")
        except Exception as e:
            log.error(f"Error downloading {category} data from {link}: {e}")

    def insert_df_into_table(self, df: pd.DataFrame, table: str):
        """
            Create connection with database, empty table and then insert dataframe

            args:
                - df: dataframe object to insert into db
                - table: string containing table name
        """
        try:
            log.info(f"Inserting dataframe into table {table}")
            
            engine = create_engine(self.DB_URI)
            engine.connect()
            engine.execute(f"TRUNCATE TABLE {table}")
            engine.dispose()
            df.to_sql(table, engine, if_exists='append', index_label='id', method='multi', chunksize=50)
            
            log.info(f"Successfuly inserted dataframe into table {table}")
        except Exception as e:
            log.error(f"Error inserting DF into table {table}: {e}")

    def transform_source_data(self, category:str):
        """
            Find latest available data for provided datasource category and load into a Pandas DataFrame
            Sanitize columns names from camelCase to snake_case for matching requeriments
            Drop unused columns
            Fix typos, normalize information and set data types in downloaded data
            Returns sanitized dataframe

            args:
                - category: string containing category
            
            retruns:
                - source_df: pandas dataframe containing datasource category sanitized data
        """
        # Find latest available data and load into a DF
        try:
            log.info(f"Loading {category} data")
            months = {x:datetime.strptime(x, '%Y-%B') for x in os.listdir(f"data/{category}")}
            files = {x:get_date_from_name(x) for x in os.listdir(f"data/{category}/{max(months)}")}
            source_df = pd.read_csv(f"data/{category}/{max(months)}/{max(files)}")
            
            log.info(f"Successfuly loaded {category} data")
        except Exception as e:
            log.error(f"Error loading {category} data: {e}")
            raise Exception(e)

        try:
            # Sanitize and rename columns headers to match requeriments
            columns_sanitized = {x:to_snake_case(unidecode(x)) for x in source_df.columns}
            source_df.rename(columns=columns_sanitized, inplace=True)
            columns_map = {'cod_loc':'cod_localidad', 'direccion':'domicilio', 'cp': 'codigo_postal'}
            source_df.rename(columns=columns_map, inplace=True)

            # Fix typos, normalize information and set data types in downloaded data
            provincias_map = {'Neuquén\xa0': 'Neuquén', 'Tierra del Fuego':'Tierra del Fuego, Antártida e Islas del Atlántico Sur', 'Santa Fé': 'Santa Fe'}
            fuentes_map = {'Gob. Pcia.': 'Gobierno de la Provincia', 'Gobierno de la provincia': 'Gobierno de la Provincia', 'RCC- Córdoba':'RCC', 'SInCA':'INCAA / SInCA'}
            source_df.replace({'provincia':provincias_map, 'fuente': fuentes_map}, inplace=True)

            if category == 'salas_de_cine':
                source_df['butacas'] = pd.to_numeric(source_df['butacas'], errors='coerce').fillna(0)
                source_df['pantallas'] = pd.to_numeric(source_df['pantallas'], errors='coerce').fillna(0)
                source_df['espacio_incaa'] = pd.to_numeric(source_df['espacio_incaa'].replace({'si':1,'SI':1}), errors='coerce').fillna(0).astype(int)

            # Drop unused columns
            columns = ['cod_localidad', 'id_provincia', 'id_departamento', 'categoria', 'provincia', 'localidad', 'nombre', 'domicilio', 'codigo_postal', 'telefono', 'mail', 'web', 'fuente']
            if category == 'salas_de_cine':
                columns = columns + ['butacas', 'pantallas', 'espacio_incaa']
            columns_to_drop = [c for c in source_df.columns if c not in columns]
            source_df.drop(columns=columns_to_drop, inplace=True)

            # Replace nans for None to match SQL nulls
            source_df.replace({np.nan: None}, inplace=True)
            
            log.info(f"Successfuly sanitized {category} data")
        except Exception as e:
            log.error(f"Error sanitizing {category} data: {e}")
            raise Exception(e)
        
        return source_df

    def build_sumarized_reports(self, df_main: pd.DataFrame, df_cinemas: pd.DataFrame):
        """
            Build summarized reports and returns generated dataframes with load date column

            args
                - df_main: pandas dataframe containing main information (pseudo fact table)
                - df_cinemas: pandas dataframe containing cinemas information
            
            returns
                - report_main: pandas dataframe with main reports
                - report_cinemas: pandas dataframe with cinemas report
        """
        try:
            log.info('Creating reports with summarized information')

            if type(df_main)==None or type(df_cinemas)==None:
                raise Exception('DataFrame not provided')

            # Build summarized reports for each requeriment using groupby and agg
            report_category = df_main.groupby(by=['categoria'], as_index=False).agg({'nombre':'count'}).rename(columns={'nombre':'cantidad'})
            report_source = df_main.groupby(by=['fuente'], as_index=False).agg({'nombre':'count'}).rename(columns={'nombre':'cantidad'})
            report_province_category = df_main.groupby(by=['provincia','categoria'], as_index=False).agg({'nombre':'count'}).rename(columns={'nombre':'cantidad'})
            report_cinemas = df_cinemas.groupby(by=['provincia'], as_index=False).agg({'pantallas':'sum', 'butacas':'sum', 'espacio_incaa':'sum'}).rename(columns={'pantallas':'cantidad_pantallas', 'butacas':'cantidad_butacas', 'espacio_incaa':'cantidad_espacios_incaa'})

            # Merge DFs and add load date column
            report_main = pd.concat([report_category, report_source, report_province_category], ignore_index=True)
            report_main.replace({np.nan: None}, inplace=True)
            report_main['fecha_carga'] = pd.to_datetime('today').strftime("%Y-%m-%d")
            report_cinemas['fecha_carga'] = pd.to_datetime('today').strftime("%Y-%m-%d")
            
            log.info('Successfuly created reports')
        except Exception as e:
            log.error(f"Error creating reports: {e}")
            raise Exception(e)

        return report_main, report_cinemas

if __name__ == "__main__":
    etl = Etl();