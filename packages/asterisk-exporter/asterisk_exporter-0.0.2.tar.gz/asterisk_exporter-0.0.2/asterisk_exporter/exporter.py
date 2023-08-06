import asyncio
from panoramisk import Manager
from pprint import pprint
from prometheus_client import start_http_server
from prometheus_client import Gauge, Counter
from asterisk_exporter.log import log


def start_server(host, port, user, password):
    manager = Manager(loop=asyncio.get_event_loop(), host="localhost", username=user, secret=password)

    @manager.register_event('FullyBooted')
    def on_asterisk_FullyBooted(manager, msg):
        log.debug(msg)
        resp_iax_peer_list = yield from manager.send_action({'Action': 'IAXpeerlist'})
        try:
            iax_peers = [ 'IAX2/' + msg.ObjectName for msg in resp_iax_peer_list if msg.Event=='PeerEntry' and 'OK' in msg.Status ]
        except AttributeError:
            iax_peers = []
        for iax_peer in iax_peers:
            peer_status_gauge.labels(proto='IAX2', peer=iax_peer).set(1)
        resp_pjsip_contacts = yield from manager.send_action({'Action': 'PJSIPShowContacts'})
        try:
            pjsip_peers = [ 'PJSIP/' + msg.Endpoint for msg in resp_pjsip_contacts if msg.Event=='ContactList' and msg.Status == 'Reachable' ]
        except AttributeError:
            pjsip_peers = []
        for pjsip_peer in pjsip_peers:
            peer_status_gauge.labels(proto='SIP', peer=pjsip_peer).set(1)
        resp_sip_peer_list = yield from manager.send_action({'Action': 'SIPPeers'})
        try:
            sip_peers = [ 'SIP/' + msg.ObjectName for msg in resp_sip_peer_list if msg.Event=='PeerEntry' and 'OK' in msg.Status ]
        except AttributeError:
            sip_peers = []
        for sip_peer in sip_peers:
            peer_status_gauge.labels(proto='SIP', peer=sip_peer).set(1)

    @manager.register_event('PeerStatus')
    def on_peer_status(manager, msg):
        log.debug(msg)
        if msg.ChannelType == 'PJSIP':
            proto = 'SIP'
        else:
            proto = msg.ChannelType
        if msg.PeerStatus == 'Unreachable' or msg.PeerStatus == 'Unregistered':
            peer_status_gauge.labels(proto=proto, peer=msg.Peer).set(0)
        if msg.PeerStatus == 'Reachable' or msg.PeerStatus == 'Registered':
            peer_status_gauge.labels(proto=proto, peer=msg.Peer).set(1)

    @manager.register_event('Newchannel')
    def on_channel_creation(manager, msg):
        log.debug(msg)
        channel_type = msg.Channel.split('/')[0]
        current_channels_gauge.labels(type=channel_type).inc()
        channels_counter.labels(type=channel_type).inc()

    @manager.register_event('Hangup')
    def on_channel_deletion(manager, msg):
        log.debug(msg)
        channel_type = msg.Channel.split('/')[0]
        current_channels_gauge.labels(type=channel_type).dec()

    start_http_server(port, host)
    peer_status_gauge = Gauge('asterisk_peer_status',
                              'Status of iax and sip peers',
                              ['proto', 'peer'])
    current_channels_gauge = Gauge('asterisk_current_channels',
                                  'Number of active channels',
                                  ['type'])
    channels_counter = Counter('asterisk_channels_total',
                               'Total number of created channels',
                               ['type'])
    current_channels_gauge.labels('IAX').set(0)
    current_channels_gauge.labels('PJSIP').set(0)
    current_channels_gauge.labels('SIP').set(0)
    manager.connect()
    manager.loop.run_forever()
