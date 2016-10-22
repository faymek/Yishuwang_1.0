# Yishuwang_1.0
易书网
----------
先在自己的github尝试一下
使用说明:

1. 使用github客户端把本repository clone到本地，然后用pycharm
点击file->ope 然后找到你clone的目录->Yishuwang_1.0 

2. 然后用命令行依次执行：

- 数据库

`python manage.py makemigrations`

`python manage.py migrate`

- 管理员账户

`python manage.py createsuperuser`

- 然后按照提示输入 注意密码输入的时候不显示出来，就好像没输入一样  

- 运行

`python manage.py runserver `

python manage.py migrate your_app --fake
