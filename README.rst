==========
 FS Tools
==========

Diese Django Anwendung beinhaltet einige Tools, die verschiedene
Aufgaben der Fachschaft Physik in Marburg vereinfachen. Dazu gehören
derzeit die Vorlesungsevaluation und ein Programm zum Erstellen der 
Auswertung dieser und des LaTeX Codes für die Zeitschrift *Renthofpostille*.
Außerdem die Umfrage für den Patricia Pahamy Preis und ein Umfragemodul. 
Diverse weitere Apps kommen mit der Zeit dazu. (hoffentlich!)

Abhängigkeiten
==============

* django 1.4
* Jinja2
* Python > 2.5
* Sqlite3
* Jingo jinja2 interface
* South http://south.aeracode.org/ für Datenbank Migrationen

Installation:
=============

#. Repo clonen
#. Datenbank erstellen mit: ``python manage.py syncdb``
#. Server starten mit: ``python manage.py runserver`` 
#. *127.0.0.1:8000* besuchen
