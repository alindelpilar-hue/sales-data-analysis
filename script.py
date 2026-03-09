Objetivos del proyecto
1-cuales son los productos ms vendidos(Proyectos mas vendidos)
2-q estado tiene mas ventas(Estados con mas vendidos) 
3-cual es el compotamiento de ventas por mes?(Comportamiento mensual)
4-existen patrones en los clientes frecuentes(Patrones de clientes)
*tips-revisar quienes son esos clientes, ver q compran, cuanto gstan, cuando compran?

fuente kaggle.
#importar el archivo e importar librerias
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
path=link
data=pd.read_csv(path)

#analizar la data en busca de archivos nulos y duplicados
data.columns
data.isna().sum() 
#the dt set its already clean, so we dont need to erase null value or refill it.
data['order_id'].duplicated().sum()
# el dtaset no tiene duplicados pero en la columna country tenemos errores

data['country']=data['country'].replace('India','Estados Unidos')
data.head()#arreglar la columna country

#separa el top 10 de productos mas vendido para guardarlo en un documento para exportarlo mas tarde y usarlo en power point
top_10=data.groupby("product_name")["quantity"].sum().sort_values(ascending=False).head(10)
top_10.to_csv('top 10 of the products with more sales.csv')

# Hacemos una vizualizacion para ir entendiendo el comportamiento por producto
top_10.plot(kind="bar", figsize=(10,5))
plt.title("Top 10 productos más vendidos")
plt.xlabel("Producto")
plt.ylabel("Cantidad vendida")
plt.show()

#separar el top 10 d ciuddes q mas han pagado.
top_city=data.groupby(['city','state'])['total_sales'].sum().sort_values(ascending=False).head(10)
top_city.to_csv('states and cities with more sales.csv')

#vizualizamos tamben este reultado
top_city.plot(kind="bar", figsize=(10,5), color="orange")
plt.title("Estados con más ventas")
plt.xlabel("Ciudad / Estado")
plt.ylabel("Ventas totales")
plt.show()


#conocer el comportmiento de las ventas de manera mensual
# Asegurar formato fecha
data['order_date'] = pd.to_datetime(data['order_date'])

# Extraer mes
data['month'] = data['order_date'].dt.month

# Ventas totales por mes
ventas_mensuales = data.groupby('month')['total_sales'].sum()
ventas_mensuales.to_csv("monthly_sales.csv")
#graficar el comportaiento
plt.figure(figsize=(8,5))
plt.plot(ventas_mensuales.index, ventas_mensuales.values, marker='o')
plt.xlabel('Mes')
plt.ylabel('Ventas Totales')
plt.title('Comportamiento de Ventas por Mes')
plt.grid(True)
plt.show()


#analizar o identificar los patrones entre los clientes frecuentes
clientes=data['customer_id'].value_counts().head(10)

patron_producto = (
    data.groupby(['customer_id', 'product_name'])['quantity']
    .sum()
    .reset_index()
)

patron_mensual = (
    data.groupby(['customer_id', 'month'])['order_id']
    .count()
    .reset_index()
)

patron_gasto = (
    data.groupby('customer_id')['total_sales']
    .sum()
    .sort_values(ascending=False)
)


# tratamos de identificar clientes vip y clientes ocasionales
fecha_actual = data['order_date'].max()

rfm = data.groupby('customer_id').agg({
    'order_date': lambda x: (fecha_actual - x.max()).days,
    'order_id': 'count',
    'total_sales': 'sum'
})

rfm.columns = ['Recency', 'Frequency', 'Monetary']

rfm.sort_values('Monetary', ascending=False).head()
rfm.to_csv("rfm_customers.csv")

# vizualizamos los resultados
plt.scatter(rfm["Frequency"], rfm["Monetary"])
plt.xlabel("Frequency")
plt.ylabel("Monetary")
plt.title("Customer Segmentation")
plt.show()