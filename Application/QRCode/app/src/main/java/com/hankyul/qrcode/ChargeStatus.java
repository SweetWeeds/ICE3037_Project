package com.hankyul.qrcode;

import com.google.firebase.database.IgnoreExtraProperties;

@IgnoreExtraProperties
public class ChargeStatus {
    public String chargingStatus;
    public String chargePercentage;
    public String voltageValue;

    public ChargeStatus() {
        this.chargingStatus = "testing";
        this.chargePercentage = "testing";
        this.voltageValue = "testing";
    }

    public ChargeStatus(String chargingStatus, String chargePercentage, String voltageValue) {
        this.chargingStatus = chargingStatus;
        this.chargePercentage = chargePercentage;
        this.voltageValue = voltageValue;
    }

    public String getChargingStatus() {
        return chargingStatus;
    }

    public void setChargingStatus(String chargingStatus) {
        this.chargingStatus = chargingStatus;
    }

    public String getChargePercentage() {
        return chargePercentage;
    }

    public void setChargePercentage(String chargePercentage) {
        this.chargePercentage = chargePercentage;
    }

    public String getVoltageValue() {
        return voltageValue;
    }

    public void setVoltageValue(String voltageValue) {
        this.voltageValue = voltageValue;
    }

    @Override
    public String toString() {
        return "chargingStatus='" + chargingStatus + '\'' +
                "chargePercentage='" + chargePercentage + '\'' +
                "voltageValue='" + voltageValue + '\'' +
                '}';
    }
}
