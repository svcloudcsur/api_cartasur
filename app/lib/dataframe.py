import sys
import traceback
import pandas as pd
import math

from datetime import datetime
from lib.tools import parse_date


#  Given a date it calculates the age
#  (doesn't have to be perfect, this is just an approximation)
# -------------------------------------------------------------------------
def calculate_age(client_birth_date):
    return ((datetime.now()  - client_birth_date) / 365.2425).dt.days


#  This function calculates a custom value that we call "confiabilidad_log"
#  which is the value we want to predict
#
#
def calculate_confiabilidad(id_credito, pagos, cuotas, ingreso_neto):
    try:
        f_pagos = []
        n_pagos = 0
        total_pagos = 0

        if len(pagos) > 0:
            f_pagos = pagos[pagos['pagos_FPAGO'] < datetime.now()]
            n_pagos = len(f_pagos)
            total_pagos_capital = f_pagos['pagos_CAPITAL'].sum()
            total_pagos_interes = f_pagos['pagos_INTERES'].sum()
            total_pagos = total_pagos_capital + total_pagos_interes

        n_cuotas = len(cuotas)

        total_cuotas_capital = cuotas['CAPITAL'].sum()
        total_cuotas_interes = cuotas['INTERES'].sum()
        total_cuotas = total_cuotas_capital + total_cuotas_interes

        pagos_vs_cuotas = (n_cuotas / n_pagos) if (n_pagos > 0) else 0
        total_pagos_vs_ingreso_neto = (total_pagos / ingreso_neto) if (ingreso_neto > 0) else 0.25
        total_pagos_vs_total_cuotas = (total_pagos / total_cuotas) if (total_cuotas > 0) else 1

        # confiabilidad = (pagos_vs_cuotas) * total_pagos_vs_total_cuotas * total_pagos_vs_ingreso_neto
        confiabilidad = 1 if total_pagos_vs_total_cuotas > 1 else total_pagos_vs_total_cuotas

        # confiabilidad = total_cuotas_capital
    except Exception as e:
        traceback.print_exc(file=sys.stdout)

    # print("=============================================================")
    # print("Total pagos: {}".format(total_pagos))
    # print("Total cuotas: {}".format(total_cuotas))
    # print("# cuotas: {}".format(n_cuotas))
    # print("# pagos: {}".format(n_pagos))
    # print("Ingreso Neto: {}".format(ingreso_neto))
    #
    return confiabilidad


#  This function calculates a custom value that we call "confiabilidad_log"
#  which is the value we want to predict
def calculate_confiabilidad_20210731(id_credito, pagos, cuotas):
    if pagos.empty:
        return -10 # If there's no payment, "confiabilidad_log" is very low

    monto_pagos = pagos[(pagos.pagos_ID_CREDITO == id_credito)]['pagos_CAPITAL'].sum()
    monto_pagos_log = monto_pagos

    if(cuotas.FVTO[0] == ''):
        monto_cuotas = monto_pagos
    else:
        cuotas_en_cuenta = cuotas[(cuotas.ID_CREDITO == id_credito) & (cuotas.FVTO <= datetime.now())]
        monto_cuotas = cuotas_en_cuenta['CAPITAL'].sum()

    if monto_pagos == 0:
        monto_pagos_log = 1

    confiabilidad = (monto_pagos / monto_cuotas)
    confiabilidad_log = math.log(monto_pagos_log) * (monto_pagos / monto_cuotas)

    return confiabilidad_log


