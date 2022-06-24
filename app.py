from flask import Flask, request

import sys
import time
import random
import paho.mqtt.client as mqtt
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context
# MQTT parameters
MQTT_HOST = "www.lingjacksmart.com"
MQTT_PORT = 8883
MQTT_USERNAME = ""
MQTT_PASSWORD = ""
MQTT_USE_TLS = True
MQTT_TLS_ALLOW_SELF_SIGNED_CERT=True
MQTT_TLS_CA_FILE = "C:/Users/John Paul D Dala/Documents/project files/lingjack/mqttgatewayProject/mqttkeys_sample/ca.pem"
MQTT_TLS_CLIENT_CERT_FILE = "C:/Users/John Paul D Dala/Documents/project files/lingjack/mqttgatewayProject/mqttkeys_sample/client.pem"
MQTT_TLS_CLIENT_CERT_KEY_FILE = "C:/Users/John Paul D Dala/Documents/project files/lingjack/mqttgatewayProject/mqttkeys_sample/clientkey.pem"

# Other parameters
MESSAGE_SEND_INTERVAL = 30.0    # Seconds
SHOW_GATEWAY_AND_SINK = True
GATEWAY_ID = "1"     # TODO: Query gateways and sinks
SINK_ID = "sink1"

# Import Protocol Buffers message classes
sys.path.insert(0, "proto-py")
import generic_message_pb2 as generic_message
import wp_global_pb2 as wp_global
import data_message_pb2 as data_message

app = Flask(__name__)

def on_connect(client, userdata, flags, rc):
    '''Connection callback'''

    print("connected with result code %s, flags: %s" % (rc, flags))

    # Subscribe to topic "gw-event/received_data/#" to receive data packets.
    # The MQTT topics are documented in WP-RM-123 – WNT Gateway to Backend
    # Interface.
    #
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed
    client.subscribe("gw-event/received_data/#")
    client.subscribe("gw-request/send_data/#")
    client.subscribe("gw-response/send_data/#")


def on_disconnect(client, userdata, rc):
    '''Disconnection callback'''

    print("disconnected with result code %s" % rc)


def on_message(client, userdata, mqtt_msg):
    '''MQTT message callback'''
    # print("message on topic %s: '%s'" % (mqtt_msg.topic, mqtt_msg.payload))
    if mqtt_msg.topic.startswith("gw-event/received_data/"):
        # print(mqtt_msg.payload)
        # Wirepas Mesh data packet, parse bytes to a Protocol Buffers message
        proto_msg = generic_message.GenericMessage()
        proto_msg.ParseFromString(mqtt_msg.payload)
        recv_packet = proto_msg.wirepas.packet_received_event

        if SHOW_GATEWAY_AND_SINK:
            print('data packet from gateway "%s", sink "%s"' %
                  (recv_packet.header.gw_id, recv_packet.header.sink_id))

        if (recv_packet.source_endpoint == 240 and
            recv_packet.destination_endpoint == 255):
            # Remote API response packet
            print("remote API response from %d, travel time: %.3f s" %
                  (recv_packet.source_address,
                   recv_packet.travel_time_ms / 1000.0))
        else:
            # Some other data packet
            #network_address = str(hex(recv_packet.source_address)).replace("0x","")
            nodeid = str(hex(recv_packet.source_address)).replace("0x","")
            data = str(recv_packet.payload).replace("b'","").replace("'","")
            print("data from %s: %d bytes, travel time: %.3f s, "
                  "source, dest ep: %d, %d | Data: [%s]" %
                  (nodeid,
                   len(recv_packet.payload),
                   recv_packet.travel_time_ms / 1000.0,
                   recv_packet.source_endpoint,
                   recv_packet.destination_endpoint,
                   data))
                   
    # elif mqtt_msg.topic.startswith("gw-response/send_data/"):
        
    #     proto_msg = generic_message.GenericMessage()
    #     proto_msg.ParseFromString(mqtt_msg.payload)
    #     recv_packet = proto_msg.wirepas.packet_received_event

    else:
        # Something else, print it as is
        print("message on topic %s: '%s'" % (mqtt_msg.topic, mqtt_msg.payload))

def send_remote_api_ping(client, gw_id, sink_id, payload):
    '''Message send function'''

    print("sending data to %s:%s, broadcast | Payload: %s" % (gw_id, sink_id, payload)) 

    # Create an empty GenericMessage()
    proto_msg = generic_message.GenericMessage()

    # Fill out the message fields. WirepasMessage()
    # and SendPacketReq() are created automatically
    sp_req = proto_msg.wirepas.send_packet_req
    sp_req.header.req_id = (
        random.randint(0, 2 ** 48))             # At least 48 bits of randomness
    sp_req.header.sink_id = sink_id
    sp_req.destination_address = int(payload['NodeID'], 16)     # Broadcast
    sp_req.source_endpoint = int(payload['System']) #6                 # Wirepas reserved
    sp_req.destination_endpoint = int(payload['EP']) #100           # Remote API
    sp_req.qos = 1                              # Normal QoS
    sp_req.payload = str.encode(payload['Data'])                # Empty Remote API Ping request \x00\x00

    # Convert Protocol Buffers message to bytes
    payload = proto_msg.SerializeToString()

    # Publish MQTT message to the given gateway and sink
    client.publish("gw-request/send_data/%s/%s" % (gw_id, sink_id), payload)


def get_node_data(node):
    
    return node


@app.route('/protobuf', methods= ['POST', 'GET'])
def index():
    # TODO: Query gateways and sinks with a GetConfigsReq message
    gateways_and_sinks = {GATEWAY_ID: [SINK_ID], "1": ["sink1"], "5": ["sink1"]}
    data = request.get_json()

    # for val in data['payload']:
    #     print(val)

    for gw in data['gateways']:    
        for payload in data['payload']:
            send_remote_api_ping(client, gw['GatewayID'], ("sink"+gw['SinkID']), payload)

        # print(gw_id['NetworkID'])
    # print(testData)
    # print("running main loop... %s", data['payload'])

    # for gw_id in gateways_and_sinks:
    #     for sink_id in gateways_and_sinks[gw_id]:
    #         send_remote_api_ping(client, gw_id, sink_id)

    # send_remote_api_ping(client, gw_id, sink_id)
    return "Successfully send"


if __name__ == "__main__":

    # print(wni.get_gateways())

    client = mqtt.Client(clean_session = True)
    client.enable_logger()  # Show exceptions in callbacks 
    # client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    if MQTT_USE_TLS:
        # Turn on SSL/TLS support for MQTT connection
        client.tls_set(ca_certs=MQTT_TLS_CA_FILE, certfile=MQTT_TLS_CLIENT_CERT_FILE, keyfile=MQTT_TLS_CLIENT_CERT_KEY_FILE)

    # Register MQTT client callbacks
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    # Connect to MQTT broker
    print("connecting to %s:%d" % (MQTT_HOST, MQTT_PORT))
    client.connect(MQTT_HOST, MQTT_PORT, 60)
    client.loop_start()
    app.run(debug=True)