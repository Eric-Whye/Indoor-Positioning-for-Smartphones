package com.fyp.intertialgatherer;

import androidx.annotation.NonNull;
import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;

import android.Manifest;
import android.annotation.SuppressLint;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.pm.PackageManager;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.net.wifi.ScanResult;
import android.net.wifi.WifiInfo;
import android.net.wifi.WifiManager;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.View;
import android.view.animation.Animation;
import android.view.animation.RotateAnimation;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.jjoe64.graphview.GraphView;
import com.jjoe64.graphview.Viewport;
import com.jjoe64.graphview.series.DataPoint;
import com.jjoe64.graphview.series.LineGraphSeries;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.StringTokenizer;
import java.util.concurrent.ScheduledThreadPoolExecutor;
import java.util.concurrent.TimeUnit;

public class MainActivity extends AppCompatActivity{
    //Text view of Wifi data
    private TextView wifiTextView;

    //Text view of angle data
    private TextView angleTextView;

    //Compass image variable
    private ImageView compassImg;

    //Graph variables
    private int pointsPlotted=1;
    private final LineGraphSeries<DataPoint> series = new LineGraphSeries<DataPoint>(new DataPoint[] {
            new DataPoint(0, 0)
    });
    private Viewport viewport;

    //Sensors
    private SensorManager sensorManager;
    private Sensor accelerometer;
    private Sensor rotateSensor;

    //Wifi
    private WifiManager wifiManager;
    private WifiInfo wifiInfo;
    private boolean isWifiReady = false;
    private String currScan;

    //File I/O Related
    private String fileName = "data.csv";
    private String[] header = {"X", "Y", "Z", "Acceleration", "Heading", "Timestamp", "Wifi"};
    private boolean isRecordStart = false;
    private List<String[]> data = new ArrayList<>();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        handlePermissions(this,
                Manifest.permission.ACCESS_FINE_LOCATION,
                Manifest.permission.ACCESS_WIFI_STATE,
                Manifest.permission.CHANGE_WIFI_STATE);

        //Sensor Management
        sensorManager = (SensorManager) getSystemService(SENSOR_SERVICE);
        accelerometer = sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
        rotateSensor = sensorManager.getDefaultSensor(Sensor.TYPE_GAME_ROTATION_VECTOR);

        sensorManager.registerListener(sensorEventListener, accelerometer, SensorManager.SENSOR_DELAY_GAME);
        sensorManager.registerListener(sensorEventListener, rotateSensor, SensorManager.SENSOR_DELAY_GAME);



        //Acceleration Graph
        GraphView graph = (GraphView) findViewById(R.id.graph);
        viewport = graph.getViewport();
        viewport.setXAxisBoundsManual(true);
        viewport.setYAxisBoundsManual(true);
        viewport.setMaxY(10+20);
        viewport.setMinY(10-20);
        graph.addSeries(series);


        //Text view of Angle data
        angleTextView = findViewById(R.id.text_angle);

        //Compass Image
        compassImg = (ImageView) findViewById(R.id.compass);


