# -------------------------------------------------------------------------
#  Optimized process
#
#  Optimized process is a way to work with the huge amount of that provided
#  by Cartasur
#
#  Before we were working with Pandas, but pandas requires a lot of memory
#  For that reason we have to move into Dask
#
# -------------------------------------------------------------------------

import dask.dataframe as dd

#  LOADING DATASETS
# -------------------------------------------------------------------------
print("+ Loading files")
clientes = dd.read_csv("clientes.csv", sep="|", encoding="iso-8859-1")
creditos = dd.read_csv("creditos.csv", sep="|", encoding="iso-8859-1")
cuotas = dd.read_csv("cuotas.csv", sep="|")
pagos = dd.read_csv("pagos.csv", sep="|")


#  MERGE DATASETS
# -------------------------------------------------------------------------
print("+ Merging files")
df = dd.merge(clientes, creditos, left_on="ID_CLIENTE", right_on="ID_CLIENTE")
df = dd.merge(df, cuotas, left_on="ID_CREDITO", right_on="ID_CREDITO")
df = dd.merge(df, pagos, how="left", left_on=["ID_CREDITO", "NRO_CUOTA"], right_on=["ID_CREDITO","NRO_CUOTA"])

#  SAVE FILE
# -------------------------------------------------------------------------
print("+ Saving to joined.csv")
dd.to_csv(df, 'joined.csv')
