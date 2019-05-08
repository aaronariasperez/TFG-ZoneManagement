# TFG-ZoneManagement

Para crear los datasets, hay que ejecutar el script 'run.bat' una vez por cada proporción de tramos verdes que se quiera cubrir, en una consola distinta cada una para crear
5 procesos para utilizar 5 núcleos de la CPU.

Antes de esto hay que limpiar las carpetas 'datasets' y 'routes'.

start run.bat 0.02
start run.bat 0.05
start run.bat 0.1
start run.bat 0.15
start run.bat 0.2

Al ejecutar estos 5 comandos en 5 consolas distintas, se creará en la carpeta datasets un datasetX.csv donde X es el porcentaje de tramo verde que se quiere cubrir. 
Cada uno de estos csv tendrá 183*20=3660 entradas, que luego fusionaremos en un único dataset.

Para fusionar todos los datasets creados en la carpeta 'datasets', ejecutamos 'Merge_datasets.py' y nos creará un archivo 'dataset.csv' en el directorio principal.