        //Wifi Management
        wifiManager = (WifiManager) getSystemService(Context.WIFI_SERVICE);
        this.registerReceiver(new WifiScanReceiver(), new IntentFilter(WifiManager.SCAN_RESULTS_AVAILABLE_ACTION));
    }

    private final SensorEventListener sensorEventListener = new SensorEventListener() {
        float x;
        float y;
        float z;
        double acceleration;

        float[] values = new float[3];
        private float lastRotateDegree;

        @Override
        public void onSensorChanged(SensorEvent event) {
            if (event.sensor.getType() == Sensor.TYPE_ACCELEROMETER) {

                //Extract axis from acceleration
                x = event.values[0];
                y = event.values[1];
                z = event.values[2];
                acceleration = Math.sqrt(x*x + y*y + z*z);

                //update graph
                pointsPlotted++;
                if (pointsPlotted > 1000) {
                    pointsPlotted = 1;
                    series.resetData(new DataPoint[] {new DataPoint(pointsPlotted, acceleration)});
                } else
                    series.appendData(new DataPoint(pointsPlotted, acceleration), true, pointsPlotted);
                viewport.setMaxX(pointsPlotted);
                viewport.setMinX(pointsPlotted-200);


            }
            else if (event.sensor.getType() == Sensor.TYPE_GAME_ROTATION_VECTOR) {

                float[] R = new float[9];
                values = new float[3];
                SensorManager.getRotationMatrixFromVector(R, event.values);
                SensorManager.getOrientation(R, values);
                Log.d("MainActivity", "value[0] is " + Math.toDegrees(values[0]));
                float rotateDegree = -(float) Math.toDegrees(values[0]);
                if (Math.abs(rotateDegree - lastRotateDegree) > 1) {
                    RotateAnimation animation = new RotateAnimation(
                            lastRotateDegree, rotateDegree, Animation.RELATIVE_TO_SELF, 0.5f, Animation.RELATIVE_TO_SELF, 0.5f);
                    animation.setFillAfter(true);
                    compassImg.startAnimation(animation);
                    lastRotateDegree = rotateDegree;
                }

                angleTextView.setText(String.format("%.3f", rotateDegree));

                //Record Sensor Data when activated
                if (isRecordStart) {
                    String[] line;
                    if (isWifiReady){
                        scan();
                        line = new String[]{String.valueOf(x), String.valueOf(y), String.valueOf(z),
                                String.valueOf(acceleration), String.valueOf(Math.toDegrees(values[0])), String.valueOf(event.timestamp),
                        currScan};
                        isWifiReady = false;
                    } else {
                        line = new String[]{String.valueOf(x), String.valueOf(y), String.valueOf(z),
                                String.valueOf(acceleration), String.valueOf(Math.toDegrees(values[0])), String.valueOf(event.timestamp),
                                ""};
                    }
                    data.add(line);


                }
            }
        }

        @Override
        public void onAccuracyChanged(Sensor sensor, int i) {
        }


    };

    public void calibrate(View v){
        sensorManager.unregisterListener(sensorEventListener, rotateSensor);
        sensorManager.registerListener(sensorEventListener, rotateSensor, SensorManager.SENSOR_DELAY_GAME);
    }

    public void startRec(View v){
        if (isRecordStart){
            Toast.makeText(this, "Recording Already Started", Toast.LENGTH_SHORT).show();
            return;
        }
        isRecordStart = true;
        ScheduledThreadPoolExecutor exec = new ScheduledThreadPoolExecutor(2);
        exec.scheduleAtFixedRate(new Runnable() {
            public void run() {
                isWifiReady = true;
            }
        }, 1, 4, TimeUnit.SECONDS); // execute every 60 seconds
        Toast.makeText(this, "Data Recording Started", Toast.LENGTH_SHORT).show();
    }

    public void endRec(View v){
        if (!isRecordStart){
            Toast.makeText(this, "No Data Recorded", Toast.LENGTH_SHORT).show();
            return;
        }
        File path = getApplicationContext().getFilesDir();
        try {
            FileOutputStream writer = openFileOutput(fileName, MODE_PRIVATE);
            StringBuilder content = new StringBuilder(String.join(",", header)).append("\n");

            for (int i = 0; i < data.size(); i++){
                String line = String.join(",", data.get(i));
                content.append(line).append("\n");
            }
            writer.write(content.toString().getBytes());
            Toast.makeText(this, "Data saved to " + path + "/" + fileName, Toast.LENGTH_LONG).show();

            writer.close();
        } catch (IOException e) {e.printStackTrace();}

        isRecordStart = false;
        data.clear();
    }



    public void scan() {
        if (isRecordStart)
            wifiManager.startScan();
    }

    class WifiScanReceiver extends BroadcastReceiver {
        private String delim = " ";
        @Override
        public void onReceive(Context context, Intent intent) {
            if (intent.getBooleanExtra(WifiManager.EXTRA_RESULTS_UPDATED, false)) {
                StringBuilder stringBuilder = new StringBuilder();


                for (ScanResult result : wifiManager.getScanResults()){
                    //Handle edge cases where SSID contains whitespace or is null
                    String ssid = result.SSID;
                    if (ssid==null || ssid.equals("")) ssid = "NOSSID";
                    if (ssid.contains(" ")) ssid = ssid.replaceAll(" ", "");

                    int rssi = result.level;
                    stringBuilder.append(ssid + delim + result.BSSID + delim + rssi + delim);
                }
                currScan = stringBuilder.toString();
            }
        }
    }


    
    @Override
    protected void onPause() {
        super.onPause();
    }

    @Override
    protected void onResume(){
        super.onResume();
    }

    public void handlePermissions(Context context, String... permissions){
        if (context != null && permissions != null) {
            for (String permission : permissions) {
                if (ActivityCompat.checkSelfPermission(context, permission) != PackageManager.PERMISSION_GRANTED) {
                    ActivityCompat.requestPermissions(this, permissions, 1);
                    return;
                }
            }
        }
    }
}