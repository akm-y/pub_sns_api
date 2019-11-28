[SystemVersion]
Python Version 3.7.3
Django Version 2.0
pip3 Version 9.0.3
mysql
DynamoDB

[commands]
＜linux,unix＞
Django(FrameWork)
{code}
cd /var/www/vhosts/django/
source bin/activate
{/code}

uwsgi(AppServer)
{code}
・httpを使用
uwsgi --http :8001 --wsgi-file api/wsgi.py --master --processes 1 --threads 1 --stats 127.0.0.1:8001 --pythonpath /usr/bin/python   --chmod-socket=777 --gid nginx --uid nginx　-s api.sock

・uwsgiを使用nohup uwsgi --wsgi-file api/wsgi.py --master --processes 1 --threads 1 --pythonpath /usr/bin/python   --chmod-socket=777 --gid nginx --uid nginx -s api.sock -s ./aip.soxk &

{/code}

nginx（PloxyServer）
{code}
systemctl start nginx
systemctl stop nginx
systemctl status nginx
{/code}
config
{code}
vi /etc/etc/nginx/conf.d/api.conf
{/code}

＜win10＞
{code}
git clone git@github.com:akm-y/hulicol_api.git
cd hulicol_api2
virtualenv ./
pip3 install django == 2.0
Scripts/activate
python .\manage.py runserver --debug-mode
{/code}

[Env Value]
Production Settings by  api/settings/prod.py

using
{code}
//win
python .\manage.py runserver
{/code}

Development Settings by api/settings/dev.py
uwsgi起動

[package]
setting file output
{code}
pip3 freeze > requirements.txt
{/code}

setting file input
{code}
pip3 install -r requirements.txt
{/code}