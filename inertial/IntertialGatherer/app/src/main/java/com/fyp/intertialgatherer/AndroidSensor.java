package com.fyp.intertialgatherer;

import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;

import java.util.List;

public class AndroidSensor implements SensorEventListener {
    private List<Float> values;

    public AndroidSensor(int sensorFeature){

    }

    @Override
    public void onSensorChanged(SensorEvent sensorEvent) {

    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int i) {

    }
}
