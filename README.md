# Deploy Real-Time Attendance System on AWS EC2 Instance

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
     sudo apt-get update
     ```

### 2.2 Install and Configure Apache2
   - Follow the steps outlined in the official [Ubuntu tutorial](https://ubuntu.com/tutorials/install-and-configure-apache#1-overview) to install and configure Apache2.
     ```bash
     sudo apt install apache2
     ```

### 2.3 Navigate to Default Root Directory
   - Change to the default root directory of Apache2:
     ```bash
     cd /var/www/html
     ```

### 2.4 Delete Default Index File
   - Remove the default `index.html` file from the directory:
     ```bash
     rm index.html
     ```

Now, your EC2 instance is set up with Apache2 installed and the default web page removed. You can proceed to deploy your Real-Time Attendance System on this instance. Customize the Apache2 configuration and upload your application files to the `/var/www/html` directory for hosting on the web server.
