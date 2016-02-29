Dependencies
	Base Python
	Python 2.7.11 x64 	https://www.python.org/downloads/release/python-2711/
						python-2.7.11.amd64
	
	Keyboard Emulation
	pywin32 x64 		http://sourceforge.net/projects/pywin32/files/pywin32/Build%20219/
						pywin32-219.win-amd64-py2.7
	
	Process Pausing
	psutil				C:\Python27\Scripts\easy_install.exe psutil
	
	IRC Connectivity Bot
	irc 				C:\Python27\Scripts\easy_install.exe irc
	
	Joystick Support
	vJoy				http://vjoystick.sourceforge.net/site/index.php/download-a-install/72-download
						vJoy_216_150815
	
Architecture
	Gui
		Build Config For Run
			Color
			Boxes
			Text Files
			Memory Reading
			
	
	Run	
		Read In Config
		Bot
			Sanitize
			Initialize Command for each chat
			Execute Command
			
	Command
		admin (bool)
		banned (bool)
		
		trigger
			Chat String
			
		type
			1 Chat - Default
			2 Key Command/Combo
			3 Mouse Command/Combo
			4 Joy Command/Combo
			5 Mode Command
			6 Admin Command
			
		Execute
			Combo.execute()
		
		Action
			Combo
				KeyAction (list)
					key
					Pause
					
				MouseAction (list)
					changex
					changey
					button (L R M)
					Pause
					
				JoyAction (list)
					button
					axis (ENUM X,Y,Z,Rx,Ry,Rz,Slider,Slider2)
					axispos
					hat (ENUM 1,2,3,4)
					hatpos 
					Pause
					
				ModeAction
					index (Modes)
					step (+ or -)
					
	Pause
		before
		during
		after	
		
	Modes (list)
		type (bool,int)
		posswitch
		negswitch
		max
		min
		init
		value
		ref
		innateloss
		onUpdate()
		
	Democracy
		enabled
		votes (list)
		timer
		delay
		pause
		
	Memory (list)
		address
		file
		display (bool)	

	Config
		Commands (list)
		Modes (list)
		Democracy
		Memory (list)
			