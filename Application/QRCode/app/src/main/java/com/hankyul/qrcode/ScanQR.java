package com.hankyul.qrcode;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.widget.Toast;

import com.google.android.gms.tasks.OnFailureListener;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.IgnoreExtraProperties;
import com.google.zxing.integration.android.IntentIntegrator;
import com.google.zxing.integration.android.IntentResult;


public class ScanQR extends AppCompatActivity {
    private IntentIntegrator qrScan;
    private DatabaseReference mDatabase = FirebaseDatabase.getInstance().getReference();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        //new IntentIntegrator(this).initiateScan();
        qrScan = new IntentIntegrator(this);
        qrScan.setOrientationLocked(false);
        qrScan.initiateScan();
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        IntentResult result = IntentIntegrator.parseActivityResult(requestCode, resultCode, data);

        if (result != null) {
            if (result.getContents() == null) {
                Toast.makeText(this, "취소되었습니다.", Toast.LENGTH_LONG).show();
                this.finish();
            } else {
                Toast.makeText(this, "스캔했습니다: " + result.getContents(), Toast.LENGTH_LONG).show();
                this.sendRequest("wc-robo:1", result.getContents());
                Intent intent = new Intent(ScanQR.this, StatusActivity.class);
                startActivity(intent);
                //this.finish();
            }
        } else {
            super.onActivityResult(requestCode, resultCode, data);
        }
    }

    protected void sendRequest(String targetDev, String targetPlaceId) {
        mDatabase.child("charge_request").child(targetDev).setValue(targetPlaceId)
                .addOnSuccessListener(new OnSuccessListener<Void>() {
                    @Override
                    public void onSuccess(Void unused) {
                        Toast.makeText(ScanQR.this, "요청에 성공했습니다.", Toast.LENGTH_SHORT).show();
                    }
                })
                .addOnFailureListener(new OnFailureListener() {
                    @Override
                    public void onFailure(@NonNull Exception e) {
                        Toast.makeText(ScanQR.this, "요청에 실패했습니다.", Toast.LENGTH_SHORT).show();
                    }
                });
    }
}
