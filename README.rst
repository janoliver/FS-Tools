==========
 FS Tools
==========

Diese Django Anwendung beinhaltet einige Tools, die verschiedene
Aufgaben der Fachschaft Physik in Marburg vereinfachen. Dazu geh�ren
derzeit die Vorlesungsevaluation und ein Programm zum Erstellen der 
Auswertung dieser und des LaTeX Codes f�r die Zeitschrift *Renthofpostille*.
Diverse weitere Apps kommen mit der Zeit dazu. (hoffentlich!)

Abh�ngigkeiten
==============

* Django PAM f�r die Integration der Linux Benutzerdatenbank:
  https://bitbucket.org/maze/django-pam
* django 1.3
* Python > 2.5
* Sqlite3

Installation:
=============

1. Repo clonen
#. Datenbank erstellen mit: ``python manage.py syncdb``
#. Server starten mit: ``python manage.py runserver`` 
#. *127.0.0.1:8000* besuchen
