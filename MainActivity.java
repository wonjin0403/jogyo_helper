package com.bignerdranch.android.tahelper;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;

import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.net.SocketAddress;
import java.net.UnknownHostException;

public class MainActivity extends AppCompatActivity {

    private static Socket socket;
    private static TextView textview;
    private static OutputStream os = null ;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        textview = (TextView)findViewById(R.id.ConnectionText);

        try {
            socket = new Socket();
            SocketAddress addr = new InetSocketAddress("192.168.56.1", 35357/*port*/) ;
            socket.connect(addr);

            byte[] bufSnd = new byte[64];

            // TODO : fill bufSnd with data.
            bufSnd[0] = 0x00;
            bufSnd[1] = 0x11;
            bufSnd[15] = 0x0F;

            OutputStream os = socket.getOutputStream() ;
            os.write(bufSnd, 0/*off*/, 16/*len*/) ;

            textview.setText("Success");
            while(true) {

            }
        } catch (UnknownHostException e) {
            e.printStackTrace();
            Log.d("asdfasdfasdfasdf", "UnknownHostException");
        } catch (IOException e) {
            e.printStackTrace();
            Log.d("asdfasdfasdfasdf", "IO");
        }

        try {
            if (os != null)
                os.close();

            if (socket != null)
                socket.close() ;

            Log.d("CloseSocket", "aasdfjiosajfoaisdfjasiodfjaiosdjfoiasjfaiosdj");
        } catch (Exception e) {
            // TODO : process exceptions.
        }
    }
}