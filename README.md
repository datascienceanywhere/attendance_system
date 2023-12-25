### Deploy Real-Time Attendance System in <span style="color:orange">AWS EC2 Instance</span>

#### 1. Create EC2 Instance
1. Login in to AWS account (<https://aws.amazon.com/>)
2. Create instance **EC2**
    - Click on Launch Instance
    - Select **Ubuntu** os image
    - Instance type -> t2.micro
3. Connect to instance as ***root*** user.

#### 2. Setting the Instance
1. Update ubuntu instance
```bash
sudo apt-get update
```
2. Install and Configure Apache2

   Reference: https://ubuntu.com/tutorials/install-and-configure-apache#1-overview
```bash
sudo apt install apache2
```
