<img src="https://i.ibb.co/YD4XKb8/02.png" alt="PyEWS" style="zoom: 80%;" />



# Python Electrical Wire Sizes 

El módulo PyEWS (**0.1.16**) puede ser utilizado para dimensionar conductores  de baja tensión de una instalación eléctrica. Es fácil de utilizar e interpretar sus resultados mostrando un panorama más general al poder visualizar por completo una lista de conductores propuestos con los parámetros de entrada.

## Instalación

La instalación del módulo se realiza con :

```Python
pip install ElectricalWireSizes
```

## Iniciar paquete de instalación

El módulo tiene dependencias siendo necesario instalar `tabulate` el cual da una mejor apariencia al momento de mostrar los resultados.

```tex
#VF: Tensión de fase o en su defecto tensión de línea para sistemas de 1F2H, 2F.
#VL: Tensión de línea.
#In: Corriente nominal total de una de las fases.
#Nc: Número de conductores por fase.
#L : Longitud en metros.
#FA: Número de conducrtores activos en el tubo conduit.
#Type: Tipo de tubo conduit (1:PVC,2:AL,3:ACERO)
#Ta: Temperatura ambiente en centigrados, únicamente ingresar la opcion númerica.
---- 1:20 2:25 3:30 4:35 5:40 6:45 7:50 8:55 9:60 10:65 11:70 12:75
#Vd: Caída de tensión (porcentual de 2, 3, 5)
---- 2,3,5	
#S:  Seleccione el sistema que desea propner en base a este se muestran los resultados.
---- 1:(1F-2H) 2:(2F-3H) 3:(3F-3H) 4:(3F-4H)
#Fp: Factor de potencia
#Op: Opción para mostrar resultados
	 1: Mostrar los resultados adecuadamente estructurado en una tabla. 
	 2: Mostrar los resultados como datos acumulados. Esta opción es necesario cuando se activa
	 	la función para múltiples cargas.
	
```

```python
import PyEWS
#Para conductores de cobre
PyEWS.MBTCU(VF,VL,In,Nc,L,FA,Type,Ta,Vd,S,Fp,Op)
#Para conductores de aluminio
PyEWS.MBTAL(VF,VL,In,Nc,L,FA,Type,Ta,Vd,S,Fp,Op)
```

El módulo de corriente directa  necesita la información siguiente :

```python
#MODBTCUSTD(Vcd,In,Nc,L,Class,Ta,Vd,View):
#Vcd   :  Tensión en corriente directa.
#In    :  Corriente directa del circuito.
#Nc    :  Número de conductores en corriente directa.
#L     :  Longitud del circuito en metros.
#Class :  Clase de conductor A:1 B:2 y C:3.
#Ta	   :  Temperatura ambiente 
#Vd	   :  Caída de tensión.
#View  :  Mostrar los resultados adecuadamente en una tabla con 1 para multiples cargas debe ser 2.

PyEWS.MBTCUSTD(1200,145,1,100,1,25,3,1)
```



## PyEWS Módulos

