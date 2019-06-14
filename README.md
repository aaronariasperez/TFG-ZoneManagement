# TFG-ZoneManagement

## ¿De qué trata este proyecto? ##

Lo que se trata de conseguir con este projecto es desarrollar un sistema inteligente que haga una planificación de los tramos de una ruta de autobús (para un autobús híbrido eléctrico enchufable), es decir, que se decida si utilizar el motor eléctrico o el de combustión para cada tramo, de modo que el uso de la batería sea lo mas óptimo posible. Además, también se respetará los tramos verdes, donde el vehículo deberá de utilizar el motor eléctrico obligatoriamente.

Para esto el problema se divide en dos contextos, el estático y el dinámico. En el estático se da una solución (una planificación de ruta) a priori, es decir, antes de que se empiece la ruta. Esto lo resolvemos mediante un algoritmo genético y también utilizando una red neuronal supervisada.
En el dinámico, la decisión por cada tramo se va tomando a medida que se va ejecutando. Para dar solución a este problema se ha utilizado una técnica de aprendizaje por refuerzo, la neuroevolución. Esta técnica utiliza un algoritmo genético para la optimización de los pesos de la red neuronal.

Se ha implementado un simulador simplificado para cada contexto, de manera que podamos entrenar y testear nuestros modelos.

##Información sobre la ejecución (en construcción)##

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

***************************************

Para hacer las pruebas del fitness del genético vs red neuronal, primero hay que ejecutar Create_route_for_nn.py, cambiando el path_windows2 con la ruta que queramos "routeX.csv" 
y cambiando la ruta donde se va a escribir el resultado "route_for_nnX.csv". Luego, debemos ejecutar Static_nn_allroute.py, cambiando el path_windows con la ruta que queramos 
"route_for_nnX.csv" y el path_windows4 igual, "routeX.csv". Cuando se ejecuta este script, se imprime el fitness del genético y de la red neuronal, además de la planificación
de la ruta que ha realizado la red neuronal.