def generate_dataframe(creditos, clientes, cuotas, pagos):
    df = pd.merge(clientes, creditos, left_on='clientes_ID_CLIENTE', right_on='creditos_ID_CLIENTE')

    #  COLUMN SELECTION (HEADER)
    result = pd.DataFrame(
        columns=['cliente_id',
                 'cliente_edad',
                 'cliente_ingreso_neto',
                 'cliente_tipo_laboral',
                 'cliente_metal',
                 'cliente_operaciones',
                 'cliente_refines',
                 'cliente_peor_atraso_historico',
                 'cliente_juicios_cancelados',
                 'cliente_apto_venta_en_caja',
                 'cliente_score',                       # This HAS to be the independent variable (selected by cartasur)
                 'credito_id',
                 'credito_monto',
                 'credito_sucursal',                    # Sucursal donde saco el credito
                 'credito_recibo',                      #
                 'credito_clase_plan',                  # RENOVAODR / NUEVO
                 'credito_monto_moras_bcra',
                 'credito_cantidad_moras_bcra',
                 'credito_meses_relacion_dependencia',
                 'credito_veraz_score',
                 'credito_consultas_anuales',
                 'credito_consultas_mensuales',
                 'credito_sector_laboral',
                 'creditos_ingreso',
                 'credito_compromiso',
                 'credito_score_poblacion',
                 'credito_score',
                 'credito_max_bcra_24m',
                 'credito_max_bcra_12m',
                 'credito_max_bcra_6m',
                 'credito_cantidad_moras',
                 'credito_categoria',
                 'credito_consultas_3m',
                 'credito_consultas_6m',
                 'credito_consultas_24m',
                 'confiabilidad_log'
                 ]
    )

    try:
        for index, row in df.iterrows():
            id_cliente = row.creditos_ID_CLIENTE
            id_credito = row.creditos_ID_CREDITO

            #  COLUMN SELECTION
            result = result.append(
                {
                    'cliente_id'                            : str(id_cliente),
                    'cliente_edad'                          : int(((datetime.now()  - clientes[(clientes.clientes_ID_CLIENTE == id_cliente)].clientes_FNAC) / 365.2425).dt.days),
                    'cliente_ingreso_neto'                  : row.clientes_INGRESO_NETO,
                    'cliente_tipo_laboral'                  : row.clientes_TIPOLABORAL_cat,
                    'cliente_metal'                         : row.clientes_METAL_cat,
                    'cliente_operaciones'                   : row.clientes_OPERACIONES,
                    'cliente_refines'                       : row.clientes_REFINES,
                    'cliente_peor_atraso_historico'         : row.clientes_PEOR_ATRASO_HIST,
                    'cliente_juicios_cancelados'            : row.clientes_JUICIOS_CANCELADOS,
                    'cliente_apto_venta_en_caja'            : row.clientes_APTO_VENTA_EN_CAJA_cat,
                    'cliente_score'                         : row.clientes_SCORE,
                    'credito_id'                            : id_credito,
                    'credito_monto'                         : creditos[(creditos.creditos_ID_CREDITO == id_credito)].creditos_MONTO.sum(),
                    'credito_sucursal'                      : row.creditos_SUCURSAL_cat,
                    'credito_recibo'                        : row.creditos_RECIBO,
                    'credito_clase_plan'                    : row.creditos_CLASE_PLAN_cat,
                    'credito_monto_moras_bcra'              : row.creditos_siisa_montoMorasBCRA,
                    'credito_cantidad_moras_bcra'           : row.creditos_siisa_cantMorasBCRA,
                    'credito_meses_relacion_dependencia'    : row.creditos_siisa_relDepMeses,
                    'credito_score_veraz'                   : row.creditos_veraz_score,
                    'credito_consultas_anuales'             : row.creditos_siisa_consultasAno,
                    'credito_consultas_mensuales'           : row.creditos_siisa_consultasMes,
                    'credito_sector_laboral'                : row.creditos_siisa_sectorLaboral_cat,
                    'credito_ingreso'                       : row.creditos_siisa_ingreso,
                    'credito_compromiso'                    : row.creditos_siisa_compromiso,
                    'credito_score_poblacion'               : row.creditos_siisa_scorePoblacion,
                    'credito_max_bcra_24m'                  : row.creditos_siisa_maxBCRA24m,
                    'credito_max_bcra_12m'                  : row.creditos_siisa_maxBCRA12m,
                    'credito_max_bcra_6m'                   : row.creditos_siisa_maxBCRA6m,
                    'credito_score'                         : row.creditos_siisa_score,
                    'credito_cantidad_moras'                : row.creditos_siisa_cantMoras,
                    'credito_categoria'                     : row.creditos_siisa_sesCat,
                    'credito_consultas_3m'                  : row.creditos_siisa_consultasTresMeses,
                    'credito_consultas_6m'                  : row.creditos_siisa_consultasSeisMeses,
                    'credito_consultas_24m'                 : row.creditos_siisa_consultasDosAno,
                    'confiabilidad_log'                     : calculate_confiabilidad(id_credito, pagos, cuotas, row.clientes_INGRESO_NETO)
                }, ignore_index=True)
    except Exception as e:
        traceback.print_exc(file=sys.stdout)

    return result.fillna(0)  # NaN has to be treated as 0
    # TODO: Create the same but to estiamte the amount that can be lent
