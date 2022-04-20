# JDLOGIN
使用 vnc selenium 等技术自助获取 jd cookie 并部署到 qinglong 环境变量  
自用请勿登录  

![](https://cdn.jsdelivr.net/gh/kaminodalao/Assets@main/images/202204210000976.png)  

## 优点
完全没有

## 功能
- 使用网页vnc登录jd获取cookie
- cookie部署到qinglong环境变量(暂无)

## 部署
### 前端页面
```
git clone https://github.com/kaminodalao/JdLogin.git -b frontend jdlogin_frontend
cd jdlogin_frontend
yarn
yarn build
```
### docker容器
```
git clone https://github.com/kaminodalao/JdLogin.git -b main jdlogin_docker
cd jdlogin_docker
docker build -t jdlogin:debug .
```

### 后端服务
```
git clone https://github.com/kaminodalao/JdLogin.git -b main jdlogin_api
cd jdlogin_api
cp config.example.json config.json
pip install -r requirements.txt
flask db init
flask db migrate
flask db upgrade
python app.py
```

