import sys
import time
import pandas as pd
from dateutil.parser import parse
from sklearn.preprocessing import LabelEncoder

from lib.tools import *
from lib.dataframe import *

print("--- CUOTAS")
last_time = time.time()
print("  + Leyendo Archivo")
cuotas = pd.read_csv('cuotas.csv', sep='|') # ID_CREDITO|ID_CUOTA_CREDITO|NRO_CUOTA|FVTO|CAPITAL|INTERES
parse_date(cuotas, 'FVTO')

# Sin pérdida de generalidad para nuestro trabajo, podemos descartar las filas
# que NO tienen fecha de vencimiento
print("  + Removiendo NaN de la columna FVTO")
cuotas.dropna(subset = ["FVTO"], inplace=True)

print("  + Procesando")
round_values(cuotas, 'CAPITAL', 100)
round_values(cuotas, 'INTERES', 100)
#rename_columns(cuotas, 'cuotas')
time_diff = round(time.time() - last_time)
print(" {} segundos\n".format(time_diff))


#-----------------------------------------------------
# pagos
#-----------------------------------------------------
print("--- PAGOS")
last_time = time.time()
print("  + Leyendo Archivo")
pagos = pd.read_csv('pagos.csv', sep='|')
print("  + Procesando")
parse_date(pagos, 'FPAGO')
parse_float(pagos, 'CAPITAL')
parse_float(pagos, 'INTERES')
rename_columns(pagos, 'pagos')
time_diff = round(time.time() - last_time)
print(" {} segundos\n".format(time_diff))


#-----------------------------------------------------
# creditos
#-----------------------------------------------------
print("--- CREDITOS")
last_time = time.time()
print("  + Leyendo Archivo")
creditos = pd.read_csv('creditos.csv', sep='|', encoding='iso-8859-1')

# Remove unnecessary columns
# TDOC are all NaN
# NDOC are all NaN
# PKEY_JOB / PAR_KEY are some ort of uuid
for col in ['TDOC', 'NDOC','PKEY_JOB', 'PAR_KEY']:
    if col in creditos.columns:
        drop_column(creditos, col)

for col in ['FECHAINFORME', 'FLIQUIDACION']:
    if col in creditos.columns:
        parse_date(creditos, col)

parse_float(creditos, 'MONTO')
parse_categories(creditos, 'SUCURSAL')
parse_categories(creditos, 'NOMBRE')
parse_yes_no(creditos, 'RECIBO')
parse_categories(creditos, 'CLASE_PLAN')
parse_categories(creditos, 'siisa_subsectorLaboral')
parse_categories(creditos, 'siisa_sectorLaboral')
round_values(creditos, 'siisa_ingreso', 1000)
round_values(creditos, 'siisa_compromiso', 100)
round_values(creditos, 'siisa_montoMorasBCRA', 100)
parse_int(creditos, 'siisa_relDepMeses')
round_values(creditos, 'veraz_score', 10)
round_values(creditos, 'siisa_sesModelo', 5)
round_values(creditos, 'siisa_consultasAno', 1)
parse_categories(creditos, 'siisa_sectorLaboral')
round_values(creditos, 'siisa_ingreso', 1000)
round_values(creditos, 'siisa_compromiso', 100)
parse_int(creditos, 'siisa_maxBCRA24m')
parse_int(creditos, 'siisa_score')
parse_categories(creditos, 'siisa_scorePoblacion')
parse_int(creditos, 'siisa_maxBCRA12m')
parse_int(creditos, 'siisa_cantMoras')
parse_int(creditos, 'siisa_maxBCRA6m')
parse_int(creditos, 'siisa_consultasSeisMeses')
parse_int(creditos, 'siisa_sesCat')
parse_int(creditos, 'siisa_consultasDosAno')
parse_int(creditos, 'siisa_consultasTresMeses')
parse_int(creditos, 'siisa_consultasMes')
rename_columns(creditos, 'creditos')
time_diff = round(time.time() - last_time)
print(" {} segundos\n".format(time_diff))

