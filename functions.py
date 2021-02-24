from params import cols

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import datetime
import requests
import gc

from PIL import Image
from IPython.display import display


###---<Lambda Functions:>---###
col_lemma = lambda position: pd.Series([i.split("_")[position] for i in cols]).unique()
colsbylemma = lambda lemma: cols[cols.str.contains(lemma)]

###---<Normal Functions:>---###
def try_guest_shape(array):
    plotarr_shape_list = [(2,-1),(3,-1),(5,-1),(7,-1)]
    for s in plotarr_shape_list:
        try:
            result = array.reshape(s)
            break
        except Exception:
            continue
    return result.shape

def daterange2df(json, **params):
    end_date, start_date, formato = [params.get(i,) for i in ["end_date","start_date","formato"]]
    
    td = end_date - start_date
    dl = [end_date - datetime.timedelta(days=x) for x in range(td.days)]
    dl_parsed = [i.strftime(formato) for i in dl]
    print("dl:%a"%dl,
          "\n\ndl_parsed:%a"%dl_parsed)

    df = pd.DataFrame()
    for d in dl_parsed:
            df_new = pd.DataFrame(json["dates"][d]["countries"]["Spain"]).set_index("date").iloc[:,7:]
            df = pd.concat([df_new, df])
      
    df.index = df.index.astype("datetime64[ns]")
    df.sort_index(inplace=True)

    return df

def make_plots_by_lemma(lemma, df):
    lemma_arr = np.array(colsbylemma(lemma))
    sh = try_guest_shape(lemma_arr)

    import matplotlib.dates as mdates

    days = df.index
    fig, axs = plt.subplots(nrows=sh[0], ncols=sh[-1],
                           sharex=False, sharey=False, figsize=(20,20))
    #fig.set_tight_layout(10)
    for i in range(sh[0]):
        for j,field in enumerate(lemma_arr[ i*sh[-1] : (i+1)*sh[-1] ] ):
            
            axs[i,j].xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
            plt.setp( axs[i,j].xaxis.get_majorticklabels(), rotation=70 ,)
            axs[i,j].set_title(field)
            axs[i,j].plot(days, df[field])
            
    return fig,axs
###---<TLDR Functions:>---###

def api_covid19tracking(**params):
    # Requesting API
    global response
    global base_url, url
    base_url = "https://api.covid19tracking.narrativa.com"
    
    # params
    formato = params["formato"]
    formato_query = params["formato_query"]

    start_date = params["start_date"]
    end_date = params["end_date"]
    
    country = params["country"]
    region = params["region"]
    sub_region = params["sub_region"]

    def url_constructor(country=country, region=region, sub_region=None):
        url = base_url + "/api"
        if country:
            url += "/country/{0}"
        if region:
            url += "/region/{1}" 
        if sub_region:
            url += "/sub_region/{2}"

        return url

    
    # parameters to the GET request
    metadata = {"country":country,
               "region":region,
               }
    payload = {"date_from":start_date.strftime(formato_query),
               "date_to":end_date.strftime(formato_query),
              }
    headers= {'User-Agent': 'python-requests/2.24.0', 
              'Accept-Encoding': 'gzip, deflate', 
              'Accept': '*/*', 
              'Connection': 'keep-alive',
             }
   
    url = url_constructor(country, region, sub_region)
    
    # GET request
    response = requests.request("GET", url.format(country,region,sub_region), 
                                params=payload, 
                                headers=headers)
    # some pre-PRINTS
    print("pre-url: {}".format(url))
    print("url: %s"%url.format(country,region,sub_region), 
          "\nquery_url:%s"%response.url)
    print("status_code:%i"%response.status_code)
    return response.json()