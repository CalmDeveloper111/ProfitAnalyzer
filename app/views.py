from django.shortcuts import render , HttpResponse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from . import pp

# Create your views here.

# def index(request) :
#     return HttpResponse('This is the index page')

def index(request) :
    return render(request,'index.html')

def file_upload(request) :
    if request.method == 'POST' :
        uploaded_data = request.FILES['file']
        data = pd.read_csv(uploaded_data)
        return data
    
# def analysis(request):
    # return  HttpResponse('This is the analysis page')

def analysis(request) :
    data =file_upload(request)

    data = pp.process(data)
 
#  overall metrics

    overall_metrics = pp.overall_metrics(data)
    overall_metrics_df = pd.DataFrame(overall_metrics)
    overall_metrics_result = overall_metrics_df.to_html(index=False)

#Total cost break down

    cost_break_down = pp.cost_breakdown(data)
    cost_break_down = cost_break_down.to_frame()
    cost_break_down_result = cost_break_down.to_html(index=True)

# histogram for Total profit per order

    hist = pp.hist_profit_per_order(data)

# pie chart for total cost breakdown

    pie = pp.pi_chart_cost_break_down(data)
  
    return render_template(request , overall_metrics_result ,cost_break_down_result,hist,pie)






def render_template(request , overall_metrics , cost_break_down ,hist,pie) :
    return render(request , 'result.html' , {'overall_metrics_result' : overall_metrics ,
                                             'cost_break_down_result' : cost_break_down , 
                                             'hist_total_profit_per_order' : hist ,
                                             'piechart_cost_break_down' : pie
                                             } )




    
