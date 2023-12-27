![Screenshot 2023-12-26 180229](https://github.com/datascienceanywhere/attendance_system/assets/75901421/42153374-8786-4059-80e3-3ecb1676c27d)## Deploy Real-Time Attendance System on AWS EC2 Instance
It is highly recommended to use **GIT Bash** for Windows. For Linux/Mac, use the default terminal.

### 1. Setting up Code for Deployment
##### 1.1. Create a new directory with the name attendance_system_app.
  
  ```bash
  $ mkdir attendance_system_app
  ```
  
##### 1.2. Navigate to the folder
  
  ```bash
  $ cd attendance_system_app
  ```
  
##### 1.3. Lets test the application developed in the previous lesson. First Create a virtual environment.
  
```bash
~/attendance_system_app $ python -m venv virtualenv
```
  
##### 1.4. Activate the virtual environment
  - For Windows (Git Bash)
    ```bash
    ~/attendance_system_app $ source virtualenv/Scripts/activate
    ```
  - For Windows (Command Prompt or PowerShell),
    
    ```bash
    ~/attendance_system_app $ virtualenv\Scripts\activate
    ```
  - For Linux/Mac
    ```bash
    ~/attendance_system_app $ source virtualenv/bin/activate
    ```
      
##### 1.5. Create another directory named `app`
  ```bash
  (virtualenv) ~/attendance_system_app $ mkdir app
  ```

##### 1.6. Copy and paste the complete application code into the app directory.
  
##### 1.7. Install required packages from `requirements.txt` in the app folder.
  ```bash
  (virtualenv) ~/attendance_system_app $ cd app
  (virtualenv) ~/attendance_system_app/app $ pip install -r requirements.txt
  ```
  
##### 1.8. Run the application
  ```bash
  (virtualenv) ~/attendance_system_app/app $ streamlit run Home.py
  ```

### 2. Add necessary code into the app for streamlit-webrtc to run in cloud 

##### 2.1. Remove all unnecessary files not part of the application.

##### 2.2. Modify the code of streamlit-webrtc as per the official documentation.

- HTTPS is required to access local media devices.
  - Create a bash file named "configure.sh" and copy and paste the following code:
    ```bash
  echo "
      <VirtualHost *:80>
          ServerName <domain or ip address>
          Redirect / https://<domain or ip address>
      </VirtualHost> 
      
      <VirtualHost  *:443>
      
          ServerName <domain or ip address>
          SSLEngine on
          SSLProxyEngine On
          SSLCertificateFile      /etc/ssl/certs/ssl-cert-snakeoil.pem
          SSLCertificateKeyFile /etc/ssl/private/ssl-cert-snakeoil.key
      
          ProxyRequests     Off
          ProxyPreserveHost On
          #AllowEncodedSlashes NoDecode
          <Proxy *>
              Order deny,allow
              Allow from all
          </Proxy>
      
          ProxyPass         /_stcore        ws://localhost:8501/_stcore
          ProxyPassReverse  /_stcore        ws://localhost:8501/_stcore
      
          # The order is important here
          ProxyPass         /        http://localhost:8501/
          ProxyPassReverse  /        http://localhost:8501/
      
      </VirtualHost>" > /etc/apache2/sites-available/deploy_attendance_app.conf
      ```
    
  - STUN/TURN servers are required to establish the media stream connection. Configure the STUN server. To deploy the app to the cloud, configure the STUN server via the rtc_configuration argument on webrtc_streamer() as follows:
    ```python
    webrtc_streamer(
        # ...
        rtc_configuration={
            "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
        }
        # ...
    )
    ```
  - Apply inbound rules for cloud deployment as TYPE -> Custom UDP and PORT range -> 49152 - 65535.
  - Reference: [Streamlit-webrtc Documentation](https://github.com/whitphx/streamlit-webrtc?tab=readme-ov-file#serving-from-remote-host)

##### 2.3. Create a bash file with the name main.sh and copy and paste the following bash commands:
```bash
bash configure.sh
streamlit run Home.py
```

### 3. Push Complete Update Code to GitHub Repository

##### 3.1. Log in to your GitHub account and create an empty repository.

##### 3.2. In your local computer, use the following git commands:
```bash
$ echo "# attendance-system-app" >> README.md
$ git init
$ git add README.md
$ git commit -m "first commit"
$ git branch -M main
$ git remote add origin https://github.com/datascienceanywhere/attendance-system-app.git
$ git push -u origin main
```
### 4. Clone app in AWS EC2 Instance

##### 4.1. Log in to AWS Account
  - Open the AWS Management Console at https://aws.amazon.com/.
  - Sign in to your AWS account.
      
##### 4.2. Create EC2 Instance
- Navigate to the EC2 Dashboard.
- Click on "Launch Instance."
- Choose the Ubuntu OS image.
- Select the instance type as t2.micro.
- Follow the on-screen instructions to complete the instance creation.
  
##### 4.3. Connect to the Instance
- Connect to the newly created instance as the root user.
      
##### 4.4. Setting Up the Instance to run streamlit app
a) Update Ubuntu Instance. Execute the following command to update the Ubuntu instance:

```bash
$ sudo apt-get update
```

b) Install and Configure Apache2. Follow the steps outlined in the official Ubuntu tutorial to install and configure Apache2.

