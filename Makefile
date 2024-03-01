open-chrome:
	mkdir -p chrome_sessions
	/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=21220  --user-data-dir=./chrome_sessions/chrome_user_0
