import datetime
import pandas as pd

class Utils:
    @classmethod
    def create_values(self, value, tp):
        """
        Foi criado essa funcao devido a estrutura do nosso hub, em alguns casos temos que passar da seguinte forma:
        {'field': {'String': 'value', 'Valid': True}}
        Essa funcao cria o par de chaves e atribui seus tipos para ser atribuido no body de maneira correta.
        """
        pairKey = dict()  
        if tp == 'String':
            pairKey[tp] = str(value) if value != '' and value != None else ''
        elif tp == 'Int32':
            pairKey[tp] = int(value) if value != '' and value != None else 0
        elif tp == 'Int64':
            pairKey[tp] = int(value) if value != '' and value != None else 0
        elif tp == 'Float64':
            pairKey[tp] = float(value) if value != '' and value != None else 0  
        elif tp == 'Boolean':
            pairKey[tp] = bool(value) if value != '' and value != None else False
        pairKey['Valid'] = True if value != '' and value != None else False  
        return pairKey
    
    @classmethod
    def normalize_datetime(self, date):
        new_dt = date
        if new_dt and new_dt != '':
            if len(new_dt) > 25:
                # Eg: 2020-10-14T14:24:57.789000   
                new_dt = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f')
                new_dt = new_dt.strftime('%d/%m/%Y %H:%M:%S')
            elif len(new_dt) == 25:
                # 2015-01-09T22:00:00-02:00
                new_dt = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z')
                new_dt = new_dt.strftime('%d/%m/%Y %H:%M:%S')
            elif len(new_dt) == 10:
                # 1995-01-01
                try:
                    new_dt = datetime.datetime.strptime(date, '%Y-%m-%d')
                    new_dt = new_dt.strftime('%d/%m/%Y')
                except:
                    new_dt = datetime.datetime.strptime(date, '%d-%m-%Y')
                    new_dt = new_dt.strftime('%d/%m/%Y')
            elif len(new_dt) == 19:
                print(new_dt)
                new_dt = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
                new_dt = new_dt.strftime('%d/%m/%Y %H:%M:%S')
        return new_dt

    @classmethod
    def aggregate_to_new_collumn(self,target_file, by, target, separator, columns, convert_columns=None, header=None, error_bad_lines=True, encoding='latin-1') -> list:
        csv_data = pd.read_csv(
            target_file,
            sep=separator,
            encoding=encoding,
            names=columns,
            index_col=False,
            header=header,
            error_bad_lines=error_bad_lines,
        )
        df = pd.DataFrame(columns=columns, data = csv_data)
        
        if convert_columns:
            for column in convert_columns:
                df[column] = df[column].apply(lambda x: x.strip() if isinstance(x, str) else x).replace('', 0).replace('None', 0)
                try:
                    df = df.replace(',','.', regex=True).astype({column: float})
                except:
                    df = df.astype({column: float})
        
        df_ag = df.groupby(by=[by])[target].sum()

        df_f = pd.merge(df,df_ag, left_on=by, right_index=True)
        
        return df_f.values.tolist()