```bash
$ sudo apt install apache2
```

c) Navigate to Default Root Directory. Change to the default root directory of Apache2:

```bash
$ cd /var/www/html
```

d) Delete Default `index.html` File. Remove the default index.html file from the directory:

```bash
~/var/www/html $ rm index.html
```

e) Clone Streamlit App Using Git
```bash
~/var/www/html $ git clone <your github repository>
```

f) Change Directory to Project Folder
```bash
~/var/www/html $ cd attendance-system-app
```

g) Install All Required Packages in requirements.txt
```bash
~/var/www/html/attendance-system-app $ pip3 install -r requirements.txt
```

h) Run the Streamlit App

```bash
~/var/www/html/attendance-system-app $ streamlit run Home.py
```

i) Configure Inbound Rules in Security Group to View the Web App with IP Address
  - Make sure to add the following inbound rules:
    
| Type | Protocol | Port Range | Source | CIDR blocks|
| :---: | :---: | :---: | :---: | :---: |
| SSH | TCP | 22 | Custom | 0.0.0.0/0 |
| Custom | TCP | 8501 | Custom | 0.0.0.0/0 |
    
    
### 5 Configure HTTPS with Apache2
##### 5.1 Run the configure.sh bash file with the following command:

```bash
~/var/www/html/attendance-system-app $ bash configure.sh
```
This command will create a file deploy_attendance_app.conf in the /etc/apache2/sites-available/ directory.
  
##### 5.2 Open the deploy_attendance_app.conf file in /etc/apache2/sites-available/ directory using vim:

```bash
~$ vi /etc/apache2/sites-available/deploy_attendance_app.conf
```
  
##### 5.3 Modify the deploy_attendance_app.conf as per the provided screenshot.
![Screenshot 2023-12-26 180229](https://github.com/datascienceanywhere/attendance_system/assets/75901421/2fa93cf2-16ae-482d-ba83-6c85c51652b8)

##### 5.4 Enable the site within the Apache2 configuration:

```bash
~$ sudo a2ensite /etc/apache2/sites-available/deploy_attendance_app.conf
```
  
##### 5.5 Restart Apache2 server:

```bash
~$ sudo service apache2 restart
```
  
##### 5.6 Configure Inbound Rules in Security Group, Make sure to add the following inbound rules:
  
| Type | Protocol | Port Range | Source | CIDR blocks|
| :---: | :---: | :---: | :---: | :---: |
| SSH | TCP | 22 | Custom | 0.0.0.0/0 |
| HTTPS | TCP | 443 | Custom | 0.0.0.0/0 |
| HTTP | TCP | 80 | Custom | 0.0.0.0/0 |

### 6. Run Jobs with `pm2`

#### 6.1. Install [npm](https://docs.npmjs.com/about-npm) and [pm2](https://www.npmjs.com/package/pm2)

```bash
$ sudo apt install npm
```
Now install pm2 with npm
```bash
$ npm install pm2 -g
```
#### 6.2 Start app with pm2

```bash
~/var/www/html/attendance-system-app $ pm2 start "streamlit run Home.py" --name "Attendance App"
```

#### 6.3 Continous excution with pm2
By default, PM2 may stop running the app if the instance is restarted. To prevent this from happening, execute the following command:

```bash
$ pm2 startup "Attendance App"
```

