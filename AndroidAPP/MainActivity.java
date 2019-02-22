package com.sqyon.sensor.sensordatacollection;

import android.Manifest;
import android.annotation.SuppressLint;
import android.app.Activity;
import android.content.Context;
import android.content.pm.ActivityInfo;
import android.content.pm.PackageManager;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Bundle;
import android.os.Environment;
import android.os.Handler;
import android.os.Looper;
import android.os.Message;
import android.view.View;
import android.widget.EditText;
import android.widget.Switch;
import android.widget.TextView;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.math.BigDecimal;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.net.UnknownHostException;

public class MainActivity extends Activity implements SensorEventListener {
    private SensorManager mSensorManager;
    private Sensor mAcc;
    private TextView tv_accX, tv_accX2, tv_accX3;
    private TextView tv_accY, tv_accY2, tv_accY3;
//    private TextView tv_a, tv_av, tv_ah;
    private TextView tv_datasize;
    private TextView tv_result, tv_resule2;
    private UDPClient client = null;
    private Boolean filedel = false;
    private Boolean writable = false;
    private SensorData senserData = new SensorData();
    private String savepath = "", filename = "sensordata.json";
    @SuppressLint("HandlerLeak")
    private Handler handler = new Handler() {
        public void handleMessage(Message msg) {
            if (msg.what == 2) {
                tv_result.setText((String) msg.obj);
            }
        }
    };

    public static String HumanReadableFilesize(double size) {
        double kiloByte = size / 1024;
        if (kiloByte < 1) {
            return size + "B";
        }

        double megaByte = kiloByte / 1024;
        if (megaByte < 1) {
            BigDecimal result1 = new BigDecimal(Double.toString(kiloByte));
            return result1.setScale(2, BigDecimal.ROUND_HALF_UP).toPlainString() + "KB";
        }

        double gigaByte = megaByte / 1024;
        if (gigaByte < 1) {
            BigDecimal result2 = new BigDecimal(Double.toString(megaByte));
            return result2.setScale(2, BigDecimal.ROUND_HALF_UP).toPlainString() + "MB";
        }

        double teraBytes = gigaByte / 1024;
        if (teraBytes < 1) {
            BigDecimal result3 = new BigDecimal(Double.toString(gigaByte));
            return result3.setScale(2, BigDecimal.ROUND_HALF_UP).toPlainString() + "GB";
        }
        BigDecimal result4 = new BigDecimal(teraBytes);
        return result4.setScale(2, BigDecimal.ROUND_HALF_UP).toPlainString() + "TB";
    }

    public void WritalbeSwitch(View view) {
        writable = ((Switch) view).isChecked();
//		EditText t = (EditText) findViewById(R.id.FileName);
//		filename = t.getText().toString() + ".json";
    }

    public void SelectFile(View view) {
        EditText t = (EditText) findViewById(R.id.FileName);
        filename = t.getText().toString() + ".json";
        tv_resule2.setText("已选择文件" + filename);
    }

    private void init() {
        // 为重力传感器注册监听器
        mSensorManager.registerListener(this, mSensorManager
                .getDefaultSensor(Sensor.TYPE_GRAVITY), SensorManager
                .SENSOR_DELAY_GAME);
        // 为线性加速度传感器注册监听器
        mSensorManager.registerListener(this, mSensorManager
                        .getDefaultSensor(Sensor
                                .TYPE_ACCELEROMETER),
                SensorManager.SENSOR_DELAY_GAME);
    }

