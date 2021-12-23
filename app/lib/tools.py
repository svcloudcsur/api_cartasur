# -------------------------------------------------------------------------
#  Las siguientes funciones son "helpers" que creamos con el objetivo de:
#
#   - Parsear datos que venían en formatos no compatibles
#   - Realizar cambios en tipos de datos (SI, NO, NaN) a valores estandarizados
#   - Redondear valores (para poder aplicar técnicas de ML luego)
#   - Categorizar (LabelEncoder) datos para poder utilizar técnicas de ML
#   - Renombrar columnas para poder utilizarlas luego en JOINS de Pandas.
#
# -------------------------------------------------------------------------
from dateutil.parser import parse
from sklearn.preprocessing import LabelEncoder

def parse_float(df, col):
    try:
        df[col] = df[col].fillna(0)
        df[col] = df[col].apply(lambda x: float(str(x).replace(",",".")))
    except: # There are amounts with invalid characters
        df[col] = 0.0

def parse_int(df, col):
    df[col] = df[col].fillna(0)
    df[col] = df[col].apply(lambda x: int(float(str(x).replace(",","."))))

def parse_date(df, col):
    try:
        df[col] = df[col].apply(lambda x: parse(x))
    except:
        df[col] = ''

def drop_column(df, col):
    df.drop(col, axis='columns', inplace=True)

def parse_yes_no(df, col):
    df[col] = df[col].apply(lambda x: 1 if x == 'SI' else 0)

def parse_categories(df, col):
    label_encoder = LabelEncoder()
    new_col = f"{col}_cat"
    df[new_col] = label_encoder.fit_transform(df[col].astype(str))

def round_values(df, col, amount):
    df[col] = df[col].fillna(0)
    df[col] = df[col].apply(lambda x: int(float(str(x).replace(",","."))) - (int(float(str(x).replace(",","."))) % amount) )

def rename_columns(df, df_name):
    for col in df.columns:
        old_name = col
        new_name = "{}_{}".format(df_name, col)
        df.rename(columns={old_name:new_name}, inplace=True)
