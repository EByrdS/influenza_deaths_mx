# Mortalidad-INEGI

I cannot upload the database source files, but you can download them yourself using the file 
`download_data.py`. Run that file and two folder will be created: **/csv** and **/dbf**.
The databases are downloaded from two different webpages of INEGI
(Mexican National Institute for Statiscits and Geography), which you can consult on your browser:
* 2005-2011 (.dbf): https://www.inegi.org.mx/programas/mortalidad/default.html#Microdatos
* 2012-2018 (.csv): https://www.inegi.org.mx/programas/mortalidad/default.html#Datos_abiertos

Each web page contains the corresponding links to each database.

The script downloads the corresponding ZIP file from each link and decompress only the database
of interest, and discards the rest, so you do not have to worry about 
downloading a bunch of useless information. 

The names of the downloaded files are kept as the same names you would get if you downloaded
the databases manually, from a web browser.
