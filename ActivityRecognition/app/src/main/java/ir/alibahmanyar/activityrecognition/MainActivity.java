package ir.alibahmanyar.activityrecognition;

import android.content.Context;
import android.content.Intent;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.AsyncTask;
import android.provider.Telephony;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.speech.tts.TextToSpeech;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import java.util.List;
import java.util.Locale;
import java.util.Objects;

import android.widget.TextView;


public class MainActivity extends ActionBarActivity implements SensorEventListener{
    private SensorManager senSensorManager;
    private Sensor senAccelerometer;
    private TCPClient mTcpClient;
    TextToSpeech t1;
    String lastactivity = "How are you today?";
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);


        senSensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);
        senAccelerometer = senSensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
        senSensorManager.registerListener(this, senAccelerometer, SensorManager.SENSOR_DELAY_NORMAL);

        t1=new TextToSpeech(getApplicationContext(), new TextToSpeech.OnInitListener() {
            @Override
            public void onInit(int status) {
                if(status != TextToSpeech.ERROR) {
                   t1.setLanguage(Locale.US);


                }
            }
        });
        new connectTask().execute("");
    }
    @Override
    protected void onRestart() {

        new connectTask().execute("");

        senSensorManager.registerListener(this, senAccelerometer, SensorManager.SENSOR_DELAY_NORMAL);
        Button btn =(Button) findViewById(R.id.startstopbtn);
        btn.setText("STOP");

        super.onResume();
    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }
    public void reconnectbtn(View v){
        mTcpClient.stopClient();
        new connectTask().execute("");
        senSensorManager.unregisterListener(this);
        senSensorManager.registerListener(this, senAccelerometer, SensorManager.SENSOR_DELAY_NORMAL);
        Button btn =(Button) findViewById(R.id.startstopbtn);
        btn.setText("STOP");

    }
    public void startstopbtn(View v){
        Button btn =(Button) findViewById(R.id.startstopbtn);

        if (Objects.equals(btn.getText().toString(), "STOP")){
            btn.setText("START");
            senSensorManager.unregisterListener(this);
            mTcpClient.stopClient();
//            Log.d("HI", "Stopped");

        }
        else if (Objects.equals(btn.getText().toString(), "START")){
            btn.setText("STOP");
            senSensorManager.registerListener(this, senAccelerometer, SensorManager.SENSOR_DELAY_NORMAL);
            new connectTask().execute("");
//            Log.d("HI", "Started");



        }

    }
    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            Intent intent = new Intent(this, SettingsActivity.class);
            startActivity(intent);
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    @Override
    public void onSensorChanged(SensorEvent event) {
        Sensor mySensor = event.sensor;
        // Log.wtf("MyActivity", "wtf!");
        if (mySensor.getType() == Sensor.TYPE_ACCELEROMETER) {
            float x = event.values[0];
            float y = event.values[1];
            float z = event.values[2];
            String xs = Float.toString(x);
            String ys = Float.toString(y);
            String zs = Float.toString(z);
            TextView xtextview = (TextView)findViewById(R.id.x);
            xtextview.setText("X: "+xs);


            TextView ytextview = (TextView)findViewById(R.id.y);
            ytextview.setText("Y: "+ys);


            TextView ztextview = (TextView)findViewById(R.id.z);
            ztextview.setText("Z: "+zs);
            String msg = '|'+xs+'|'+ys+'|'+zs+'|';
            if (mTcpClient != null) {
                mTcpClient.sendMessage(msg);
            }

        }





    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {

    }
    @Override
    protected void onStop() {
        super.onStop();
        senSensorManager.unregisterListener(this);
        mTcpClient.stopClient();
        Log.d("Activity", "activity Stopped");
    }


    public class connectTask extends AsyncTask<String,String,TCPClient> {

        @Override
        protected TCPClient doInBackground(String... message) {

            //we create a TCPClient object and
            mTcpClient = new TCPClient(new TCPClient.OnMessageReceived() {
                @Override
                //here the messageReceived method is implemented
                public void messageReceived(String message) {
                    //this method calls the onProgressUpdate
                    publishProgress(message);
                }
            });
            mTcpClient.run();

            return null;
        }
        @Override
        protected void onProgressUpdate(String... values) {
            super.onProgressUpdate(values);
//            Log.d("HI", "Bye!");
            TextView activitytextview = (TextView)findViewById(R.id.activitytext);
            activitytextview.setText(values[0]);


            lastactivity=values[0];

           int a=t1.speak(values[0].toString(), TextToSpeech.QUEUE_ADD, null, "Activity");

            String asa = Integer.toString(a);
            Log.d("tts", asa);


        }

    }




}
