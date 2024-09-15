start:
	sudo python main.py

other-start:
	sudo python other_device.py

bl-start:
	sudo systemctl start bluetooth

bl-stop:
	sudo systemctl stop bluetooth

bl-restart:
	sudo systemctl restart bluetooth