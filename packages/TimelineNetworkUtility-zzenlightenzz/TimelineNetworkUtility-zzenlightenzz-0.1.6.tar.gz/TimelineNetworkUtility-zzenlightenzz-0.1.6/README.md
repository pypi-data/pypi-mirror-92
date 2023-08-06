# TimelineNetworkUtility

A TimelineNetworkUtility is a small library that composing of Timeline and Network utility function. The timeline can help to manage the execution step of function. The useful of timeline is to help the embedded device to handle the sequence of the data reading from sensor. Which prevented the exceeding of reading speed limit of the hardware. The network utility provided the simple to use of some network function. Which include normal POST, base64 image POST, and client listening (SSE).

# Usage

	import TimelineNetworkUtility as STLS
	import _thread as thread

	def interval_time():
    	pass;

	def off_able():
		print('excute off_able');
		STLS.StepEnable("off_able", False);

	def sensor1_read():
		print('read sensor1 data');

	def sensor2_read():
		print('read sensor2 data');

	def sensor_post():
		BodyP = {
	    	'data': 'post data'
	    };
	    status, data = STLS.SendPOST(BodyP, ServerIP + ":" + ServerPORT, "/PostData.php");
	    time = 15.0; # seconds
	    off_able_enable = True;
	    if not off_able_enable:
	        STLS.ChangeStepTime("interval_time", round(time*10/2));
	    else:
	        STLS.StepEnable("off_able", True);

	def image_post():
		BodyP = {
            "base64_image": base64_image
        };
		status, res = STLS.SendPOSTImage(BodyP, ServerIP + ":" + ServerPORT, "/PostImage.php");

	def listen_to_server(thread_name, delay):
	    try:
	        STLS.StartPYTHONListen(ServerIP, ServerPORT, image_post, "/PythonListen.php");
	    except KeyboardInterrupt:
	        print("^C received, shutting down the listen");

	try:
		thread.start_new_thread( listen_to_server, ("Thread-2", 2, ) );
	except:
		print("Error: unable to start listen thread");

	STLS.AddStep("interval_time", 25, interval_time, True);
	STLS.AddStep("sensor1_read", 1, sensor1_read, True);
	STLS.AddStep("sensor2_read", 1, sensor2_read, True);

	STLS.AddStep("sensor_post", 1, LocalOperate, True);
	STLS.AddStep("off_able", 30, off_able, False);
	STLS.AddStep("interval_time", 25, interval_time, True);

	STLS.EnableLoop(True);
	STLS.Start();
	STLS.Run();