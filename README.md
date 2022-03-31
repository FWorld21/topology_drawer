ABOUT		       

Script was builded for drawing network topology from file.
It can easily display all network connection, if it has a right
format. Example of topology, you can find into topologies dir, 
at the root of the project. On output you can get .graphml file.
This file can be opened by yEd Graph Editor program (Windows, Linux, Mac).
Link for download this program: https://www.yworks.com/products/yed/download#download


INSTRUCTION		

1. You need to clone this repository using this command:
		
		git clone https://github.com/FWorld21/topology_drawer.git

2. Go to the path of script by command:
		
		cd topology_drawer 

3. Don't forget to install all dependencies, by command:
		
		pip3 install -r requirements.txt
    
4. That's all! Now you can launch the script, using argument, to set path of topology:
		
		python3 main.py --file path/to/file



For launch help, use <b>--help</b> for script	
