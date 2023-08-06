source $2/config/shell_config.ini
projectDir=$1
cmd=$3
outputs=$4
echo "Project directory: $projectDir, build path: $2, cmd: $3, out path: $4"
cd $projectDir
if [[ "$TEST" = false ]]; then
	ls
	git pull
	if [[ "$cmd" = 'u' ]]; then
        echo "uploadArchives"
	    ./gradlew uploadArchives --stacktrace --info
	elif [[ "$cmd" = 'i' ]]; then
		echo "installDebug"
		./gradlew installDebug --stacktrace --info 
	else
		echo "command $cmd excute........"
		./gradlew $cmd --stacktrace --info
        
		if [ $? -ne 0 ]; then
		    echo "gradlew run error."
		else
            cp -rf ${projectDir}/app/build/outputs ${outputs}
			echo "fetch your apk in $outputs"
		fi
	fi
fi