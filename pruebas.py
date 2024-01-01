from dfgpx import dfgpx

archivo_gpx ="rutas_gpx\Sendero_Perez_Nortes.gpx"

ruta = dfgpx(archivo_gpx)

print(ruta.desnivel_acumulado("meters"))


# Guardar el dataframe en un archivo de Excel

nombre = "rutas_xlsx\\" + "Sendero_Perez_Nortes" + ".xlsx"
ruta.df.to_excel(nombre, index=False) 