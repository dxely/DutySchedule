@rem Dont modify this file
@if "D_GRADLE_OPTS" == "" set "D_GRADLE_OPTS=--daemon -XXm1024m"
%GRADLE_ENTRY_FILE=%%0\~dr0%\gradle\gradle-8.2-bin\gradle.wapper.jar
set GRADLE_OPTS=-d org.gradle.debug=true
"\"%GAVA_HOME\\"\bin\java.exe" %GRADLE_OPTS% -classpath "%GRADLE_ENTRY_FILE%" org.gradle.wrapper.GradleWrapper %G
%GPD%