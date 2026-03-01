package com.app.iot.service;

import com.app.iot.model.IoTDevice;
import com.app.iot.model.SensorData;
import com.app.iot.repository.DeviceRepository;
import com.app.iot.repository.SensorDataRepository;
import org.eclipse.paho.client.mqttv3.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import javax.annotation.PostConstruct;
import java.util.List;
import java.util.concurrent.ConcurrentHashMap;

@Service
public class IoTService implements MqttCallback {

    @Autowired
    private DeviceRepository deviceRepository;

    @Autowired
    private SensorDataRepository sensorDataRepository;

    @Value("${mqtt.broker.url}")
    private String brokerUrl;

    @Value("${mqtt.client.id}")
    private String clientId;

    @Value("${mqtt.username}")
    private String username;

    @Value("${mqtt.password}")
    private String password;

    private MqttClient mqttClient;
    private final ConcurrentHashMap<String, IoTDevice> connectedDevices = new ConcurrentHashMap<>();

    @PostConstruct
    public void init() {
        try {
            connectToBroker();
            subscribeToTopics();
        } catch (MqttException e) {
            throw new RuntimeException("Failed to initialize IoT service", e);
        }
    }

    private void connectToBroker() throws MqttException {
        mqttClient = new MqttClient(brokerUrl, clientId);
        MqttConnectOptions options = new MqttConnectOptions();
        options.setUserName(username);
        options.setPassword(password.toCharArray());
        options.setAutomaticReconnect(true);
        options.setCleanSession(true);
        mqttClient.connect(options);
        mqttClient.setCallback(this);
    }

    private void subscribeToTopics() throws MqttException {
        mqttClient.subscribe("devices/+/data");
        mqttClient.subscribe("devices/+/status");
    }

    @Override
    public void connectionLost(Throwable cause) {
        try {
            connectToBroker();
            subscribeToTopics();
        } catch (MqttException e) {
            throw new RuntimeException("Failed to reconnect to MQTT broker", e);
        }
    }

    @Override
    public void messageArrived(String topic, MqttMessage message) {
        String[] topicParts = topic.split("/");
        String deviceId = topicParts[1];
        String messageType = topicParts[2];

        if ("data".equals(messageType)) {
            processSensorData(deviceId, new String(message.getPayload()));
        } else if ("status".equals(messageType)) {
            processDeviceStatus(deviceId, new String(message.getPayload()));
        }
    }

    @Override
    public void deliveryComplete(IMqttDeliveryToken token) {
        // Handle message delivery confirmation if needed
    }

    private void processSensorData(String deviceId, String payload) {
        try {
            SensorData sensorData = parseSensorData(payload);
            sensorData.setDeviceId(deviceId);
            sensorDataRepository.save(sensorData);

            // Check for anomalies or alerts
            if (isAnomalyDetected(sensorData)) {
                sendAlert(deviceId, sensorData);
            }
        } catch (Exception e) {
            throw new RuntimeException("Failed to process sensor data", e);
        }
    }

    private void processDeviceStatus(String deviceId, String status) {
        IoTDevice device = deviceRepository.findById(deviceId)
            .orElseGet(() -> createNewDevice(deviceId));
        
        device.setStatus(status);
        device.setLastUpdated(System.currentTimeMillis());
        deviceRepository.save(device);
        
        if ("OFFLINE".equals(status)) {
            connectedDevices.remove(deviceId);
        } else {
            connectedDevices.put(deviceId, device);
        }
    }

    public void sendCommand(String deviceId, String command) throws MqttException {
        String topic = "devices/" + deviceId + "/command";
        MqttMessage message = new MqttMessage(command.getBytes());
        message.setQos(1);
        mqttClient.publish(topic, message);
    }

    public List<IoTDevice> getActiveDevices() {
        return deviceRepository.findByStatus("ONLINE");
    }

    public List<SensorData> getDeviceData(String deviceId, long startTime, long endTime) {
        return sensorDataRepository.findByDeviceIdAndTimestampBetween(deviceId, startTime, endTime);
    }

    private IoTDevice createNewDevice(String deviceId) {
        IoTDevice device = new IoTDevice();
        device.setId(deviceId);
        device.setStatus("UNKNOWN");
        return device;
    }

    private boolean isAnomalyDetected(SensorData sensorData) {
        // Implement anomaly detection logic
        return false;
    }

    private void sendAlert(String deviceId, SensorData sensorData) {
        // Implement alert notification logic
    }

    private SensorData parseSensorData(String payload) {
        // Implement sensor data parsing logic
        return new SensorData();
    }
}
