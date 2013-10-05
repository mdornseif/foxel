Experimente zur automatischen Ganprofilvermessong von Hohlräumen. Das Ergebnis sieht dann etwa so aus:

![Unter meinem Schreibtisch](http://static.23.nu/md/Pictures/PythonSnapz001.png)

Entwickelt mit einem Hokuyo-URG04 SCIP 1.0 LIDAR und gedacht für die Forschungsarbeit des Arbeitskreises Kluterthöhle http://akkh.de/


Hardware
========

Momentan benutzen wir den [Hokuyo URG-04LX][1] Laser Range Finder, der  mit 500mA Stromverbrauch, 4095mm maximaler Messdistnaz und 240° Erfassungswinkel für unseren Anwendungsbereich gut geeignet. Der Strassenpreis für das Modul liegt momentan bei etwa 2000 Euro. 

Wir haben den URG-04LX in einer Höhle getestet und können unter üblichen Höhlenbedingungen eine Reichweite von etwa 2m errzeihelen, d.h. Gänge bis zu einem Querschnitt von 4m können erfasst werden. Bei stark verlehmten oder sehr feuchten Wänden erziehlen wir allerdings drastisch schlechtere Werte.

Der folgende Gangquerschnitt ist exemplarisch und [stammt aus der "Kückelhauser Klutert"][2]. Die roten "Laserstrahlen" geben gültiger Messwerte wieder - die fehlenden Werte sidn gut zu erkennen. Der Scanner benötigt eine zehntel sekunde für eine Messung.

![Kückelhauser Klutert](http://f.cl.ly/items/2u351v0B0V1F3K2C3q3j/Image%202012.02.16%2022:04:13.png)

Der [Hokuyo URG-04LX-UG01] ist eine etwa halb so teure Alternative, aber bisher ungetestet. Der [Hokuyo UTM-30LX] kostet etwa doppelt so viel, hat aber 270° Erfassungswinkel und biz zu 30.000mm (30m!) Reichweite. Mit 700mA Stromverbrauch ist er auch noch für mobile Anwendugen gut geeignet. Beide Geräte haben allerdings nur eine USW-Schnittstelle, die mit Eigenbau-Elektronik nicht ganz einfach anzusprechen ist. Beide Geräte sind bisher nicht getestet.



Implementierung
===============

Zur Ansteuerung des LIDAR siehe [`foxellib.py`][3]. 


1: http://www.hokuyo-aut.jp/02sensor/07scanner/urg_04lx.html
2: http://blog.akkh.de/experimente-mit-volldigitaler-gangprofilverme
3: https://github.com/mdornseif/foxel/blob/master/foxellib.py


[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/mdornseif/foxel/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