| Id   | Descripción                                                  | Módulo   | Versión |                      Descargar                      |
| ---- | ------------------------------------------------------------ | -------- | ------- | :-------------------------------------------------: |
| 1    | Módulo de baja tensión para conductores de cobre clase B, C y D  tensión de 600V a 2000V | MBTCU    | 0.1.15  | [PyEWS 0.1.16](https://github.com/jacometoss/PyEWS) |
| 2    | Módulo de baja tensión para conductores de aluminio clase B, C y  D, tensión 600V a 2000V | MBTAL    | 0.1.15  | [PyEWS 0.1.16](https://github.com/jacometoss/PyEWS) |
| 3    | Módulo de baja tensión para conductores de cobre clase B, C  y D en corriente directa hasta 2000 V | MBTCUSTD | 0.1.15  | [PyEWS 0.1.16](https://github.com/jacometoss/PyEWS) |

## Test

El módulo tiene dependencias por lo que es necesario instalar `tabulate` el cual da una mejor apariencia al momento de mostrar los resultados.

```python
import PyEWS
PyEWS.MBTCU(127,220,15,1,22,1,1,35,3,1,0.9,1)
```

Los se resultados muestran con la iteración de todos los conductores tanto para tensión monofásica como trifásica.

- `Vd (Voltage Drop)` es la pérdida de tensión porcentual 
- `60,75,90` la ampacidad real de los conductores.
- `Nc` es el número de conductores por fase.
- `Op` muestra si el resultado es correcto al aparecerer en la columna como Yes.
- `ITM` es la protección del circuito.

![Resultados](https://i.ibb.co/VDtY0vz/Ejemplo-01.jpg)

El circuito mostrado es la solución y para ver el resumen este fue agregado para la opción multiples cargas.

## Base de datos de conductores

Para poder ampliar el módulo se agregó la tabla de conductores donde incluye las resistencias y reactancias como ampacidades. Ingrese el código mostrado para visualizar la tabla completa.

```python
import PyEWS
#1 Conductores de cobre, 
#2 conductores de aluminio, 
#3 conductores de cobre estandar para corriente directa.
PyEWS.DBC(1)
```

## Múltiples cargas en corriente alterna

Para implementar una gran variedad de cargas se organizan como se muestra en el bloque de código, puede agregar hasta 25 cargas.

```python
carga=[
     ["1",127,220,15,1,22,1,1,35,3,1,0.9,2],
     ["2",127,220,12,1,22,1,1,25,3,1,0.9,2],
     ["2",127,220,22,1,22,1,1,25,3,1,0.9,2],
     ["2",127,220,22,1,22,1,1,25,3,1,0.9,2],
     ["2",127,220,22,1,22,1,1,25,3,1,0.9,2],
     ["2",127,220,22,1,22,1,1,25,3,1,0.9,2],
     ["2",127,220,22,1,22,1,1,25,3,1,0.9,2],
     ["2",127,220,22,1,22,1,1,25,3,1,0.9,2],
     ["1",127,220,15,1,22,1,1,35,3,1,0.9,2],    
     ["2",127,220,22,1,22,1,1,25,3,1,0.9,2],
     ["1",127,220,15,1,22,1,1,35,3,1,0.9,2],
     ["2",127,220,22,1,22,1,1,25,3,1,0.9,2],
     ["2",127,220,22,1,22,1,1,25,3,1,0.9,2],
     ["2",127,220,22,1,22,1,1,25,3,1,0.9,2],
     ["2",127,220,22,1,22,1,1,25,3,1,0.9,2],
     ["2",127,220,22,1,22,1,1,25,3,1,0.9,2],
     ["2",127,220,22,1,22,1,1,25,3,1,0.9,2],    
     ["2",127,220,22,1,22,1,1,25,3,1,0.9,2],
     ["2",127,220,22,1,22,1,1,25,3,1,0.9,2],
    ["3",127,220,196,3,55,0.8,3,75,3,3,0.9,2]
    ]
#Una forma sencilla de mostrar el total de cargas
print("Total de cargas : ",len(carga))
#Para mostar completo el desarrollo
#----------PyEWS.DBCIRCUIT(carga,1,1) #Cobre
#----------PyEWS.DBCIRCUIT(carga,1,2) #Aluminio
#Para mostar el resumen únicamente 
#----------PyEWS.DBCIRCUIT(carga,2,1) #Cobre
#----------PyEWS.DBCIRCUIT(carga,2,2) #Aluminio
```

Para mostrar el resumen para  conductores de cobre

```python
PyEWS.DBCIRCUIT(carga,2,1)
```

![Resultados](https://i.ibb.co/Btdp62f/A.jpg)

Para mostrar el resumen para conductores de aluminio

```python
PyEWS.DBCIRCUIT(carga,2,2)
```

![Resultados](https://i.ibb.co/DttdHzk/B.jpg)

## Múltiples cargas en corriente directa 

Para implementar una gran variedad de cargas se organizan como se muestra en el bloque de código, puede agregar hasta 25 cargas.

```python
#(Vcd,In,Nc,L,Class,Ta,Vd,View):
cargacd=[
    ["1",1200,30,1,100,1,25,3,2],
    ["2",1200,30,1,100,1,25,3,2],
    ["3",1200,30,1,100,1,25,3,2],
    ["4",1200,30,1,100,1,25,3,2],
    ["5",1200,30,1,100,1,25,3,2],
    ["6",1200,30,1,100,1,25,3,2],
    ["7",1200,30,1,100,1,25,3,2],
    ["8",1200,30,1,100,1,25,3,2],
    ["9",1200,30,1,100,1,25,3,2],
    ["10",1200,30,1,100,1,25,3,2],
    ["11",1200,30,1,100,1,25,3,2],
    ["12",1200,30,1,100,1,25,3,2],
    ["13",1200,30,1,100,1,25,3,2],
    ["14",1200,30,1,100,1,25,3,2]
    ]
print("Total de cargas : ",len(cargacd))
DBCIRCUITCD(cargacd,2,1)

#Para mostar completo el desarrollo
#----------PyEWS.DBCIRCUITCD(carga,1,1) #Cobre Estándar
#----------PyEWS.DBCIRCUITCD(carga,1,2) #Aluminio No disponible
#Para mostar el resumen únicamente 
#----------PyEWS.DBCIRCUITCD(carga,2,1) #Cobre Estándar
#----------PyEWS.DBCIRCUITCD(carga,2,2) #Aluminio No disponible
```

Para mostrar el resumen para  conductores de cobre estándar

```
DBCIRCUITCD(cargacd,2,2)
```

![MODBTCD](https://i.ibb.co/rswpHm2/04.jpg)

## Referencias

[1] Norma Oficial Mexicana NOM-001-SEDE-2012, *Instalaciones Eléctricas (utilización)*

[2] Thue, W., 1978. *Electrical Power Cable Engineering*. 2nd ed. New York, Basel: Marcel Dekker Inc., p.34.

