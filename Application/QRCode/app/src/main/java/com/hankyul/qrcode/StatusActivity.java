package com.hankyul.qrcode;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.widget.Toast;
import android.widget.TextView;

import com.google.android.gms.tasks.OnFailureListener;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.IgnoreExtraProperties;
import com.google.firebase.database.ValueEventListener;
import com.hankyul.qrcode.ChargeStatus;

public class StatusActivity extends AppCompatActivity {
    private DatabaseReference mDatabase = FirebaseDatabase.getInstance().getReference();
    private TextView statusTextView;
    private TextView percentageTextView;
    private TextView voltageTextView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_status);
        statusTextView     = (TextView)findViewById(R.id.statusTextView);
        percentageTextView = (TextView)findViewById(R.id.percentageTextView);
        voltageTextView    = (TextView)findViewById(R.id.voltageTextView);
        readUser();
    }

    private void readUser() {
        mDatabase.child("charge_status").child("wc-robo:1").addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot snapshot) {
                // Get Post object and use the values to update the UI
                if(snapshot.getValue(ChargeStatus.class) != null){
                    ChargeStatus post = snapshot.getValue(ChargeStatus.class);
                    Toast.makeText(StatusActivity.this, "getData" + post.toString(), Toast.LENGTH_SHORT).show();
                    statusTextView.setText(post.getChargingStatus());
                    percentageTextView.setText(post.getChargePercentage() + '%');
                    voltageTextView.setText(post.getVoltageValue() + 'V');
                } else {
                    Toast.makeText(StatusActivity.this, "데이터 없음...", Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onCancelled(@NonNull DatabaseError error) {
                Toast.makeText(StatusActivity.this, "loadPost:onCancelled" + error.toException(), Toast.LENGTH_SHORT).show();
            }
        });
    }
}