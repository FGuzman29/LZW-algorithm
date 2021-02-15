# LZW-algorithm

los archivos a comprimir deben estar en el mismo directorio que el script

correr de la siguiente manera(ejemplo):
python lzw.py -c mifolder test3.txt
python lzw.py -d result.lzw		(puede borrar los archivos antes de descomprimir para comprobar que funciona)


////////////////////////////////////////////////////////////

Para correr el programa como un comando -lzw- en shell, en cualquier directorio, inicialmente se queria hacer un archivo .cmd o .bat que se corra una vez y quede todo listo
pero en el camino nos encontramos con alguna adversidades. 

paso 1) agregar directorio actual a path user variable
	setx PATH "%PATH%;%cd%"
este fue el unico comando que encontramos que permite agregar permanentemente a PATH (ya que -set- solo lo hace temporalmente) pero no nos funciono y ademas trunca el contenido de path del sistema a las del usuario
tambien intentamos sin exito con el el script adjunto.

paso 2)agregar python.exe y python scripts a path.
pero no podemos lograr esto ya que donde python esta instalado puede varia en cada computadora

paso 3) agregar .PY a la variable de sistema PATHEXT y correr lo siguiente:
	assoc .py=Python.File
	ftype Python.File=c:\path to\python.exe "%1" %*
pero no encontramos como editar PATHEX a traves de cmd


haciendo los pasos 2 y 3 se logra correr el programa simplemente escribiendo lzw pero solamente en el directorio donde se encuentra el script. O si se quiere correr donde desde cualquier directorio, agregar manualmente el directorio del script a path.