    private void datasave() {
        for (boolean i : senserData.vis)
            if (!i)
                return;
        senserData.calc();
//        tv_a.setText(Float.toString(senserData.a));
//        tv_av.setText(Float.toString(senserData.av));
//        tv_ah.setText(Float.toString(senserData.ah));
        netwrite();
        if (checkSelfPermission(Manifest.permission.WRITE_EXTERNAL_STORAGE) != PackageManager
                .PERMISSION_GRANTED)
            requestPermissions(new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE}, 1);
        if (writable)
            write();
        senserData = new SensorData();
    }

    @Override
    public void onSensorChanged(SensorEvent event) {
        if (event.sensor.getType() == Sensor.TYPE_ACCELEROMETER) {
            float accValues[] = event.values.clone();
            synchronized (senserData) {
//                if (senserData.vis[0])
//                    return;
                senserData.datatype = "TYPE_ACCELEROMETER";
                senserData.ti[0] = System.currentTimeMillis();
                senserData.val[0] = accValues;
                senserData.vis[0] = true;
                tv_accX.setText(String.valueOf(senserData.val[0][0]));
                tv_accX2.setText(String.valueOf(senserData.val[0][1]));
                tv_accX3.setText(String.valueOf(senserData.val[0][2]));
            }
        } else if (event.sensor.getType() == Sensor.TYPE_GRAVITY) {
            float[] gyrValues = event.values.clone();
            synchronized (senserData) {
//                if (senserData.vis[1])
//                    return;
                senserData.datatype = "TYPE_GRAVITY";
                senserData.ti[1] = System.currentTimeMillis();
                senserData.val[1] = gyrValues;
                senserData.vis[1] = true;
                tv_accY.setText(String.valueOf(senserData.val[1][0]));
                tv_accY2.setText(String.valueOf(senserData.val[1][1]));
                tv_accY3.setText(String.valueOf(senserData.val[1][2]));
            }
        } else return;
        datasave();
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int i) {

    }

    private void netwrite() {
        if (client != null) {
            client.sendMessageThroughUDP(MakeJson());
        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
        mSensorManager = (SensorManager) getSystemService(Context
                .SENSOR_SERVICE);
        mAcc = mSensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
        tv_accX = findViewById(R.id.accX);
        tv_accX2 = findViewById(R.id.accX2);
        tv_accX3 = findViewById(R.id.accX3);
        tv_accY = findViewById(R.id.accY);
        tv_accY2 = findViewById(R.id.accY2);
        tv_accY3 = findViewById(R.id.accY3);
        tv_datasize = findViewById(R.id.datasize);
        tv_result = findViewById(R.id.result);
        tv_resule2 = findViewById(R.id.result2);
//        tv_a = findViewById(R.id.valueA);
//        tv_av = findViewById(R.id.valueAV);
//        tv_ah = findViewById(R.id.valueAH);
        File file = new File(Environment
                .getExternalStorageDirectory() +
                File.separator + savepath + File.separator +
                filename);
        tv_datasize.setText(HumanReadableFilesize(file.length()));
    }

    @Override
    protected void onResume() {
        super.onResume();
        init();
    }

    @Override
    protected void onPause() {
        super.onPause();
    }

    public void delfile(View view) {
        File file = new File(Environment
                .getExternalStorageDirectory() +
                File.separator + savepath + File.separator +
                filename);
        file.delete();
        tv_datasize.setText(HumanReadableFilesize(file.length()));
        tv_resule2.setText("已经删除文件" + filename);
    }

    public void setUdpIpAndPort(View view) {
        tv_result.setText("正在连接至服务器");
        EditText inputIp = (EditText) findViewById(R.id.input_ip);
        EditText inputPort = (EditText) findViewById(R.id.input_port);
        String ip = inputIp.getText().toString();
        String port = inputPort.getText().toString();
        client = new UDPClient(ip, port);
    }

    private String MakeJson() {
        //time,ax,ay,az,gx,gy,gz,a,av,ah
        String ret = "";
        ret += Long.toString(senserData.avet);
        for (float[] i : senserData.val)
            for (float j : i)
                ret += "," + Float.toString(j);

//        ret += Float.toString(senserData.a) + "," + Float.toString(senserData.av) + "," + Float
//                .toString(senserData.ah);
        return ret;
    }

    private boolean write() {
        if (filedel)
            return false;
        BufferedWriter out = null;
        try {
            if (Environment.getExternalStorageState().equals(Environment
                    .MEDIA_MOUNTED)) {

                String conent = MakeJson();
                File file = new File(Environment
                        .getExternalStorageDirectory() +
                        File.separator + savepath + File.separator +
                        filename);

                tv_datasize.setText(HumanReadableFilesize(file.length()));
                if (!file.getParentFile().exists()) {
                    file.getParentFile().mkdirs();
                }
                try {
                    FileOutputStream fo = new FileOutputStream(file,
                            true);
                    OutputStreamWriter ow = new OutputStreamWriter(fo);
                    out = new BufferedWriter(ow);
                    out.write(conent);
                    tv_resule2.setText("正在写入:" + filename);
                } catch (FileNotFoundException e) {
                    e.printStackTrace();
                } finally {
                    if (out != null)
                        out.close();
                }
                return true;
            } else
                return false;
        } catch (Exception e) {
            e.printStackTrace();
        }
        return false;
    }

    public class UDPClient {
        private int BIND_PORT = 20120;
        private DatagramSocket sendSock;
        private InetAddress inetAddress = null;
        private Integer targetPort;
        private SendThread sendThread;
        private RcvThread rcvThread = null;
        private Boolean exit = false;

        public UDPClient(String targetIp, String port) {
            if (rcvThread == null)
                rcvThread = new RcvThread();
            try {
                rcvThread.start();
            } catch (Exception e) {
                e.printStackTrace();
            }
            try {
                inetAddress = InetAddress.getByName(targetIp);
                targetPort = Integer.parseInt(port);
                sendSock = new DatagramSocket();

            } catch (UnknownHostException e) {
                e.printStackTrace();
                System.out.println("==========未知host===============");
            } catch (SocketException e) {
                e.printStackTrace();
                System.out.println
                        ("==========socket初始化异常===============");
            }
            sendThread = new SendThread();
            sendThread.start();

        }

        public void sendMessageThroughUDP(String pureMsg) {
            if (exit)
                return;
            Message msg = Message.obtain();
            msg.obj = pureMsg.getBytes();
            msg.what = 1;
            if (sendThread != null) {
                // 把 msg 传给 SendThread 的 handler
                sendThread.mHandler.sendMessage(msg);
            }
        }

        private class SendThread extends Thread {
            Handler mHandler;

            @SuppressLint("HandlerLeak")
            @Override
            public void run() {
                if (exit)
                    return;
                Looper.prepare();
                if (exit)
                    return;
                mHandler = new Handler() {
                    @Override
                    public void handleMessage(Message msg) {
                        try {
                            byte[] buf = (byte[]) msg.obj;
                            sendSock.send(new DatagramPacket(buf, buf
                                    .length, inetAddress, targetPort));
                        } catch (IOException e) {
                            e.printStackTrace();
                        }
                    }
                };
                Looper.loop();
            }
        }

        private class RcvThread extends Thread {
            private DatagramSocket rcvSock;

            @Override
            public void run() {
                if (exit)
                    return;
                try {
                    rcvSock = new DatagramSocket(BIND_PORT);
                } catch (SocketException e) {
                    e.printStackTrace();
                }

                while (true) {
                    if (exit)
                        return;
                    byte[] buf = new byte[1024];
                    DatagramPacket pkt = new DatagramPacket(buf, buf
                            .length);

                    try {
                        rcvSock.receive(pkt);
                    } catch (IOException e) {
                        e.printStackTrace();
                    }

                    String receivedMsg = new String(buf, 0, pkt.getLength
                            ());

                    //接下来送到UI线程去更新UI
                    Message msg = Message.obtain();
                    msg.what = 2;
                    msg.obj = receivedMsg;
                    handler.sendMessage(msg);
                }
            }
        }
    }
}
