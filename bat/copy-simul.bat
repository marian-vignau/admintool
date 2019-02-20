@ECHO OFF
SETLOCAL
rem  /S :: Copiar subdirectorios, pero no los vacíos.
rem /Z :: Copiar archivos en modo reiniciable.
rem /B :: Copiar archivos en modo de copia de seguridad.
rem                /ZB :: Usar modo reiniciable; si se deniega el acceso, usar
rem                        modo de copia de seguridad.
rem /COPYALL :: copiar toda la información del archivo
rem /MT[:n] :: hacer copias multiproceso con n subprocesos
rem /R:n :: Número de reintentos en copias con errores; valor
rem /L :: Solo mostrar, no copiar
rem /V :: Producir resultados detallados
rem /UNILOG:archivo :: Incluir estado en archivo LOG como UNICODE

rem echo myNameFull     %1
rem echo myNameShort    %~n1
rem echo myNameLong     %~nx1
rem echo myPath        %~dp1


robocopy "w:\%~nx1" "j:\%~nx1" /E /ZB /copyall /mt:24 /R:2 /V /L /unilog:"j:\%~nx1.log"
