// node-red function node: normalize + decide
// inputs: mqtt-in nodes on ioe/zigbee/sensor, ioe/wifi/sensor, ioe/bluetooth/sensor
// output: connect to mqtt-out node (topic ioe/alert) and a debug node

const protocols = { zigbee: "Zigbee", wifi: "WiFi", bluetooth: "Bluetooth" };
const protocol = protocols[msg.topic.split("/")[1]];

let temperature;
if (typeof msg.payload === "object") {
    temperature = Number(msg.payload.temperature);              // {"temperature":30}
} else {
    temperature = Number(String(msg.payload).split(/[:=]/)[1]); // TEMP:28 / temperature=30 / T:27
}

msg.topic = "ioe/alert";
msg.payload = {
    status: temperature > 30 ? "WARNING" : "NORMAL",
    source: protocol,
    temperature: temperature,
};
return msg;
