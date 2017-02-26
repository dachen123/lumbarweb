#!/usr/bin/zsh
BASE_PATH=$CM_BACKEND_DIR
SCRIPT_PATH=$BASE_PATH/cm_web/script
CONF_PATH=$SCRIPT_PATH
EXE_PATH=/home/lumbarv2/project/venv/bin
PID_FILE=/var/run/lumbarv2_web/gunicorn/gunicorn_lumbarv2_web.pid

export PROJ_PATH=$BASE_PATH
export PYTHONPATH=$CM_BACKEND_DIR:$PYTHONPATH

cd $SCRIPT_PATH
case $1 in                                                                                
    'start')
	echo '启动gunicorn进程树'
        $EXE_PATH/gunicorn --config $CONF_PATH/gunicorn_conf.py run:app
	sleep 0
        ;;  
    'stop') 
	echo '停止gunicorn进程树'
	cat $PID_FILE | xargs kill
	sleep 0
        ;;                                                                                
    'restart')
	$0 stop
	sleep 1
	$0 start
	;;
    'status')
	ids=`pgrep lumbarv2_web_gunicorn`
	echo "正在活动的gunicorn父进程号(需要root权限才能杀): $ids"
	;;
    *)                                                                                    
        echo "$0 start|stop|restart|status"
    	;;                                                                                
esac

