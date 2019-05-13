###########################################################
# File: README.txt
# Author: Howard Nathanson
#         Full Stack Nanodegree - project 1
# History: 05/10/2019 - Initial Version


Overview:
---------
The programs will produce 3 Log Anaylsis reports as defined by the clients. The files consist of 2 python modules, using python3, as described below. 

The logsanalysis (logs analysis) folder contains all the files required to maintain the webpage and the reports. The folder contains:

	* loganalysis.py - main python file containing the main() and the code to produce the report displayed in the terminmal window in plain text format. 
	* loganalysisdb.py - python file containing the PostgreSQL code. There is 1 function for each report being produced.

The reports connect to the "news" database and the "articles", "authors", and "log" tables. 

Pre-Requisites:
---------------
To execute and maintain these reports, you need the following:

1) (optional) Code Repository
A Git repository is not required but suggested for this project. Git can be downloaded from https://git-scm.com/downloads.

2) Terminal Emulation program
This project used Git Bash which was included in the Git download. Git Bash can be downloaded from https://git-scm.com/downloads.

3) Virtual Machine Host
This project used Oracle VM VirtualBox. The software can be downloaded from https://www.virtualbox.org/wiki/Downloads.

4) Virtual Machine Command Line Utility
This project used HashiCorp Vagrant as the virtual box command line utility when accessing the virtual machine. The software can be downloaded from https://www.vagrantup.com/downloads.html. 

5) Python
This project is coded in Python. Python will be loaded during the setup using Vagrant. The installion is defined for Python2 and Python3 in the Vagrantfile file.

6) ProgreSQL
ProgreSQL is the relational database management system to store the data. PostgreSQL will be loaded during the setup using Vagrant. The installation is defined in the Vagrantfile file.

7) news Database Setup File
The newsdata.zip file contains the database table definitions and data used for this project. If the file is zipped, extact the file directly into the vagrant directory. 

Setup Environment:
------------------
Once the software was installed, the configuration of the project directories and the Vagrantfile used was obtained by forking then cloning the fullstack-nanodegree-vm Git repository, accessed on the github.com website: https://github.com/udacity/fullstack-nanodegree-vm.

From within your terminal emulator, go to the directory where this respository resides. All of the activity will occur within the vagrant. The Vagrantfile file contains the setups including the name of the virtual machine in the config.vm.box assignment. You can change this to the box of your choosing. The box used for this project was based upon research and trial-and-error. Your choice can be different. 

Staying in the vagrant directory, start the VM VirtualBox and run the configurations defined within the Vagrantfile file. At the command prompt, type

	vagrant up

If this is the first time you are running this, it may take several minutes to complete. NOTE: There is no default server URL defined in the Vagrantfile. To get vagrant up to work for me, I needed to add the following line to define one to allow vagrant to know where to find the software needed. This line get inserted at the top of the Vagrant file.

Vagrant::DEFAULT_SERVER_URL.replace('https://vagrantcloud.com')

NOTE: Upon successful completion, the VM VirtualMachine will be started.


The last step to setup your environment will be to initiate the Vagrant secure shell interface. This will allow you to execute the psql and python commands to test your coding and run the project. To start the SSH session, type

	vagrant ssh

Upon successful completion, change the directory to /vagrant/logsanalysis. The project files will be resident in this directory. From here, create the database tables and data by typing

	psql -d news -f newsdata.sql

The VM VirtualBox is running, the SSH session started, and the database tables and data are created. You are now ready to view, updated, and execute the project.

Execution:
----------
The program was developed and tested to run within a Vagrant Virtual Machine, SSH terminal, from the Vagrant SSH command line. To access the project folder, go to the /vagrant/logsanalysis folder. To start the project, run:

	python loganalysis_txt.py or python3 loganalysis_txt.py depending on the version of Python used.

This will generate the reports in your active SSH terminal. 

Output:
-------
Each report will be displayed with a header and the details listed in the SSH terminal in plain text.


End Session:
------------
To end the SSH session, type "exit". This will bring you back to the command line in your terminal emulator but leave the VM VirtualBox active. To turn off the box, you can run one of the following
	* vagrant suspend - wil stop the VM from running, saving its current state
	* vagrant halt - will shut down and power off the VM
	* vagrant destroy - will shout down and removed the VM
NOTE: To restart the VM, type vagrant up.


