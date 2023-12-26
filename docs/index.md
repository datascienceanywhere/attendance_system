
# Deploy Real-Time Attendance System on AWS EC2 Instance
It is highly recommed to use GIT bash for Windows. For Linux/Mac use default terminal.
## 0. Setting up Code for Deployment
1. Create a new directory with name `attendance_system_app`.
   ```bash
   $ mkdir attendance_system_app
   ```
2. Navigate to the folder
   ```bash
   $ cd attendance_system_app
   ```
3. Lets test our application that we developed in the previous lesson working or not.
   - Create virtual environemnt
     ```bash
     ~/attendance_system_app $ python -m venv  virtualenv
     ```
   - Activate virtual environment
     For windows (if git bash),
     ```bash
     ~/attendance_system_app $ source virtualenv/Scripts/activate
     ```
     For windows (command prompt or powershell)
     ```bash
     ~/attendance_system_app $ virtualenv\Scripts\activate
     ```
     For Linux/Mac
     ```bash
     ~/attendance_system_app $ source virtualenv/bin/activate
     ```
   - Create another directory with name `app`
     ```bash
     (virtualenv) ~/attendance_system_app $ mkdir app
     ```
      - Then copy and paste complete application code in `app` directory.
   - Install only required packages from `requirements.txt` in app folder. Make sure you check that only necessary packages are there in requirements.txt file
     ```bash
     (virtualenv) ~/attendance_system_app $ cd app
     (virtualenv) ~/attendance_system_app/app $ pip install -r requirements.txt
     ```
  - Run the application
     ```bash
     (virtualenv) ~/attendance_system_app/app $ streamlit run Home.py
     ```
4. Remove all unnecesary files that are not part of the application to run which lite our application.
5. Modifiy our code of streamlit-webrtc as per official documentation.
   - HTTPS is required to access local media devices.
      > Create bash file with name "configure.sh" and copy and paste below code
      > ```bash
      >  echo "
      >      <VirtualHost *:80>
      >          ServerName <domain or ip address>
      >          Redirect / https://<domain or ip address>
      >      </VirtualHost> 
      >      
      >      <VirtualHost  *:443>
      >      
      >          ServerName <domain or ip address>
      >          SSLEngine on
      >          SSLProxyEngine On
      >          SSLCertificateFile      /etc/ssl/certs/ssl-cert-snakeoil.pem
      >          SSLCertificateKeyFile /etc/ssl/private/ssl-cert-snakeoil.key
      >      
      >          ProxyRequests     Off
      >          ProxyPreserveHost On
      >          #AllowEncodedSlashes NoDecode
      >          <Proxy *>
      >              Order deny,allow
      >              Allow from all
      >          </Proxy>
      >      
      >          ProxyPass         /_stcore        ws://localhost:8501/_stcore
      >          ProxyPassReverse  /_stcore        ws://localhost:8501/_stcore
      >      
      >          # The order is important here
      >          ProxyPass         /        http://localhost:8501/
      >          ProxyPassReverse  /        http://localhost:8501/
      >      
      >      </VirtualHost>" > /etc/apache2/sites-available/deploy_attendance_app.conf
      > ```
   
   - STUN/TURN servers are required to establish the media stream connection.
      > Configure the STUN server
      > To deploy the app to the cloud, we have to configure the STUN server via the rtc_configuration argument on webrtc_streamer() like below.
      > ```bash
      > webrtc_streamer(
      >     # ...
      >     rtc_configuration={  # Add this config
      >        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
      >     }
      >     # ...
      > )
      > ```
      > This configuration is necessary to establish the media streaming connection when the server is on a remote host.
      > In cloud we need to apply inbound rules as `TYPE -> Custom UDP`  and `PORT range -> 49152 - 65535`
      > Reference: <https://github.com/whitphx/streamlit-webrtc?tab=readme-ov-file#serving-from-remote-host>
6. Create a bash file with name **main.sh** and in that copy and paste the below bash commands
   ```bash
   bash configure.sh
   streamlit run Home.py
   ```
## 1. Push Complete update code in github repository. Follow below git commands
   - Login to your Github account and create empty repository.
   - In your local computer use below git commands
   ```bash
   git init
   git add .
   git commit -m "attendance system"
   git remote
   git branch -M
   git push -u origin main
   ```


## 1. Create EC2 Instance

To set up a Real-Time Attendance System on an AWS EC2 Instance, follow these steps:

### 1.1 Log in to AWS Account
   - Open the AWS Management Console at [https://aws.amazon.com/](https://aws.amazon.com/).
   - Sign in to your AWS account.

### 1.2 Create EC2 Instance
   - Navigate to the EC2 Dashboard.
   - Click on "Launch Instance."
   - Choose the **Ubuntu** OS image.
   - Select the instance type as **t2.micro**.
   - Follow the on-screen instructions to complete the instance creation.

### 1.3 Connect to the Instance
   - Connect to the newly created instance as the **root** user.

## 2. Setting Up the Instance

### 2.1 Update Ubuntu Instance
   - Execute the following command to update the Ubuntu instance:
     ```bash
     $ sudo apt-get update
     ```

### 2.2 Install and Configure Apache2
   - Follow the steps outlined in the official [Ubuntu tutorial](https://ubuntu.com/tutorials/install-and-configure-apache#1-overview) to install and configure Apache2.
     ```bash
     $ sudo apt install apache2
     ```

### 2.3 Navigate to Default Root Directory
   - Change to the default root directory of Apache2:
     ```bash
     $ cd /var/www/html
     ```

### 2.4 Delete Default Index File
   - Remove the default `index.html` file from the directory:
     ```bash
     ~/var/www/html $ rm index.html
     ```
## Running app in EC2

### 3.1 Clone streamlit app using git

```bash
~/var/www/html $ git clone <your github repository>
```
### 3.2 Change directory to project folder
```bash
~/var/www/html $ cd attendance-system-app
```

### 3.2 Install all required packages in `requirements.txt`
```bash
~/var/www/html/attendance-system-app $ pip3 install -r requirements.txt
```
### 3.3 Run the streamlit app

```bash
~/var/www/html/attendance-system-app $ streamlit run Home.py
```
### 3.4 Configuring Inbound Rules in security group to view the web app with IP address.
Make sure you add below inbound rules 
|Type|Protocol|Port range|Source|CIDR blocks|
|:--:|:--:|:--:|:--:|:--:|
|SSH|TCP|22|Custom|0.0.0.0/0|
|Custom TCP|TCP|8501|Custom|0.0.0.0/0|


## Configure HTTPS with Apache2
1. 

### 3.4 Configuring Inbound Rules in security group
Make sure you add below inbound rules 
|Type|Protocol|Port range|Source|CIDR blocks|
|:--:|:--:|:--:|:--:|:--:|
|SSH|TCP|22|Custom|0.0.0.0/0|
|HTTPS|TCP|443|Custom|0.0.0.0/0|
|HTTP|TCP|80|Custom|0.0.0.0/0|





### 

Now, your EC2 instance is set up with Apache2 installed and the default web page removed. You can proceed to deploy your Real-Time Attendance System on this instance. Customize the Apache2 configuration and upload your application files to the `/var/www/html` directory for hosting on the web server.
