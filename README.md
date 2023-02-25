# Indoor-Positioning-for-Smartphones
Final Year Project where the aim is to apply techniques to achieve viable indoor positioning (In the UCD O'Brien Science Centre) using a smartphone

The Core Objectives of the project are:

Using Wifi fingerprinting to estimate the phones location

Using the phone's inertial sensors to detect steps taken by the user as a form of Pedestrian Dead Reckoning to aid in tracking

Combining the above in a Particle Filter that has the potential to accurately simulate the user and track their position


Contents:

wifi is the folder where the project first started so there's a lot of junk there.

WifiGatherer is the android app for making the fingerprinting grid map.  (Offline phase)
  
InertialGatherer is the app where the user's acceleration data, rotational vector and wifi scans are collected. (Online Phase)
  
Inertial Data Processing is the processing of data for step detection

Particle Filter is the development of the particle filter and eventual integration of all the data.

Core is the integration of all 3 data processing parts. Wifi Prediction, Steps and particle filter
