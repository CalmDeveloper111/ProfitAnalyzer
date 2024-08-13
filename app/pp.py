import matplotlib.pyplot as plt
import io
import base64

def extract_discount(dis_str):
    if '%' in dis_str :
        return float(dis_str.split('%')[0])
    elif 'off' in dis_str:
        return float(dis_str.split(' ')[0])
    else: 
        return 0.0
    

def process(data) :
    
    data['discount percentage']=data['Discounts and Offers'].apply(lambda x: extract_discount(x))
    data['discount amount']=data.apply(lambda x: (x['Order Value'] * x['discount percentage']/100)
                                  if x['discount percentage'] > 1
                                  else x['discount percentage'],axis=1)
    data['final price']=data['Order Value']-data['discount amount']

    data['cost']=data['Delivery Fee']+data['Payment Processing Fee']+data['discount amount']

    data['revenue']=data['Commission Fee']
    data['profit']=data['revenue']-data['cost']

    return data


def overall_metrics (data) :

    total_orders = data['Order ID'].sum()
    total_cost = data['cost'].sum()
    total_revenue = data['revenue'].sum()
    total_profit = data['profit'].sum()

    overall_metrics = {

    'Total orders' : [total_orders] , 
    'Total cost' : [total_cost] , 
    'Total revenue' : [total_revenue] , 
    'Total profit' : [total_profit]
    
    }

    return overall_metrics

index_cost_break_down = None

def cost_breakdown(data) :
    global cost_break_down
    cost_break_down = data [['Delivery Fee' , 'Payment Processing Fee','discount amount']].sum()

    

    return cost_break_down


def hist_profit_per_order(data) :

    plt.switch_backend('Agg')
    fig = plt.figure(figsize=(10,6))
    ax = fig.add_subplot(111)
    ax.hist(data['profit'],bins=50,linewidth=1,color='skyblue',edgecolor='black')
    ax.set_xlabel('Profit')
    ax.set_ylabel('No of orders')
    ax.set_title('Profit per order')
    ax.axvline(data['profit'].mean(),linestyle='dashed',linewidth=1,color='red')

    plt.tight_layout()
    
    buffer = io.BytesIO()
    plt.savefig(buffer,format='png')
    buffer.seek(0)

    plot_data = base64.b64encode(buffer.read()).decode()

    plt.close(fig)

    return plot_data

def pi_chart_cost_break_down(data) :

    global index_cost_break_down
    index_cost_break_down = cost_break_down.index
    
    plt.switch_backend('Agg')
    fig = plt.figure(figsize=(16,8))
    ax = fig.add_subplot(111)
    ax.pie(cost_break_down,labels=index_cost_break_down,colors=['gold','silver','pink'],autopct='%1.1f%%',startangle=140)
    ax.set_title('Proportion of total cost in food delivery')

    plt.tight_layout()
    buffer = io.BytesIO()
    plt.savefig(buffer,format = 'png')
    buffer.seek(0)

    pie_data = base64.b64encode(buffer.read()).decode()

    plt.close(fig)

    return pie_data

    

    


        