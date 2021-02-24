# example call i.e. "from params import params, today"
import datetime
from pandas import Series

today = datetime.datetime.today()

# PARAMETER DEFINITIONS:
params = dict(country = "spain",
          region = "andalucia",
          sub_region = "cordoba",
             )
              
format_params = dict(formato = "%Y-%m-%d",
              formato_query = "%Y-%m-%d",
                    )

params.update(format_params)

dates_params = dict( 
                 start_date = datetime.datetime.strptime("2021-01-01", params["formato"]),
                 end_date = datetime.datetime.strptime("2021-01-14", params["formato"]),
                    )

params.update(dates_params)


cols = ['today_confirmed',
 'today_deaths',
 'today_hospitalised_patients_with_symptoms',
 'today_intensive_care',
 'today_new_confirmed',
 'today_new_deaths',
 'today_new_hospitalised_patients_with_symptoms',
 'today_new_intensive_care',
 'today_new_open_cases',
 'today_new_recovered',
 'today_new_total_hospitalised_patients',
 'today_open_cases',
 'today_recovered',
 'today_total_hospitalised_patients',
 'today_vs_yesterday_confirmed',
 'today_vs_yesterday_deaths',
 'today_vs_yesterday_hospitalised_patients_with_symptoms',
 'today_vs_yesterday_intensive_care',
 'today_vs_yesterday_open_cases',
 'today_vs_yesterday_recovered',
 'today_vs_yesterday_total_hospitalised_patients',
 'yesterday_confirmed',
 'yesterday_deaths',
 'yesterday_hospitalised_patients_with_symptoms',
 'yesterday_intensive_care',
 'yesterday_open_cases',
 'yesterday_recovered',
 'yesterday_total_hospitalised_patients']

cols = Series(cols,)