#-----------------------------------------------------
# clientes
#-----------------------------------------------------
print("--- CLIENTES")
last_time = time.time()
print("  + Leyendo Archivo")
clientes = pd.read_csv('clientes.csv', sep='|', encoding='iso-8859-1')

print("  + Procesando")
for col in ['TDOC', 'NROC','FECHA_ALTA_LABORAL','SUCURSAL','COD_POSTAL_PER','PROVINCIA_PER']:
    if col in clientes.columns:
        drop_column(clientes, col)

parse_date(clientes, 'FALTA')
parse_date(clientes, 'FNAC')
round_values(clientes, 'INGRESO_NETO', 1000)
parse_categories(clientes, 'TIPOLABORAL')
parse_categories(clientes, 'METAL')
parse_int(clientes, 'OPERACIONES')
parse_int(clientes, 'REFINES')
parse_int(clientes, 'PEOR_ATRASO_HIST')
parse_int(clientes, 'JUICIOS_CANCELADOS')
parse_categories(clientes, 'APTO_VENTA_EN_CAJA')
rename_columns(clientes, 'clientes')

time_diff = round(time.time() - last_time)
print(" {} segundos\n".format(time_diff))


result = generate_dataframe(creditos, clientes, cuotas, pagos)

# Varianza x columna
# cliente_edad                          2.116481e+02
# cliente_ingreso_neto                  4.176666e+08
# cliente_tipo_laboral                  1.240970e+01
# cliente_metal                         5.623737e+00
# cliente_operaciones                   7.284232e+01
# cliente_refines                       3.612121e-01
# cliente_peor_atraso_historico         8.333970e+03
# cliente_juicios_cancelados            0.000000e+00
# cliente_apto_venta_en_caja            2.443434e-01
# credito_id                            1.257127e+10
# credito_monto                         9.028718e+07
# credito_sucursal                      2.636556e+01
# credito_recibo                        1.990909e-01
# credito_clase_plan                    1.216162e-01
# credito_monto_moras_bcra              3.127971e+08
# credito_cantidad_moras_bcra           2.031313e-01
# credito_meses_relacion_dependencia    2.224145e+02
# credito_veraz_score                   0.000000e+00
# credito_consultas_anuales             1.287273e+00
# credito_consultas_mensuales           3.046465e-01
# credito_sector_laboral                1.714242e+00
# creditos_ingreso                      0.000000e+00
# credito_compromiso                    7.939467e+07
# credito_score                         2.518715e+04
# credito_max_bcra_24m                  1.594949e-01
# credito_max_bcra_12m                  1.594949e-01
# credito_max_bcra_6m                   1.594949e-01
# credito_cantidad_moras                1.425253e-01
# credito_categoria                     1.420202e+01
# credito_consultas_3m                  7.559596e-01
# credito_consultas_6m                  8.495960e-01
# credito_consultas_24m                 2.714646e+00
# confiabilidad_log                     7.675177e+00
# credito_ingreso                       2.049167e+08
# credito_score_veraz                   3.372489e+04
#
# Eliminamos todas las variables que no aportan mucha varianza y que no sirven (ej: cliente_id)
for col in ['cliente_id', 'cliente_edad', 'cliente_tipo_laboral', 'cliente_metal', 'cliente_operaciones',
            'cliente_refines', 'cliente_peor_atraso_historico', 'cliente_juicios_cancelados', 'cliente_apto_venta_en_caja',
            'credito_id', 'credito_sucursal', 'credito_recibo', 'credito_clase_plan', 'credito_cantidad_moras_bcra',
            'credito_meses_relacion_dependencia', 'credito_veraz_score', 'credito_consultas_anuales', 'credito_consultas_mensuales',
            'credito_sector_laboral', 'creditos_ingreso', 'credito_max_bcra_24m', 'credito_max_bcra_12m',
            'credito_max_bcra_6m', 'credito_cantidad_moras', 'credito_categoria', 'credito_consultas_3m', 'credito_consultas_6m',
            'credito_consultas_24m', 'credito_score_poblacion']:
    if col in result.columns:
        drop_column(result, col)

