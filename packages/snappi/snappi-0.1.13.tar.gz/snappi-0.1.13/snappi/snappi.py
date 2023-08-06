from typing import Union
from .snappicommon import SnappiObject
from .snappicommon import SnappiList
from .snappicommon import SnappiRestTransport


class Api(SnappiRestTransport):
    """Snappi Abstract API
    """
    def __init__(self):
        super(Api, self).__init__()

    def set_config(self, content):
        """POST /config

        Sets configuration resources on the traffic generator.
        """
        return self.send_recv('post', '/config', payload=content)

    def update_config(self, content):
        """PATCH /config

        Updates configuration resources on the traffic generator.
        """
        return self.send_recv('patch', '/config', payload=content)

    def get_config(self):
        """GET /config

        TBD
        """
        return self.send_recv('get', '/config', return_object=self.config())

    def set_transmit_state(self, content):
        """POST /control/transmit

        Updates the state of configuration resources on the traffic generator.
        """
        return self.send_recv('post', '/control/transmit', payload=content)

    def set_link_state(self, content):
        """POST /control/link

        Updates the state of configuration resources on the traffic generator.
        """
        return self.send_recv('post', '/control/link', payload=content)

    def set_capture_state(self, content):
        """POST /control/capture

        Updates the state of configuration resources on the traffic generator.
        """
        return self.send_recv('post', '/control/capture', payload=content)

    def get_state_metrics(self):
        """POST /results/state

        TBD
        """
        return self.send_recv('post', '/results/state', return_object=self.state_metrics())

    def get_capabilities(self):
        """POST /results/capabilities

        TBD
        """
        return self.send_recv('post', '/results/capabilities', return_object=self.capabilities())

    def get_port_metrics(self, content):
        """POST /results/port

        TBD
        """
        return self.send_recv('post', '/results/port', payload=content, return_object=self.port_metrics())

    def get_capture(self, content):
        """POST /results/capture

        TBD
        """
        return self.send_recv('post', '/results/capture', payload=content)

    def get_flow_metrics(self, content):
        """POST /results/flow

        TBD
        """
        return self.send_recv('post', '/results/flow', payload=content, return_object=self.flow_metrics())

    def get_bgpv4_metrics(self, content):
        """POST /results/bgpv4

        TBD
        """
        return self.send_recv('post', '/results/bgpv4', payload=content, return_object=self.bgpv4_metrics())

    def config(self):
        """Factory method that creates an instance of the Config class

        Return: obj(Config)
        """
        return Config()

    def transmit_state(self):
        """Factory method that creates an instance of the TransmitState class

        Return: obj(TransmitState)
        """
        return TransmitState()

    def link_state(self):
        """Factory method that creates an instance of the LinkState class

        Return: obj(LinkState)
        """
        return LinkState()

    def capture_state(self):
        """Factory method that creates an instance of the CaptureState class

        Return: obj(CaptureState)
        """
        return CaptureState()

    def state_metrics(self):
        """Factory method that creates an instance of the StateMetrics class

        Return: obj(StateMetrics)
        """
        return StateMetrics()

    def capabilities(self):
        """Factory method that creates an instance of the Capabilities class

        Return: obj(Capabilities)
        """
        return Capabilities()

    def port_metrics_request(self):
        """Factory method that creates an instance of the PortMetricsRequest class

        Return: obj(PortMetricsRequest)
        """
        return PortMetricsRequest()

    def port_metrics(self):
        """Factory method that creates an instance of the PortMetricList class

        Return: obj(PortMetricList)
        """
        return PortMetricList()

    def capture_request(self):
        """Factory method that creates an instance of the CaptureRequest class

        Return: obj(CaptureRequest)
        """
        return CaptureRequest()

    def flow_metrics_request(self):
        """Factory method that creates an instance of the FlowMetricsRequest class

        Return: obj(FlowMetricsRequest)
        """
        return FlowMetricsRequest()

    def flow_metrics(self):
        """Factory method that creates an instance of the FlowMetricList class

        Return: obj(FlowMetricList)
        """
        return FlowMetricList()

    def bgpv4_metrics_request(self):
        """Factory method that creates an instance of the Bgpv4MetricsRequest class

        Return: obj(Bgpv4MetricsRequest)
        """
        return Bgpv4MetricsRequest()

    def bgpv4_metrics(self):
        """Factory method that creates an instance of the Bgpv4Metrics class

        Return: obj(Bgpv4Metrics)
        """
        return Bgpv4Metrics()


class Config(SnappiObject):
    __slots__ = ()

    _TYPES = {
        'ports': 'PortList',
        'lags': 'LagList',
        'layer1': 'Layer1List',
        'captures': 'CaptureList',
        'devices': 'DeviceList',
        'flows': 'FlowList',
        'options': 'ConfigOptions',
    }

    def __init__(self):
        super(Config, self).__init__()

    @property
    def ports(self):
        # type: () -> PortList
        """ports getter

        The ports that will be configured on the traffic generator.

        Returns: list[obj(snappi.Port)]
        """
        if 'ports' not in self._properties or self._properties['ports'] is None:
            self._properties['ports'] = PortList()
        return self._properties['ports']

    @property
    def lags(self):
        # type: () -> LagList
        """lags getter

        The lags that will be configured on the traffic generator.

        Returns: list[obj(snappi.Lag)]
        """
        if 'lags' not in self._properties or self._properties['lags'] is None:
            self._properties['lags'] = LagList()
        return self._properties['lags']

    @property
    def layer1(self):
        # type: () -> Layer1List
        """layer1 getter

        The layer1 settings that will be configured on the traffic generator.

        Returns: list[obj(snappi.Layer1)]
        """
        if 'layer1' not in self._properties or self._properties['layer1'] is None:
            self._properties['layer1'] = Layer1List()
        return self._properties['layer1']

    @property
    def captures(self):
        # type: () -> CaptureList
        """captures getter

        The capture settings that will be configured on the traffic generator.

        Returns: list[obj(snappi.Capture)]
        """
        if 'captures' not in self._properties or self._properties['captures'] is None:
            self._properties['captures'] = CaptureList()
        return self._properties['captures']

    @property
    def devices(self):
        # type: () -> DeviceList
        """devices getter

        The emulated device settings that will be configured on the traffic generator.

        Returns: list[obj(snappi.Device)]
        """
        if 'devices' not in self._properties or self._properties['devices'] is None:
            self._properties['devices'] = DeviceList()
        return self._properties['devices']

    @property
    def flows(self):
        # type: () -> FlowList
        """flows getter

        The flows that will be configured on the traffic generator.

        Returns: list[obj(snappi.Flow)]
        """
        if 'flows' not in self._properties or self._properties['flows'] is None:
            self._properties['flows'] = FlowList()
        return self._properties['flows']

    @property
    def options(self):
        # type: () -> ConfigOptions
        """options getter

        Global configuration options.

        Returns: obj(snappi.ConfigOptions)
        """
        if 'options' not in self._properties or self._properties['options'] is None:
            self._properties['options'] = ConfigOptions()
        return self._properties['options']


class Port(SnappiObject):
    __slots__ = ()

    def __init__(self, location=None, name=None):
        super(Port, self).__init__()
        self.location = location
        self.name = name

    @property
    def location(self):
        # type: () -> str
        """location getter

        The location of a test port. It is the endpoint where packets will emit from.. Test port locations can be the following:. - physical appliance with multiple ports. - physical chassis with multiple cards and ports. - local interface. - virtual machine, docker container, kubernetes cluster. . The test port location format is implementation specific. Use the /results/capabilities API to determine what formats an implementation supports for the location property.. Get the configured location state by using the /results/port API.

        Returns: str
        """
        return self._properties['location']

    @location.setter
    def location(self, value):
        """location setter

        The location of a test port. It is the endpoint where packets will emit from.. Test port locations can be the following:. - physical appliance with multiple ports. - physical chassis with multiple cards and ports. - local interface. - virtual machine, docker container, kubernetes cluster. . The test port location format is implementation specific. Use the /results/capabilities API to determine what formats an implementation supports for the location property.. Get the configured location state by using the /results/port API.

        value: str
        """
        self._properties['location'] = value

    @property
    def name(self):
        # type: () -> str
        """name getter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        Returns: str
        """
        return self._properties['name']

    @name.setter
    def name(self, value):
        """name setter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        value: str
        """
        self._properties['name'] = value


class PortList(SnappiList):
    __slots__ = ()

    def __init__(self):
        super(PortList, self).__init__()

    def __getitem__(self, key):
        # type: (int) -> Port
        return self._getitem(key)

    def __iter__(self):
        # type: () -> PortList
        return self._iter()

    def __next__(self):
        # type: () -> Port
        return self._next()

    def next(self):
        # type: () -> Port
        return self._next()

    def port(self, location=None, name=None):
        # type: () -> PortList
        """Factory method that creates an instance of Port class

        An abstract test port.
        """
        item = Port(location, name)
        self._add(item)
        return self


class Lag(SnappiObject):
    __slots__ = ()

    _TYPES = {
        'protocol': 'LagProtocol',
        'ethernet': 'DeviceEthernet',
    }

    def __init__(self, port_names=None, name=None):
        super(Lag, self).__init__()
        self.port_names = port_names
        self.name = name

    @property
    def port_names(self):
        # type: () -> list[str]
        """port_names getter

        A list of unique names of port objects that will be part of the same lag. The value of the port_names property is the count for any child property in this hierarchy that is a container for a device pattern.

        Returns: list[str]
        """
        return self._properties['port_names']

    @port_names.setter
    def port_names(self, value):
        """port_names setter

        A list of unique names of port objects that will be part of the same lag. The value of the port_names property is the count for any child property in this hierarchy that is a container for a device pattern.

        value: list[str]
        """
        self._properties['port_names'] = value

    @property
    def protocol(self):
        # type: () -> LagProtocol
        """protocol getter

        Static lag or LACP protocol settings.

        Returns: obj(snappi.LagProtocol)
        """
        if 'protocol' not in self._properties or self._properties['protocol'] is None:
            self._properties['protocol'] = LagProtocol()
        return self._properties['protocol']

    @property
    def ethernet(self):
        # type: () -> DeviceEthernet
        """ethernet getter

        Emulated ethernet protocol. A top level in the emulated device stack.Per port ethernet and vlan settings.

        Returns: obj(snappi.DeviceEthernet)
        """
        if 'ethernet' not in self._properties or self._properties['ethernet'] is None:
            self._properties['ethernet'] = DeviceEthernet()
        return self._properties['ethernet']

    @property
    def name(self):
        # type: () -> str
        """name getter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        Returns: str
        """
        return self._properties['name']

    @name.setter
    def name(self, value):
        """name setter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        value: str
        """
        self._properties['name'] = value


class LagProtocol(SnappiObject):
    __slots__ = ()

    _TYPES = {
        'lacp': 'LagLacp',
        'static': 'LagStatic',
    }

    LACP = 'lacp'
    STATIC = 'static'

    def __init__(self):
        super(LagProtocol, self).__init__()

    @property
    def lacp(self):
        # type: () -> LagLacp
        """Factory method to create an instance of the LagLacp class

        TBD
        """
        if 'lacp' not in self._properties or self._properties['lacp'] is None:
            self._properties['lacp'] = LagLacp()
        self.choice = 'lacp'
        return self._properties['lacp']

    @property
    def static(self):
        # type: () -> LagStatic
        """Factory method to create an instance of the LagStatic class

        TBD
        """
        if 'static' not in self._properties or self._properties['static'] is None:
            self._properties['static'] = LagStatic()
        self.choice = 'static'
        return self._properties['static']

    @property
    def choice(self):
        # type: () -> Union[lacp, static, choice, choice, choice]
        """choice getter

        The type of lag protocol.

        Returns: Union[lacp, static, choice, choice, choice]
        """
        return self._properties['choice']

    @choice.setter
    def choice(self, value):
        """choice setter

        The type of lag protocol.

        value: Union[lacp, static, choice, choice, choice]
        """
        self._properties['choice'] = value


class LagLacp(SnappiObject):
    __slots__ = ()

    _TYPES = {
        'actor_key': 'DevicePattern',
        'actor_port_number': 'DevicePattern',
        'actor_port_priority': 'DevicePattern',
        'actor_system_id': 'DevicePattern',
        'actor_system_priority': 'DevicePattern',
    }

    def __init__(self):
        super(LagLacp, self).__init__()

    @property
    def actor_key(self):
        # type: () -> DevicePattern
        """actor_key getter

        A container for emulated device property patterns.A container for emulated device property patterns.The actor key.

        Returns: obj(snappi.DevicePattern)
        """
        if 'actor_key' not in self._properties or self._properties['actor_key'] is None:
            self._properties['actor_key'] = DevicePattern()
        return self._properties['actor_key']

    @property
    def actor_port_number(self):
        # type: () -> DevicePattern
        """actor_port_number getter

        A container for emulated device property patterns.A container for emulated device property patterns.The actor port number.

        Returns: obj(snappi.DevicePattern)
        """
        if 'actor_port_number' not in self._properties or self._properties['actor_port_number'] is None:
            self._properties['actor_port_number'] = DevicePattern()
        return self._properties['actor_port_number']

    @property
    def actor_port_priority(self):
        # type: () -> DevicePattern
        """actor_port_priority getter

        A container for emulated device property patterns.A container for emulated device property patterns.The actor port priority.

        Returns: obj(snappi.DevicePattern)
        """
        if 'actor_port_priority' not in self._properties or self._properties['actor_port_priority'] is None:
            self._properties['actor_port_priority'] = DevicePattern()
        return self._properties['actor_port_priority']

    @property
    def actor_system_id(self):
        # type: () -> DevicePattern
        """actor_system_id getter

        A container for emulated device property patterns.A container for emulated device property patterns.The actor system id.

        Returns: obj(snappi.DevicePattern)
        """
        if 'actor_system_id' not in self._properties or self._properties['actor_system_id'] is None:
            self._properties['actor_system_id'] = DevicePattern()
        return self._properties['actor_system_id']

    @property
    def actor_system_priority(self):
        # type: () -> DevicePattern
        """actor_system_priority getter

        A container for emulated device property patterns.A container for emulated device property patterns.The actor system priority.

        Returns: obj(snappi.DevicePattern)
        """
        if 'actor_system_priority' not in self._properties or self._properties['actor_system_priority'] is None:
            self._properties['actor_system_priority'] = DevicePattern()
        return self._properties['actor_system_priority']


class DevicePattern(SnappiObject):
    __slots__ = ()

    _TYPES = {
        'increment': 'DeviceCounter',
        'decrement': 'DeviceCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self):
        super(DevicePattern, self).__init__()

    @property
    def increment(self):
        # type: () -> DeviceCounter
        """Factory method to create an instance of the DeviceCounter class

        An incrementing pattern.
        """
        if 'increment' not in self._properties or self._properties['increment'] is None:
            self._properties['increment'] = DeviceCounter()
        self.choice = 'increment'
        return self._properties['increment']

    @property
    def decrement(self):
        # type: () -> DeviceCounter
        """Factory method to create an instance of the DeviceCounter class

        An incrementing pattern.
        """
        if 'decrement' not in self._properties or self._properties['decrement'] is None:
            self._properties['decrement'] = DeviceCounter()
        self.choice = 'decrement'
        return self._properties['decrement']

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._properties['choice']

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._properties['choice'] = value

    @property
    def value(self):
        # type: () -> str
        """value getter

        TBD

        Returns: str
        """
        return self._properties['value']

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: str
        """
        self._properties['choice'] = 'value'
        self._properties['value'] = value

    @property
    def values(self):
        # type: () -> list[str]
        """values getter

        TBD

        Returns: list[str]
        """
        return self._properties['values']

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[str]
        """
        self._properties['choice'] = 'values'
        self._properties['values'] = value


class DeviceCounter(SnappiObject):
    __slots__ = ()

    def __init__(self, start=None, step=None):
        super(DeviceCounter, self).__init__()
        self.start = start
        self.step = step

    @property
    def start(self):
        # type: () -> str
        """start getter

        TBD

        Returns: str
        """
        return self._properties['start']

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: str
        """
        self._properties['start'] = value

    @property
    def step(self):
        # type: () -> str
        """step getter

        TBD

        Returns: str
        """
        return self._properties['step']

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: str
        """
        self._properties['step'] = value


class LagStatic(SnappiObject):
    __slots__ = ()

    _TYPES = {
        'lag_id': 'DevicePattern',
    }

    def __init__(self):
        super(LagStatic, self).__init__()

    @property
    def lag_id(self):
        # type: () -> DevicePattern
        """lag_id getter

        A container for emulated device property patterns.A container for emulated device property patterns.The static lag id.

        Returns: obj(snappi.DevicePattern)
        """
        if 'lag_id' not in self._properties or self._properties['lag_id'] is None:
            self._properties['lag_id'] = DevicePattern()
        return self._properties['lag_id']


class DeviceEthernet(SnappiObject):
    __slots__ = ()

    _TYPES = {
        'mac': 'DevicePattern',
        'mtu': 'DevicePattern',
        'vlans': 'DeviceVlanList',
    }

    def __init__(self, name=None):
        super(DeviceEthernet, self).__init__()
        self.name = name

    @property
    def mac(self):
        # type: () -> DevicePattern
        """mac getter

        A container for emulated device property patterns.Media access control address (MAC) is a 48bit identifier for use as a network address. The value can be an int or a hex string with or without spaces or colons separating each byte. The min value is 0 or '00:00:00:00:00:00'. The max value is 281474976710655 or 'FF:FF:FF:FF:FF:FF'.

        Returns: obj(snappi.DevicePattern)
        """
        if 'mac' not in self._properties or self._properties['mac'] is None:
            self._properties['mac'] = DevicePattern()
        return self._properties['mac']

    @property
    def mtu(self):
        # type: () -> DevicePattern
        """mtu getter

        A container for emulated device property patterns.

        Returns: obj(snappi.DevicePattern)
        """
        if 'mtu' not in self._properties or self._properties['mtu'] is None:
            self._properties['mtu'] = DevicePattern()
        return self._properties['mtu']

    @property
    def vlans(self):
        # type: () -> DeviceVlanList
        """vlans getter

        List of vlans

        Returns: list[obj(snappi.DeviceVlan)]
        """
        if 'vlans' not in self._properties or self._properties['vlans'] is None:
            self._properties['vlans'] = DeviceVlanList()
        return self._properties['vlans']

    @property
    def name(self):
        # type: () -> str
        """name getter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        Returns: str
        """
        return self._properties['name']

    @name.setter
    def name(self, value):
        """name setter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        value: str
        """
        self._properties['name'] = value


class DeviceVlan(SnappiObject):
    __slots__ = ()

    _TYPES = {
        'tpid': 'DevicePattern',
        'priority': 'DevicePattern',
        'id': 'DevicePattern',
    }

    TPID_8100 = '8100'
    TPID_88A8 = '88a8'
    TPID_9100 = '9100'
    TPID_9200 = '9200'
    TPID_9300 = '9300'

    def __init__(self, name=None):
        super(DeviceVlan, self).__init__()
        self.name = name

    @property
    def tpid(self):
        # type: () -> DevicePattern
        """tpid getter

        A container for emulated device property patterns.Vlan tag protocol identifier.

        Returns: obj(snappi.DevicePattern)
        """
        if 'tpid' not in self._properties or self._properties['tpid'] is None:
            self._properties['tpid'] = DevicePattern()
        return self._properties['tpid']

    @property
    def priority(self):
        # type: () -> DevicePattern
        """priority getter

        A container for emulated device property patterns.Vlan priority.

        Returns: obj(snappi.DevicePattern)
        """
        if 'priority' not in self._properties or self._properties['priority'] is None:
            self._properties['priority'] = DevicePattern()
        return self._properties['priority']

    @property
    def id(self):
        # type: () -> DevicePattern
        """id getter

        A container for emulated device property patterns.Vlan id.

        Returns: obj(snappi.DevicePattern)
        """
        if 'id' not in self._properties or self._properties['id'] is None:
            self._properties['id'] = DevicePattern()
        return self._properties['id']

    @property
    def name(self):
        # type: () -> str
        """name getter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        Returns: str
        """
        return self._properties['name']

    @name.setter
    def name(self, value):
        """name setter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        value: str
        """
        self._properties['name'] = value


class DeviceVlanList(SnappiList):
    __slots__ = ()

    def __init__(self):
        super(DeviceVlanList, self).__init__()

    def __getitem__(self, key):
        # type: (int) -> DeviceVlan
        return self._getitem(key)

    def __iter__(self):
        # type: () -> DeviceVlanList
        return self._iter()

    def __next__(self):
        # type: () -> DeviceVlan
        return self._next()

    def next(self):
        # type: () -> DeviceVlan
        return self._next()

    def vlan(self, name=None):
        # type: () -> DeviceVlanList
        """Factory method that creates an instance of DeviceVlan class

        Emulated vlan protocol
        """
        item = DeviceVlan(name)
        self._add(item)
        return self


class LagList(SnappiList):
    __slots__ = ()

    def __init__(self):
        super(LagList, self).__init__()

    def __getitem__(self, key):
        # type: (int) -> Lag
        return self._getitem(key)

    def __iter__(self):
        # type: () -> LagList
        return self._iter()

    def __next__(self):
        # type: () -> Lag
        return self._next()

    def next(self):
        # type: () -> Lag
        return self._next()

    def lag(self, port_names=None, name=None):
        # type: () -> LagList
        """Factory method that creates an instance of Lag class

        A container for LAG settings.
        """
        item = Lag(port_names, name)
        self._add(item)
        return self


class Layer1(SnappiObject):
    __slots__ = ()

    _TYPES = {
        'auto_negotiation': 'Layer1AutoNegotiation',
        'flow_control': 'Layer1FlowControl',
    }

    SPEED_10_FD_MBPS = 'speed_10_fd_mbps'
    SPEED_10_HD_MBPS = 'speed_10_hd_mbps'
    SPEED_100_FD_MBPS = 'speed_100_fd_mbps'
    SPEED_100_HD_MBPS = 'speed_100_hd_mbps'
    SPEED_1_GBPS = 'speed_1_gbps'
    SPEED_10_GBPS = 'speed_10_gbps'
    SPEED_25_GBPS = 'speed_25_gbps'
    SPEED_40_GBPS = 'speed_40_gbps'
    SPEED_100_GBPS = 'speed_100_gbps'
    SPEED_200_GBPS = 'speed_200_gbps'
    SPEED_400_GBPS = 'speed_400_gbps'

    COPPER = 'copper'
    FIBER = 'fiber'
    SGMII = 'sgmii'

    def __init__(self, port_names=None, speed=None, media=None, promiscuous=None, mtu=None, ieee_media_defaults=None, auto_negotiate=None, name=None):
        super(Layer1, self).__init__()
        self.port_names = port_names
        self.speed = speed
        self.media = media
        self.promiscuous = promiscuous
        self.mtu = mtu
        self.ieee_media_defaults = ieee_media_defaults
        self.auto_negotiate = auto_negotiate
        self.name = name

    @property
    def port_names(self):
        # type: () -> list[str]
        """port_names getter

        A list of unique names of port objects that will share the choice settings. 

        Returns: list[str]
        """
        return self._properties['port_names']

    @port_names.setter
    def port_names(self, value):
        """port_names setter

        A list of unique names of port objects that will share the choice settings. 

        value: list[str]
        """
        self._properties['port_names'] = value

    @property
    def speed(self):
        # type: () -> Union[speed_10_fd_mbps, speed_10_hd_mbps, speed_100_fd_mbps, speed_100_hd_mbps, speed_1_gbps, speed_10_gbps, speed_25_gbps, speed_40_gbps, speed_100_gbps, speed_200_gbps, speed_400_gbps]
        """speed getter

        Set the speed if supported.

        Returns: Union[speed_10_fd_mbps, speed_10_hd_mbps, speed_100_fd_mbps, speed_100_hd_mbps, speed_1_gbps, speed_10_gbps, speed_25_gbps, speed_40_gbps, speed_100_gbps, speed_200_gbps, speed_400_gbps]
        """
        return self._properties['speed']

    @speed.setter
    def speed(self, value):
        """speed setter

        Set the speed if supported.

        value: Union[speed_10_fd_mbps, speed_10_hd_mbps, speed_100_fd_mbps, speed_100_hd_mbps, speed_1_gbps, speed_10_gbps, speed_25_gbps, speed_40_gbps, speed_100_gbps, speed_200_gbps, speed_400_gbps]
        """
        self._properties['speed'] = value

    @property
    def media(self):
        # type: () -> Union[copper, fiber, sgmii]
        """media getter

        Set the type of media interface if supported.

        Returns: Union[copper, fiber, sgmii]
        """
        return self._properties['media']

    @media.setter
    def media(self, value):
        """media setter

        Set the type of media interface if supported.

        value: Union[copper, fiber, sgmii]
        """
        self._properties['media'] = value

    @property
    def promiscuous(self):
        # type: () -> boolean
        """promiscuous getter

        Enable promiscuous mode if supported.

        Returns: boolean
        """
        return self._properties['promiscuous']

    @promiscuous.setter
    def promiscuous(self, value):
        """promiscuous setter

        Enable promiscuous mode if supported.

        value: boolean
        """
        self._properties['promiscuous'] = value

    @property
    def mtu(self):
        # type: () -> int
        """mtu getter

        Set the maximum transmission unit size if supported.

        Returns: int
        """
        return self._properties['mtu']

    @mtu.setter
    def mtu(self, value):
        """mtu setter

        Set the maximum transmission unit size if supported.

        value: int
        """
        self._properties['mtu'] = value

    @property
    def ieee_media_defaults(self):
        # type: () -> boolean
        """ieee_media_defaults getter

        Set to true to override the auto_negotiate, link_training and rs_fec settings for gigabit ethernet interfaces.

        Returns: boolean
        """
        return self._properties['ieee_media_defaults']

    @ieee_media_defaults.setter
    def ieee_media_defaults(self, value):
        """ieee_media_defaults setter

        Set to true to override the auto_negotiate, link_training and rs_fec settings for gigabit ethernet interfaces.

        value: boolean
        """
        self._properties['ieee_media_defaults'] = value

    @property
    def auto_negotiate(self):
        # type: () -> boolean
        """auto_negotiate getter

        Enable/disable auto negotiation.

        Returns: boolean
        """
        return self._properties['auto_negotiate']

    @auto_negotiate.setter
    def auto_negotiate(self, value):
        """auto_negotiate setter

        Enable/disable auto negotiation.

        value: boolean
        """
        self._properties['auto_negotiate'] = value

    @property
    def auto_negotiation(self):
        # type: () -> Layer1AutoNegotiation
        """auto_negotiation getter

        Container for auto negotiation settings

        Returns: obj(snappi.Layer1AutoNegotiation)
        """
        if 'auto_negotiation' not in self._properties or self._properties['auto_negotiation'] is None:
            self._properties['auto_negotiation'] = Layer1AutoNegotiation()
        return self._properties['auto_negotiation']

    @property
    def flow_control(self):
        # type: () -> Layer1FlowControl
        """flow_control getter

        A container for layer1 receive flow control settings. To enable flow control settings on ports this object must be a valid object not a null value.

        Returns: obj(snappi.Layer1FlowControl)
        """
        if 'flow_control' not in self._properties or self._properties['flow_control'] is None:
            self._properties['flow_control'] = Layer1FlowControl()
        return self._properties['flow_control']

    @property
    def name(self):
        # type: () -> str
        """name getter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        Returns: str
        """
        return self._properties['name']

    @name.setter
    def name(self, value):
        """name setter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        value: str
        """
        self._properties['name'] = value


class Layer1AutoNegotiation(SnappiObject):
    __slots__ = ()

    def __init__(self, advertise_1000_mbps=None, advertise_100_fd_mbps=None, advertise_100_hd_mbps=None, advertise_10_fd_mbps=None, advertise_10_hd_mbps=None, link_training=None, rs_fec=None):
        super(Layer1AutoNegotiation, self).__init__()
        self.advertise_1000_mbps = advertise_1000_mbps
        self.advertise_100_fd_mbps = advertise_100_fd_mbps
        self.advertise_100_hd_mbps = advertise_100_hd_mbps
        self.advertise_10_fd_mbps = advertise_10_fd_mbps
        self.advertise_10_hd_mbps = advertise_10_hd_mbps
        self.link_training = link_training
        self.rs_fec = rs_fec

    @property
    def advertise_1000_mbps(self):
        # type: () -> boolean
        """advertise_1000_mbps getter

        If auto_negotiate is true and the interface supports this option then this speed will be advertised.

        Returns: boolean
        """
        return self._properties['advertise_1000_mbps']

    @advertise_1000_mbps.setter
    def advertise_1000_mbps(self, value):
        """advertise_1000_mbps setter

        If auto_negotiate is true and the interface supports this option then this speed will be advertised.

        value: boolean
        """
        self._properties['advertise_1000_mbps'] = value

    @property
    def advertise_100_fd_mbps(self):
        # type: () -> boolean
        """advertise_100_fd_mbps getter

        If auto_negotiate is true and the interface supports this option then this speed will be advertised.

        Returns: boolean
        """
        return self._properties['advertise_100_fd_mbps']

    @advertise_100_fd_mbps.setter
    def advertise_100_fd_mbps(self, value):
        """advertise_100_fd_mbps setter

        If auto_negotiate is true and the interface supports this option then this speed will be advertised.

        value: boolean
        """
        self._properties['advertise_100_fd_mbps'] = value

    @property
    def advertise_100_hd_mbps(self):
        # type: () -> boolean
        """advertise_100_hd_mbps getter

        If auto_negotiate is true and the interface supports this option then this speed will be advertised.

        Returns: boolean
        """
        return self._properties['advertise_100_hd_mbps']

    @advertise_100_hd_mbps.setter
    def advertise_100_hd_mbps(self, value):
        """advertise_100_hd_mbps setter

        If auto_negotiate is true and the interface supports this option then this speed will be advertised.

        value: boolean
        """
        self._properties['advertise_100_hd_mbps'] = value

    @property
    def advertise_10_fd_mbps(self):
        # type: () -> boolean
        """advertise_10_fd_mbps getter

        If auto_negotiate is true and the interface supports this option then this speed will be advertised.

        Returns: boolean
        """
        return self._properties['advertise_10_fd_mbps']

    @advertise_10_fd_mbps.setter
    def advertise_10_fd_mbps(self, value):
        """advertise_10_fd_mbps setter

        If auto_negotiate is true and the interface supports this option then this speed will be advertised.

        value: boolean
        """
        self._properties['advertise_10_fd_mbps'] = value

    @property
    def advertise_10_hd_mbps(self):
        # type: () -> boolean
        """advertise_10_hd_mbps getter

        If auto_negotiate is true and the interface supports this option then this speed will be advertised.

        Returns: boolean
        """
        return self._properties['advertise_10_hd_mbps']

    @advertise_10_hd_mbps.setter
    def advertise_10_hd_mbps(self, value):
        """advertise_10_hd_mbps setter

        If auto_negotiate is true and the interface supports this option then this speed will be advertised.

        value: boolean
        """
        self._properties['advertise_10_hd_mbps'] = value

    @property
    def link_training(self):
        # type: () -> boolean
        """link_training getter

        Enable/disable gigabit ethernet link training.

        Returns: boolean
        """
        return self._properties['link_training']

    @link_training.setter
    def link_training(self, value):
        """link_training setter

        Enable/disable gigabit ethernet link training.

        value: boolean
        """
        self._properties['link_training'] = value

    @property
    def rs_fec(self):
        # type: () -> boolean
        """rs_fec getter

        Enable/disable gigabit ethernet reed solomon forward error correction (RS FEC).

        Returns: boolean
        """
        return self._properties['rs_fec']

    @rs_fec.setter
    def rs_fec(self, value):
        """rs_fec setter

        Enable/disable gigabit ethernet reed solomon forward error correction (RS FEC).

        value: boolean
        """
        self._properties['rs_fec'] = value


class Layer1FlowControl(SnappiObject):
    __slots__ = ()

    _TYPES = {
        'ieee_802_1qbb': 'Layer1Ieee8021qbb',
        'ieee_802_3x': 'Layer1Ieee8023x',
    }

    IEEE_802_1QBB = 'ieee_802_1qbb'
    IEEE_802_3X = 'ieee_802_3x'

    def __init__(self, directed_address=None):
        super(Layer1FlowControl, self).__init__()
        self.directed_address = directed_address

    @property
    def ieee_802_1qbb(self):
        # type: () -> Layer1Ieee8021qbb
        """Factory method to create an instance of the Layer1Ieee8021qbb class

        These settings enhance the existing 802.3x pause priority capabilities to enable flow control based on 802.1p priorities (classes of service). 
        """
        if 'ieee_802_1qbb' not in self._properties or self._properties['ieee_802_1qbb'] is None:
            self._properties['ieee_802_1qbb'] = Layer1Ieee8021qbb()
        self.choice = 'ieee_802_1qbb'
        return self._properties['ieee_802_1qbb']

    @property
    def ieee_802_3x(self):
        # type: () -> Layer1Ieee8023x
        """Factory method to create an instance of the Layer1Ieee8023x class

        A container for ieee 802.3x rx pause settings
        """
        if 'ieee_802_3x' not in self._properties or self._properties['ieee_802_3x'] is None:
            self._properties['ieee_802_3x'] = Layer1Ieee8023x()
        self.choice = 'ieee_802_3x'
        return self._properties['ieee_802_3x']

    @property
    def directed_address(self):
        # type: () -> str
        """directed_address getter

        The 48bit mac address that the layer1 port names will listen on for a directed pause. 

        Returns: str
        """
        return self._properties['directed_address']

    @directed_address.setter
    def directed_address(self, value):
        """directed_address setter

        The 48bit mac address that the layer1 port names will listen on for a directed pause. 

        value: str
        """
        self._properties['directed_address'] = value

    @property
    def choice(self):
        # type: () -> Union[ieee_802_1qbb, ieee_802_3x, choice, choice, choice, choice]
        """choice getter

        The type of priority flow control.

        Returns: Union[ieee_802_1qbb, ieee_802_3x, choice, choice, choice, choice]
        """
        return self._properties['choice']

    @choice.setter
    def choice(self, value):
        """choice setter

        The type of priority flow control.

        value: Union[ieee_802_1qbb, ieee_802_3x, choice, choice, choice, choice]
        """
        self._properties['choice'] = value


class Layer1Ieee8021qbb(SnappiObject):
    __slots__ = ()

    def __init__(self, pfc_delay=None, pfc_class_0=None, pfc_class_1=None, pfc_class_2=None, pfc_class_3=None, pfc_class_4=None, pfc_class_5=None, pfc_class_6=None, pfc_class_7=None):
        super(Layer1Ieee8021qbb, self).__init__()
        self.pfc_delay = pfc_delay
        self.pfc_class_0 = pfc_class_0
        self.pfc_class_1 = pfc_class_1
        self.pfc_class_2 = pfc_class_2
        self.pfc_class_3 = pfc_class_3
        self.pfc_class_4 = pfc_class_4
        self.pfc_class_5 = pfc_class_5
        self.pfc_class_6 = pfc_class_6
        self.pfc_class_7 = pfc_class_7

    @property
    def pfc_delay(self):
        # type: () -> int
        """pfc_delay getter

        The upper limit on the transmit time of a queue after receiving a message to pause a specified priority. A value of 0 or null indicates that pfc delay will not be enabled. 

        Returns: int
        """
        return self._properties['pfc_delay']

    @pfc_delay.setter
    def pfc_delay(self, value):
        """pfc_delay setter

        The upper limit on the transmit time of a queue after receiving a message to pause a specified priority. A value of 0 or null indicates that pfc delay will not be enabled. 

        value: int
        """
        self._properties['pfc_delay'] = value

    @property
    def pfc_class_0(self):
        # type: () -> int
        """pfc_class_0 getter

        The valid values are null, 0 - 7. A null value indicates there is no setting for this pfc class.

        Returns: int
        """
        return self._properties['pfc_class_0']

    @pfc_class_0.setter
    def pfc_class_0(self, value):
        """pfc_class_0 setter

        The valid values are null, 0 - 7. A null value indicates there is no setting for this pfc class.

        value: int
        """
        self._properties['pfc_class_0'] = value

    @property
    def pfc_class_1(self):
        # type: () -> int
        """pfc_class_1 getter

        The valid values are null, 0 - 7. A null value indicates there is no setting for this pfc class.

        Returns: int
        """
        return self._properties['pfc_class_1']

    @pfc_class_1.setter
    def pfc_class_1(self, value):
        """pfc_class_1 setter

        The valid values are null, 0 - 7. A null value indicates there is no setting for this pfc class.

        value: int
        """
        self._properties['pfc_class_1'] = value

    @property
    def pfc_class_2(self):
        # type: () -> int
        """pfc_class_2 getter

        The valid values are null, 0 - 7. A null value indicates there is no setting for this pfc class.

        Returns: int
        """
        return self._properties['pfc_class_2']

    @pfc_class_2.setter
    def pfc_class_2(self, value):
        """pfc_class_2 setter

        The valid values are null, 0 - 7. A null value indicates there is no setting for this pfc class.

        value: int
        """
        self._properties['pfc_class_2'] = value

    @property
    def pfc_class_3(self):
        # type: () -> int
        """pfc_class_3 getter

        The valid values are null, 0 - 7. A null value indicates there is no setting for this pfc class.

        Returns: int
        """
        return self._properties['pfc_class_3']

    @pfc_class_3.setter
    def pfc_class_3(self, value):
        """pfc_class_3 setter

        The valid values are null, 0 - 7. A null value indicates there is no setting for this pfc class.

        value: int
        """
        self._properties['pfc_class_3'] = value

    @property
    def pfc_class_4(self):
        # type: () -> int
        """pfc_class_4 getter

        The valid values are null, 0 - 7. A null value indicates there is no setting for this pfc class.

        Returns: int
        """
        return self._properties['pfc_class_4']

    @pfc_class_4.setter
    def pfc_class_4(self, value):
        """pfc_class_4 setter

        The valid values are null, 0 - 7. A null value indicates there is no setting for this pfc class.

        value: int
        """
        self._properties['pfc_class_4'] = value

    @property
    def pfc_class_5(self):
        # type: () -> int
        """pfc_class_5 getter

        The valid values are null, 0 - 7. A null value indicates there is no setting for this pfc class.

        Returns: int
        """
        return self._properties['pfc_class_5']

    @pfc_class_5.setter
    def pfc_class_5(self, value):
        """pfc_class_5 setter

        The valid values are null, 0 - 7. A null value indicates there is no setting for this pfc class.

        value: int
        """
        self._properties['pfc_class_5'] = value

    @property
    def pfc_class_6(self):
        # type: () -> int
        """pfc_class_6 getter

        The valid values are null, 0 - 7. A null value indicates there is no setting for this pfc class.

        Returns: int
        """
        return self._properties['pfc_class_6']

    @pfc_class_6.setter
    def pfc_class_6(self, value):
        """pfc_class_6 setter

        The valid values are null, 0 - 7. A null value indicates there is no setting for this pfc class.

        value: int
        """
        self._properties['pfc_class_6'] = value

    @property
    def pfc_class_7(self):
        # type: () -> int
        """pfc_class_7 getter

        The valid values are null, 0 - 7. A null value indicates there is no setting for this pfc class.

        Returns: int
        """
        return self._properties['pfc_class_7']

    @pfc_class_7.setter
    def pfc_class_7(self, value):
        """pfc_class_7 setter

        The valid values are null, 0 - 7. A null value indicates there is no setting for this pfc class.

        value: int
        """
        self._properties['pfc_class_7'] = value


class Layer1Ieee8023x(SnappiObject):
    __slots__ = ()

    def __init__(self):
        super(Layer1Ieee8023x, self).__init__()


class Layer1List(SnappiList):
    __slots__ = ()

    def __init__(self):
        super(Layer1List, self).__init__()

    def __getitem__(self, key):
        # type: (int) -> Layer1
        return self._getitem(key)

    def __iter__(self):
        # type: () -> Layer1List
        return self._iter()

    def __next__(self):
        # type: () -> Layer1
        return self._next()

    def next(self):
        # type: () -> Layer1
        return self._next()

    def layer1(self, port_names=None, speed='speed_10_gbps', media='None', promiscuous=False, mtu=1500, ieee_media_defaults=True, auto_negotiate=True, name=None):
        # type: () -> Layer1List
        """Factory method that creates an instance of Layer1 class

        A container for layer1 settings.
        """
        item = Layer1(port_names, speed, media, promiscuous, mtu, ieee_media_defaults, auto_negotiate, name)
        self._add(item)
        return self


class Capture(SnappiObject):
    __slots__ = ()

    _TYPES = {
        'basic': 'CaptureBasicFilterList',
    }

    BASIC = 'basic'
    PCAP = 'pcap'

    PCAP = 'pcap'
    PCAPNG = 'pcapng'

    def __init__(self, port_names=None, enable=None, overwrite=None, format=None, name=None):
        super(Capture, self).__init__()
        self.port_names = port_names
        self.enable = enable
        self.overwrite = overwrite
        self.format = format
        self.name = name

    @property
    def port_names(self):
        # type: () -> list[str]
        """port_names getter

        The unique names of ports that the capture settings will apply to.

        Returns: list[str]
        """
        return self._properties['port_names']

    @port_names.setter
    def port_names(self, value):
        """port_names setter

        The unique names of ports that the capture settings will apply to.

        value: list[str]
        """
        self._properties['port_names'] = value

    @property
    def choice(self):
        # type: () -> Union[basic, pcap, choice, choice, choice, choice]
        """choice getter

        The type of filter.

        Returns: Union[basic, pcap, choice, choice, choice, choice]
        """
        return self._properties['choice']

    @choice.setter
    def choice(self, value):
        """choice setter

        The type of filter.

        value: Union[basic, pcap, choice, choice, choice, choice]
        """
        self._properties['choice'] = value

    @property
    def basic(self):
        # type: () -> CaptureBasicFilterList
        """basic getter

        An array of basic filters. The filters supported are source address, destination address and custom. 

        Returns: list[obj(snappi.CaptureBasicFilter)]
        """
        if 'basic' not in self._properties or self._properties['basic'] is None:
            self._properties['basic'] = CaptureBasicFilterList()
        return self._properties['basic']

    @property
    def pcap(self):
        # type: () -> str
        """pcap getter

        The content of this property must be of pcap filter syntax. https://www.tcpdump.org/manpages/pcap-filter.7.html

        Returns: str
        """
        return self._properties['pcap']

    @pcap.setter
    def pcap(self, value):
        """pcap setter

        The content of this property must be of pcap filter syntax. https://www.tcpdump.org/manpages/pcap-filter.7.html

        value: str
        """
        self._properties['choice'] = 'pcap'
        self._properties['pcap'] = value

    @property
    def enable(self):
        # type: () -> boolean
        """enable getter

        Enable capture on the port.

        Returns: boolean
        """
        return self._properties['enable']

    @enable.setter
    def enable(self, value):
        """enable setter

        Enable capture on the port.

        value: boolean
        """
        self._properties['enable'] = value

    @property
    def overwrite(self):
        # type: () -> boolean
        """overwrite getter

        Overwrite the capture buffer.

        Returns: boolean
        """
        return self._properties['overwrite']

    @overwrite.setter
    def overwrite(self, value):
        """overwrite setter

        Overwrite the capture buffer.

        value: boolean
        """
        self._properties['overwrite'] = value

    @property
    def format(self):
        # type: () -> Union[pcap, pcapng]
        """format getter

        The format of the capture file.

        Returns: Union[pcap, pcapng]
        """
        return self._properties['format']

    @format.setter
    def format(self, value):
        """format setter

        The format of the capture file.

        value: Union[pcap, pcapng]
        """
        self._properties['format'] = value

    @property
    def name(self):
        # type: () -> str
        """name getter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        Returns: str
        """
        return self._properties['name']

    @name.setter
    def name(self, value):
        """name setter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        value: str
        """
        self._properties['name'] = value


class CaptureBasicFilter(SnappiObject):
    __slots__ = ()

    _TYPES = {
        'mac_address': 'CaptureMacAddressFilter',
        'custom': 'CaptureCustomFilter',
    }

    MAC_ADDRESS = 'mac_address'
    CUSTOM = 'custom'

    def __init__(self, and_operator=None, not_operator=None):
        super(CaptureBasicFilter, self).__init__()
        self.and_operator = and_operator
        self.not_operator = not_operator

    @property
    def mac_address(self):
        # type: () -> CaptureMacAddressFilter
        """Factory method to create an instance of the CaptureMacAddressFilter class

        A container for a mac address capture filter.
        """
        if 'mac_address' not in self._properties or self._properties['mac_address'] is None:
            self._properties['mac_address'] = CaptureMacAddressFilter()
        self.choice = 'mac_address'
        return self._properties['mac_address']

    @property
    def custom(self):
        # type: () -> CaptureCustomFilter
        """Factory method to create an instance of the CaptureCustomFilter class

        A container for a custom capture filter.
        """
        if 'custom' not in self._properties or self._properties['custom'] is None:
            self._properties['custom'] = CaptureCustomFilter()
        self.choice = 'custom'
        return self._properties['custom']

    @property
    def choice(self):
        # type: () -> Union[mac_address, custom, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[mac_address, custom, choice, choice, choice]
        """
        return self._properties['choice']

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[mac_address, custom, choice, choice, choice]
        """
        self._properties['choice'] = value

    @property
    def and_operator(self):
        # type: () -> boolean
        """and_operator getter

        TBD

        Returns: boolean
        """
        return self._properties['and_operator']

    @and_operator.setter
    def and_operator(self, value):
        """and_operator setter

        TBD

        value: boolean
        """
        self._properties['and_operator'] = value

    @property
    def not_operator(self):
        # type: () -> boolean
        """not_operator getter

        TBD

        Returns: boolean
        """
        return self._properties['not_operator']

    @not_operator.setter
    def not_operator(self, value):
        """not_operator setter

        TBD

        value: boolean
        """
        self._properties['not_operator'] = value


class CaptureMacAddressFilter(SnappiObject):
    __slots__ = ()

    SOURCE = 'source'
    DESTINATION = 'destination'

    def __init__(self, mac=None, filter=None, mask=None):
        super(CaptureMacAddressFilter, self).__init__()
        self.mac = mac
        self.filter = filter
        self.mask = mask

    @property
    def mac(self):
        # type: () -> Union[source, destination]
        """mac getter

        The type of mac address filters. This can be either source or destination.

        Returns: Union[source, destination]
        """
        return self._properties['mac']

    @mac.setter
    def mac(self, value):
        """mac setter

        The type of mac address filters. This can be either source or destination.

        value: Union[source, destination]
        """
        self._properties['mac'] = value

    @property
    def filter(self):
        # type: () -> str
        """filter getter

        The value of the mac address.

        Returns: str
        """
        return self._properties['filter']

    @filter.setter
    def filter(self, value):
        """filter setter

        The value of the mac address.

        value: str
        """
        self._properties['filter'] = value

    @property
    def mask(self):
        # type: () -> str
        """mask getter

        The value of the mask to be applied to the mac address.

        Returns: str
        """
        return self._properties['mask']

    @mask.setter
    def mask(self, value):
        """mask setter

        The value of the mask to be applied to the mac address.

        value: str
        """
        self._properties['mask'] = value


class CaptureCustomFilter(SnappiObject):
    __slots__ = ()

    def __init__(self, filter=None, mask=None, offset=None):
        super(CaptureCustomFilter, self).__init__()
        self.filter = filter
        self.mask = mask
        self.offset = offset

    @property
    def filter(self):
        # type: () -> str
        """filter getter

        The value to filter on.

        Returns: str
        """
        return self._properties['filter']

    @filter.setter
    def filter(self, value):
        """filter setter

        The value to filter on.

        value: str
        """
        self._properties['filter'] = value

    @property
    def mask(self):
        # type: () -> str
        """mask getter

        The mask to be applied to the filter.

        Returns: str
        """
        return self._properties['mask']

    @mask.setter
    def mask(self, value):
        """mask setter

        The mask to be applied to the filter.

        value: str
        """
        self._properties['mask'] = value

    @property
    def offset(self):
        # type: () -> int
        """offset getter

        The offset in the packet to filter at.

        Returns: int
        """
        return self._properties['offset']

    @offset.setter
    def offset(self, value):
        """offset setter

        The offset in the packet to filter at.

        value: int
        """
        self._properties['offset'] = value


class CaptureBasicFilterList(SnappiList):
    __slots__ = ()

    def __init__(self):
        super(CaptureBasicFilterList, self).__init__()

    def __getitem__(self, key):
        # type: (int) -> CaptureBasicFilter
        return self._getitem(key)

    def __iter__(self):
        # type: () -> CaptureBasicFilterList
        return self._iter()

    def __next__(self):
        # type: () -> CaptureBasicFilter
        return self._next()

    def next(self):
        # type: () -> CaptureBasicFilter
        return self._next()

    def basicfilter(self, and_operator=True, not_operator=False):
        # type: () -> CaptureBasicFilterList
        """Factory method that creates an instance of CaptureBasicFilter class

        A container for different types of basic capture filters.
        """
        item = CaptureBasicFilter(and_operator, not_operator)
        self._add(item)
        return self

    def mac_address(self, mac='None', filter=None, mask=None):
        # type: () -> CaptureBasicFilterList
        """Factory method that creates an instance of CaptureMacAddressFilter class

        A container for a mac address capture filter.
        """
        item = CaptureBasicFilter()
        item.mac_address
        self._add(item)
        return self

    def custom(self, filter=None, mask=None, offset=None):
        # type: () -> CaptureBasicFilterList
        """Factory method that creates an instance of CaptureCustomFilter class

        A container for a custom capture filter.
        """
        item = CaptureBasicFilter()
        item.custom
        self._add(item)
        return self


class CaptureList(SnappiList):
    __slots__ = ()

    def __init__(self):
        super(CaptureList, self).__init__()

    def __getitem__(self, key):
        # type: (int) -> Capture
        return self._getitem(key)

    def __iter__(self):
        # type: () -> CaptureList
        return self._iter()

    def __next__(self):
        # type: () -> Capture
        return self._next()

    def next(self):
        # type: () -> Capture
        return self._next()

    def capture(self, port_names=None, pcap=None, enable=True, overwrite=False, format='pcap', name=None):
        # type: () -> CaptureList
        """Factory method that creates an instance of Capture class

        Container for capture settings.
        """
        item = Capture(port_names, pcap, enable, overwrite, format, name)
        self._add(item)
        return self


class Device(SnappiObject):
    __slots__ = ()

    _TYPES = {
        'ethernet': 'DeviceEthernet',
        'ipv4': 'DeviceContainerIpv4',
        'ipv6': 'DeviceIpv6',
        'bgpv4': 'DeviceBgpv4',
    }

    ETHERNET = 'ethernet'
    IPV4 = 'ipv4'
    IPV6 = 'ipv6'
    BGPV4 = 'bgpv4'

    def __init__(self, container_name=None, device_count=None, name=None):
        super(Device, self).__init__()
        self.container_name = container_name
        self.device_count = device_count
        self.name = name

    @property
    def ethernet(self):
        # type: () -> DeviceEthernet
        """Factory method to create an instance of the DeviceEthernet class

        Emulated ethernet protocol. A top level in the emulated device stack.
        """
        if 'ethernet' not in self._properties or self._properties['ethernet'] is None:
            self._properties['ethernet'] = DeviceEthernet()
        self.choice = 'ethernet'
        return self._properties['ethernet']

    @property
    def ipv4(self):
        # type: () -> DeviceContainerIpv4
        """Factory method to create an instance of the DeviceContainerIpv4 class

        Emulated ipv4 protocol
        """
        if 'ipv4' not in self._properties or self._properties['ipv4'] is None:
            self._properties['ipv4'] = DeviceContainerIpv4()
        self.choice = 'ipv4'
        return self._properties['ipv4']

    @property
    def ipv6(self):
        # type: () -> DeviceIpv6
        """Factory method to create an instance of the DeviceIpv6 class

        Emulated ipv6 protocol
        """
        if 'ipv6' not in self._properties or self._properties['ipv6'] is None:
            self._properties['ipv6'] = DeviceIpv6()
        self.choice = 'ipv6'
        return self._properties['ipv6']

    @property
    def bgpv4(self):
        # type: () -> DeviceBgpv4
        """Factory method to create an instance of the DeviceBgpv4 class

        Emulated BGPv4 router and routes
        """
        if 'bgpv4' not in self._properties or self._properties['bgpv4'] is None:
            self._properties['bgpv4'] = DeviceBgpv4()
        self.choice = 'bgpv4'
        return self._properties['bgpv4']

    @property
    def container_name(self):
        # type: () -> str
        """container_name getter

        The unique name of a Port or Lag object that will contain the emulated interfaces and/or devices.

        Returns: str
        """
        return self._properties['container_name']

    @container_name.setter
    def container_name(self, value):
        """container_name setter

        The unique name of a Port or Lag object that will contain the emulated interfaces and/or devices.

        value: str
        """
        self._properties['container_name'] = value

    @property
    def device_count(self):
        # type: () -> int
        """device_count getter

        The number of emulated protocol devices or interfaces per port.. For example if the device_count is 10 and the choice property value is ethernet then an implementation MUST create 10 ethernet interfaces. The ethernet property is a container for src, dst and eth_type properties with each on of those properties being a pattern container for 10 possible values. . If an implementation is unable to support the maximum device_count it MUST indicate what the maximum device_count is using the /results/capabilities API.. The device_count is also used by the individual child properties that are a container for a /components/schemas/Device.Pattern.

        Returns: int
        """
        return self._properties['device_count']

    @device_count.setter
    def device_count(self, value):
        """device_count setter

        The number of emulated protocol devices or interfaces per port.. For example if the device_count is 10 and the choice property value is ethernet then an implementation MUST create 10 ethernet interfaces. The ethernet property is a container for src, dst and eth_type properties with each on of those properties being a pattern container for 10 possible values. . If an implementation is unable to support the maximum device_count it MUST indicate what the maximum device_count is using the /results/capabilities API.. The device_count is also used by the individual child properties that are a container for a /components/schemas/Device.Pattern.

        value: int
        """
        self._properties['device_count'] = value

    @property
    def choice(self):
        # type: () -> Union[ethernet, ipv4, ipv6, bgpv4, choice, choice, choice, choice, choice]
        """choice getter

        The type of emulated protocol interface or device.

        Returns: Union[ethernet, ipv4, ipv6, bgpv4, choice, choice, choice, choice, choice]
        """
        return self._properties['choice']

    @choice.setter
    def choice(self, value):
        """choice setter

        The type of emulated protocol interface or device.

        value: Union[ethernet, ipv4, ipv6, bgpv4, choice, choice, choice, choice, choice]
        """
        self._properties['choice'] = value

    @property
    def name(self):
        # type: () -> str
        """name getter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        Returns: str
        """
        return self._properties['name']

    @name.setter
    def name(self, value):
        """name setter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        value: str
        """
        self._properties['name'] = value


class DeviceContainerIpv4(SnappiObject):
    __slots__ = ()

    _TYPES = {
        'ethernet': 'DeviceEthernet',
        'address': 'DevicePattern',
        'gateway': 'DevicePattern',
        'prefix': 'DevicePattern',
    }

    def __init__(self, name=None):
        super(DeviceContainerIpv4, self).__init__()
        self.name = name

    @property
    def ethernet(self):
        # type: () -> DeviceEthernet
        """ethernet getter

        Emulated ethernet protocol. A top level in the emulated device stack.Emulated ethernet protocol. A top level in the emulated device stack.

        Returns: obj(snappi.DeviceEthernet)
        """
        if 'ethernet' not in self._properties or self._properties['ethernet'] is None:
            self._properties['ethernet'] = DeviceEthernet()
        return self._properties['ethernet']

    @property
    def address(self):
        # type: () -> DevicePattern
        """address getter

        A container for emulated device property patterns.A container for emulated device property patterns.The ipv4 address.

        Returns: obj(snappi.DevicePattern)
        """
        if 'address' not in self._properties or self._properties['address'] is None:
            self._properties['address'] = DevicePattern()
        return self._properties['address']

    @property
    def gateway(self):
        # type: () -> DevicePattern
        """gateway getter

        A container for emulated device property patterns.A container for emulated device property patterns.The ipv4 address of the gateway.

        Returns: obj(snappi.DevicePattern)
        """
        if 'gateway' not in self._properties or self._properties['gateway'] is None:
            self._properties['gateway'] = DevicePattern()
        return self._properties['gateway']

    @property
    def prefix(self):
        # type: () -> DevicePattern
        """prefix getter

        A container for emulated device property patterns.A container for emulated device property patterns.The prefix of the ipv4 address.

        Returns: obj(snappi.DevicePattern)
        """
        if 'prefix' not in self._properties or self._properties['prefix'] is None:
            self._properties['prefix'] = DevicePattern()
        return self._properties['prefix']

    @property
    def name(self):
        # type: () -> str
        """name getter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        Returns: str
        """
        return self._properties['name']

    @name.setter
    def name(self, value):
        """name setter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        value: str
        """
        self._properties['name'] = value


class DeviceIpv6(SnappiObject):
    __slots__ = ()

    _TYPES = {
        'address': 'DevicePattern',
        'gateway': 'DevicePattern',
        'prefix': 'DevicePattern',
        'ethernet': 'DeviceEthernet',
    }

    def __init__(self, name=None):
        super(DeviceIpv6, self).__init__()
        self.name = name

    @property
    def address(self):
        # type: () -> DevicePattern
        """address getter

        A container for emulated device property patterns.A container for emulated device property patterns.

        Returns: obj(snappi.DevicePattern)
        """
        if 'address' not in self._properties or self._properties['address'] is None:
            self._properties['address'] = DevicePattern()
        return self._properties['address']

    @property
    def gateway(self):
        # type: () -> DevicePattern
        """gateway getter

        A container for emulated device property patterns.A container for emulated device property patterns.

        Returns: obj(snappi.DevicePattern)
        """
        if 'gateway' not in self._properties or self._properties['gateway'] is None:
            self._properties['gateway'] = DevicePattern()
        return self._properties['gateway']

    @property
    def prefix(self):
        # type: () -> DevicePattern
        """prefix getter

        A container for emulated device property patterns.A container for emulated device property patterns.

        Returns: obj(snappi.DevicePattern)
        """
        if 'prefix' not in self._properties or self._properties['prefix'] is None:
            self._properties['prefix'] = DevicePattern()
        return self._properties['prefix']

    @property
    def ethernet(self):
        # type: () -> DeviceEthernet
        """ethernet getter

        Emulated ethernet protocol. A top level in the emulated device stack.Emulated ethernet protocol. A top level in the emulated device stack.

        Returns: obj(snappi.DeviceEthernet)
        """
        if 'ethernet' not in self._properties or self._properties['ethernet'] is None:
            self._properties['ethernet'] = DeviceEthernet()
        return self._properties['ethernet']

    @property
    def name(self):
        # type: () -> str
        """name getter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        Returns: str
        """
        return self._properties['name']

    @name.setter
    def name(self, value):
        """name setter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        value: str
        """
        self._properties['name'] = value


class DeviceBgpv4(SnappiObject):
    __slots__ = ()

    _TYPES = {
        'router_id': 'DevicePattern',
        'as_number': 'DevicePattern',
        'hold_time_interval': 'DevicePattern',
        'keep_alive_interval': 'DevicePattern',
        'dut_ipv4_address': 'DevicePattern',
        'dut_as_number': 'DevicePattern',
        'ipv4': 'DeviceContainerIpv4',
        'bgpv4_route_ranges': 'DeviceBgpv4RouteRangeList',
        'bgpv6_route_ranges': 'DeviceBgpv6RouteRangeList',
    }

    IBGP = 'ibgp'
    EBGP = 'ebgp'

    def __init__(self, as_type=None, name=None):
        super(DeviceBgpv4, self).__init__()
        self.as_type = as_type
        self.name = name

    @property
    def router_id(self):
        # type: () -> DevicePattern
        """router_id getter

        A container for emulated device property patterns.A container for emulated device property patterns.specifies BGP router identifier. It must be the string representation of an IPv4 address 

        Returns: obj(snappi.DevicePattern)
        """
        if 'router_id' not in self._properties or self._properties['router_id'] is None:
            self._properties['router_id'] = DevicePattern()
        return self._properties['router_id']

    @property
    def as_number(self):
        # type: () -> DevicePattern
        """as_number getter

        A container for emulated device property patterns.A container for emulated device property patterns.Autonomous system (AS) number of 4 byte

        Returns: obj(snappi.DevicePattern)
        """
        if 'as_number' not in self._properties or self._properties['as_number'] is None:
            self._properties['as_number'] = DevicePattern()
        return self._properties['as_number']

    @property
    def as_type(self):
        # type: () -> Union[ibgp, ebgp]
        """as_type getter

        The type of BGP autonomous system. External BGP (EBGP) is used for BGP links between two or more autonomous systems. Internal BGP (IBGP) is used within a single autonomous system.

        Returns: Union[ibgp, ebgp]
        """
        return self._properties['as_type']

    @as_type.setter
    def as_type(self, value):
        """as_type setter

        The type of BGP autonomous system. External BGP (EBGP) is used for BGP links between two or more autonomous systems. Internal BGP (IBGP) is used within a single autonomous system.

        value: Union[ibgp, ebgp]
        """
        self._properties['as_type'] = value

    @property
    def hold_time_interval(self):
        # type: () -> DevicePattern
        """hold_time_interval getter

        A container for emulated device property patterns.A container for emulated device property patterns.Number of seconds the sender proposes for the value of the Hold Timer

        Returns: obj(snappi.DevicePattern)
        """
        if 'hold_time_interval' not in self._properties or self._properties['hold_time_interval'] is None:
            self._properties['hold_time_interval'] = DevicePattern()
        return self._properties['hold_time_interval']

    @property
    def keep_alive_interval(self):
        # type: () -> DevicePattern
        """keep_alive_interval getter

        A container for emulated device property patterns.A container for emulated device property patterns.Number of seconds between transmissions of Keep Alive messages by router

        Returns: obj(snappi.DevicePattern)
        """
        if 'keep_alive_interval' not in self._properties or self._properties['keep_alive_interval'] is None:
            self._properties['keep_alive_interval'] = DevicePattern()
        return self._properties['keep_alive_interval']

    @property
    def dut_ipv4_address(self):
        # type: () -> DevicePattern
        """dut_ipv4_address getter

        A container for emulated device property patterns.A container for emulated device property patterns.IPv4 address of the BGP peer for the session

        Returns: obj(snappi.DevicePattern)
        """
        if 'dut_ipv4_address' not in self._properties or self._properties['dut_ipv4_address'] is None:
            self._properties['dut_ipv4_address'] = DevicePattern()
        return self._properties['dut_ipv4_address']

    @property
    def dut_as_number(self):
        # type: () -> DevicePattern
        """dut_as_number getter

        A container for emulated device property patterns.A container for emulated device property patterns.Autonomous system (AS) number of the BGP peer router (DUT)

        Returns: obj(snappi.DevicePattern)
        """
        if 'dut_as_number' not in self._properties or self._properties['dut_as_number'] is None:
            self._properties['dut_as_number'] = DevicePattern()
        return self._properties['dut_as_number']

    @property
    def ipv4(self):
        # type: () -> DeviceContainerIpv4
        """ipv4 getter

        Emulated ipv4 protocolEmulated ipv4 protocolThe ipv4 stack that the bgp4 protocol is implemented over.

        Returns: obj(snappi.DeviceContainerIpv4)
        """
        if 'ipv4' not in self._properties or self._properties['ipv4'] is None:
            self._properties['ipv4'] = DeviceContainerIpv4()
        return self._properties['ipv4']

    @property
    def bgpv4_route_ranges(self):
        # type: () -> DeviceBgpv4RouteRangeList
        """bgpv4_route_ranges getter

        Emulated bgpv4 route ranges

        Returns: list[obj(snappi.DeviceBgpv4RouteRange)]
        """
        if 'bgpv4_route_ranges' not in self._properties or self._properties['bgpv4_route_ranges'] is None:
            self._properties['bgpv4_route_ranges'] = DeviceBgpv4RouteRangeList()
        return self._properties['bgpv4_route_ranges']

    @property
    def bgpv6_route_ranges(self):
        # type: () -> DeviceBgpv6RouteRangeList
        """bgpv6_route_ranges getter

        Emulated bgpv6 route ranges

        Returns: list[obj(snappi.DeviceBgpv6RouteRange)]
        """
        if 'bgpv6_route_ranges' not in self._properties or self._properties['bgpv6_route_ranges'] is None:
            self._properties['bgpv6_route_ranges'] = DeviceBgpv6RouteRangeList()
        return self._properties['bgpv6_route_ranges']

    @property
    def name(self):
        # type: () -> str
        """name getter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        Returns: str
        """
        return self._properties['name']

    @name.setter
    def name(self, value):
        """name setter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        value: str
        """
        self._properties['name'] = value


class DeviceBgpv4RouteRange(SnappiObject):
    __slots__ = ()

    _TYPES = {
        'address': 'DevicePattern',
        'prefix': 'DevicePattern',
        'as_path': 'DevicePattern',
        'next_hop_address': 'DevicePattern',
        'community': 'DevicePattern',
    }

    def __init__(self, route_count_per_device=None, name=None):
        super(DeviceBgpv4RouteRange, self).__init__()
        self.route_count_per_device = route_count_per_device
        self.name = name

    @property
    def route_count_per_device(self):
        # type: () -> int
        """route_count_per_device getter

        The number of routes per device.

        Returns: int
        """
        return self._properties['route_count_per_device']

    @route_count_per_device.setter
    def route_count_per_device(self, value):
        """route_count_per_device setter

        The number of routes per device.

        value: int
        """
        self._properties['route_count_per_device'] = value

    @property
    def address(self):
        # type: () -> DevicePattern
        """address getter

        A container for emulated device property patterns.The network address of the first network

        Returns: obj(snappi.DevicePattern)
        """
        if 'address' not in self._properties or self._properties['address'] is None:
            self._properties['address'] = DevicePattern()
        return self._properties['address']

    @property
    def prefix(self):
        # type: () -> DevicePattern
        """prefix getter

        A container for emulated device property patterns.Ipv4 prefix length with minimum value is 0 to maximum value is 32

        Returns: obj(snappi.DevicePattern)
        """
        if 'prefix' not in self._properties or self._properties['prefix'] is None:
            self._properties['prefix'] = DevicePattern()
        return self._properties['prefix']

    @property
    def as_path(self):
        # type: () -> DevicePattern
        """as_path getter

        A container for emulated device property patterns.Autonomous Systems (AS) numbers that a route passes through to reach the destination

        Returns: obj(snappi.DevicePattern)
        """
        if 'as_path' not in self._properties or self._properties['as_path'] is None:
            self._properties['as_path'] = DevicePattern()
        return self._properties['as_path']

    @property
    def next_hop_address(self):
        # type: () -> DevicePattern
        """next_hop_address getter

        A container for emulated device property patterns.IP Address of next router to forward a packet to its final destination

        Returns: obj(snappi.DevicePattern)
        """
        if 'next_hop_address' not in self._properties or self._properties['next_hop_address'] is None:
            self._properties['next_hop_address'] = DevicePattern()
        return self._properties['next_hop_address']

    @property
    def community(self):
        # type: () -> DevicePattern
        """community getter

        A container for emulated device property patterns.BGP communities provide additional capability for tagging routes and for modifying BGP routing policy on upstream and downstream routers BGP community is a 32-bit number which broken into 16-bit As and 16-bit custom value Please specify those two values in this string format 65000:100

        Returns: obj(snappi.DevicePattern)
        """
        if 'community' not in self._properties or self._properties['community'] is None:
            self._properties['community'] = DevicePattern()
        return self._properties['community']

    @property
    def name(self):
        # type: () -> str
        """name getter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        Returns: str
        """
        return self._properties['name']

    @name.setter
    def name(self, value):
        """name setter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        value: str
        """
        self._properties['name'] = value


class DeviceBgpv4RouteRangeList(SnappiList):
    __slots__ = ()

    def __init__(self):
        super(DeviceBgpv4RouteRangeList, self).__init__()

    def __getitem__(self, key):
        # type: (int) -> DeviceBgpv4RouteRange
        return self._getitem(key)

    def __iter__(self):
        # type: () -> DeviceBgpv4RouteRangeList
        return self._iter()

    def __next__(self):
        # type: () -> DeviceBgpv4RouteRange
        return self._next()

    def next(self):
        # type: () -> DeviceBgpv4RouteRange
        return self._next()

    def bgpv4routerange(self, route_count_per_device=1, name=None):
        # type: () -> DeviceBgpv4RouteRangeList
        """Factory method that creates an instance of DeviceBgpv4RouteRange class

        Emulated bgpv4 route range
        """
        item = DeviceBgpv4RouteRange(route_count_per_device, name)
        self._add(item)
        return self


class DeviceBgpv6RouteRange(SnappiObject):
    __slots__ = ()

    _TYPES = {
        'address': 'DevicePattern',
        'prefix': 'DevicePattern',
        'as_path': 'DevicePattern',
        'next_hop_address': 'DevicePattern',
        'community': 'DevicePattern',
    }

    def __init__(self, route_count_per_device=None, name=None):
        super(DeviceBgpv6RouteRange, self).__init__()
        self.route_count_per_device = route_count_per_device
        self.name = name

    @property
    def route_count_per_device(self):
        # type: () -> int
        """route_count_per_device getter

        The number of routes per device.

        Returns: int
        """
        return self._properties['route_count_per_device']

    @route_count_per_device.setter
    def route_count_per_device(self, value):
        """route_count_per_device setter

        The number of routes per device.

        value: int
        """
        self._properties['route_count_per_device'] = value

    @property
    def address(self):
        # type: () -> DevicePattern
        """address getter

        A container for emulated device property patterns.The network address of the first network

        Returns: obj(snappi.DevicePattern)
        """
        if 'address' not in self._properties or self._properties['address'] is None:
            self._properties['address'] = DevicePattern()
        return self._properties['address']

    @property
    def prefix(self):
        # type: () -> DevicePattern
        """prefix getter

        A container for emulated device property patterns.Ipv6 prefix length with minimum value is 0 to maximum value is 128

        Returns: obj(snappi.DevicePattern)
        """
        if 'prefix' not in self._properties or self._properties['prefix'] is None:
            self._properties['prefix'] = DevicePattern()
        return self._properties['prefix']

    @property
    def as_path(self):
        # type: () -> DevicePattern
        """as_path getter

        A container for emulated device property patterns.Autonomous Systems (AS) numbers that a route passes through to reach the destination

        Returns: obj(snappi.DevicePattern)
        """
        if 'as_path' not in self._properties or self._properties['as_path'] is None:
            self._properties['as_path'] = DevicePattern()
        return self._properties['as_path']

    @property
    def next_hop_address(self):
        # type: () -> DevicePattern
        """next_hop_address getter

        A container for emulated device property patterns.IP Address of next router to forward a packet to its final destination

        Returns: obj(snappi.DevicePattern)
        """
        if 'next_hop_address' not in self._properties or self._properties['next_hop_address'] is None:
            self._properties['next_hop_address'] = DevicePattern()
        return self._properties['next_hop_address']

    @property
    def community(self):
        # type: () -> DevicePattern
        """community getter

        A container for emulated device property patterns.BGP communities provide additional capability for tagging routes and for modifying BGP routing policy on upstream and downstream routers BGP community is a 32-bit number which broken into 16-bit As and 16-bit custom value Please specify those two values in this string format 65000:100

        Returns: obj(snappi.DevicePattern)
        """
        if 'community' not in self._properties or self._properties['community'] is None:
            self._properties['community'] = DevicePattern()
        return self._properties['community']

    @property
    def name(self):
        # type: () -> str
        """name getter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        Returns: str
        """
        return self._properties['name']

    @name.setter
    def name(self, value):
        """name setter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        value: str
        """
        self._properties['name'] = value


class DeviceBgpv6RouteRangeList(SnappiList):
    __slots__ = ()

    def __init__(self):
        super(DeviceBgpv6RouteRangeList, self).__init__()

    def __getitem__(self, key):
        # type: (int) -> DeviceBgpv6RouteRange
        return self._getitem(key)

    def __iter__(self):
        # type: () -> DeviceBgpv6RouteRangeList
        return self._iter()

    def __next__(self):
        # type: () -> DeviceBgpv6RouteRange
        return self._next()

    def next(self):
        # type: () -> DeviceBgpv6RouteRange
        return self._next()

    def bgpv6routerange(self, route_count_per_device=1, name=None):
        # type: () -> DeviceBgpv6RouteRangeList
        """Factory method that creates an instance of DeviceBgpv6RouteRange class

        Emulated bgpv6 route range
        """
        item = DeviceBgpv6RouteRange(route_count_per_device, name)
        self._add(item)
        return self


class DeviceList(SnappiList):
    __slots__ = ()

    def __init__(self):
        super(DeviceList, self).__init__()

    def __getitem__(self, key):
        # type: (int) -> Device
        return self._getitem(key)

    def __iter__(self):
        # type: () -> DeviceList
        return self._iter()

    def __next__(self):
        # type: () -> Device
        return self._next()

    def next(self):
        # type: () -> Device
        return self._next()

    def device(self, container_name=None, device_count=1, name=None):
        # type: () -> DeviceList
        """Factory method that creates an instance of Device class

        A container for emulated protocol devices.
        """
        item = Device(container_name, device_count, name)
        self._add(item)
        return self

    def ethernet(self, name=None):
        # type: () -> DeviceList
        """Factory method that creates an instance of DeviceEthernet class

        Emulated ethernet protocol. A top level in the emulated device stack.
        """
        item = Device()
        item.ethernet
        self._add(item)
        return self

    def ipv4(self, name=None):
        # type: () -> DeviceList
        """Factory method that creates an instance of DeviceContainerIpv4 class

        Emulated ipv4 protocol
        """
        item = Device()
        item.ipv4
        self._add(item)
        return self

    def ipv6(self, name=None):
        # type: () -> DeviceList
        """Factory method that creates an instance of DeviceIpv6 class

        Emulated ipv6 protocol
        """
        item = Device()
        item.ipv6
        self._add(item)
        return self

    def bgpv4(self, as_type='None', name=None):
        # type: () -> DeviceList
        """Factory method that creates an instance of DeviceBgpv4 class

        Emulated BGPv4 router and routes
        """
        item = Device()
        item.bgpv4
        self._add(item)
        return self


class Flow(SnappiObject):
    __slots__ = ()

    _TYPES = {
        'tx_rx': 'FlowTxRx',
        'packet': 'FlowHeaderList',
        'size': 'FlowSize',
        'rate': 'FlowRate',
        'duration': 'FlowDuration',
    }

    def __init__(self, name=None):
        super(Flow, self).__init__()
        self.name = name

    @property
    def tx_rx(self):
        # type: () -> FlowTxRx
        """tx_rx getter

        A container for different types of transmit and receive endpoint containers.The transmit and receive endpoints.

        Returns: obj(snappi.FlowTxRx)
        """
        if 'tx_rx' not in self._properties or self._properties['tx_rx'] is None:
            self._properties['tx_rx'] = FlowTxRx()
        return self._properties['tx_rx']

    @property
    def packet(self):
        # type: () -> FlowHeaderList
        """packet getter

        The header is a list of traffic protocol headers. The order of traffic protocol headers assigned to the list is the order they will appear on the wire.

        Returns: list[obj(snappi.FlowHeader)]
        """
        if 'packet' not in self._properties or self._properties['packet'] is None:
            self._properties['packet'] = FlowHeaderList()
        return self._properties['packet']

    @property
    def size(self):
        # type: () -> FlowSize
        """size getter

        The frame size which overrides the total length of the packetThe size of the packets.

        Returns: obj(snappi.FlowSize)
        """
        if 'size' not in self._properties or self._properties['size'] is None:
            self._properties['size'] = FlowSize()
        return self._properties['size']

    @property
    def rate(self):
        # type: () -> FlowRate
        """rate getter

        The rate of packet transmissionThe transmit rate of the packets.

        Returns: obj(snappi.FlowRate)
        """
        if 'rate' not in self._properties or self._properties['rate'] is None:
            self._properties['rate'] = FlowRate()
        return self._properties['rate']

    @property
    def duration(self):
        # type: () -> FlowDuration
        """duration getter

        A container for different transmit durations. The transmit duration of the packets.

        Returns: obj(snappi.FlowDuration)
        """
        if 'duration' not in self._properties or self._properties['duration'] is None:
            self._properties['duration'] = FlowDuration()
        return self._properties['duration']

    @property
    def name(self):
        # type: () -> str
        """name getter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        Returns: str
        """
        return self._properties['name']

    @name.setter
    def name(self, value):
        """name setter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        value: str
        """
        self._properties['name'] = value


class FlowTxRx(SnappiObject):
    __slots__ = ()

    _TYPES = {
        'port': 'FlowPort',
        'device': 'FlowDevice',
    }

    PORT = 'port'
    DEVICE = 'device'

    def __init__(self):
        super(FlowTxRx, self).__init__()

    @property
    def port(self):
        # type: () -> FlowPort
        """Factory method to create an instance of the FlowPort class

        A container for a transmit port and 0..n intended receive ports. When assigning this container to a flow the flows's packet headers will not be populated with any address resolution information such as source and/or destination addresses. For example Flow.Ethernet dst mac address values will be defaulted to 0. For full control over the Flow.properties.packet header contents use this container. 
        """
        if 'port' not in self._properties or self._properties['port'] is None:
            self._properties['port'] = FlowPort()
        self.choice = 'port'
        return self._properties['port']

    @property
    def device(self):
        # type: () -> FlowDevice
        """Factory method to create an instance of the FlowDevice class

        A container for 1..n transmit devices and 1..n receive devices. Implemementations may use learned information from the devices to pre-populate Flow.properties.packet[Flow.Header fields].. For example an implementation may automatically start devices, get arp table information and pre-populate the Flow.Ethernet dst mac address values.. To discover what the implementation supports use the /results/capabilities API.
        """
        if 'device' not in self._properties or self._properties['device'] is None:
            self._properties['device'] = FlowDevice()
        self.choice = 'device'
        return self._properties['device']

    @property
    def choice(self):
        # type: () -> Union[port, device, choice, choice, choice]
        """choice getter

        The type of transmit and receive container used by the flow.

        Returns: Union[port, device, choice, choice, choice]
        """
        return self._properties['choice']

    @choice.setter
    def choice(self, value):
        """choice setter

        The type of transmit and receive container used by the flow.

        value: Union[port, device, choice, choice, choice]
        """
        self._properties['choice'] = value


class FlowPort(SnappiObject):
    __slots__ = ()

    def __init__(self, tx_name=None, rx_name=None):
        super(FlowPort, self).__init__()
        self.tx_name = tx_name
        self.rx_name = rx_name

    @property
    def tx_name(self):
        # type: () -> str
        """tx_name getter

        The unique name of a port that is the transmit port.

        Returns: str
        """
        return self._properties['tx_name']

    @tx_name.setter
    def tx_name(self, value):
        """tx_name setter

        The unique name of a port that is the transmit port.

        value: str
        """
        self._properties['tx_name'] = value

    @property
    def rx_name(self):
        # type: () -> str
        """rx_name getter

        The unique name of a port that is the intended receive port.

        Returns: str
        """
        return self._properties['rx_name']

    @rx_name.setter
    def rx_name(self, value):
        """rx_name setter

        The unique name of a port that is the intended receive port.

        value: str
        """
        self._properties['rx_name'] = value


class FlowDevice(SnappiObject):
    __slots__ = ()

    def __init__(self, tx_names=None, rx_names=None):
        super(FlowDevice, self).__init__()
        self.tx_names = tx_names
        self.rx_names = rx_names

    @property
    def tx_names(self):
        # type: () -> list[str]
        """tx_names getter

        The unique names of devices that will be transmitting.

        Returns: list[str]
        """
        return self._properties['tx_names']

    @tx_names.setter
    def tx_names(self, value):
        """tx_names setter

        The unique names of devices that will be transmitting.

        value: list[str]
        """
        self._properties['tx_names'] = value

    @property
    def rx_names(self):
        # type: () -> list[str]
        """rx_names getter

        The unique names of emulated devices that will be receiving.

        Returns: list[str]
        """
        return self._properties['rx_names']

    @rx_names.setter
    def rx_names(self, value):
        """rx_names setter

        The unique names of emulated devices that will be receiving.

        value: list[str]
        """
        self._properties['rx_names'] = value


class FlowHeader(SnappiObject):
    __slots__ = ()

    _TYPES = {
        'custom': 'FlowCustom',
        'ethernet': 'FlowEthernet',
        'vlan': 'FlowVlan',
        'vxlan': 'FlowVxlan',
        'ipv4': 'FlowIpv4',
        'ipv6': 'FlowIpv6',
        'pfcpause': 'FlowPfcPause',
        'ethernetpause': 'FlowEthernetPause',
        'tcp': 'FlowTcp',
        'udp': 'FlowUdp',
        'gre': 'FlowGre',
        'gtpv1': 'FlowGtpv1',
        'gtpv2': 'FlowGtpv2',
    }

    CUSTOM = 'custom'
    ETHERNET = 'ethernet'
    VLAN = 'vlan'
    VXLAN = 'vxlan'
    IPV4 = 'ipv4'
    IPV6 = 'ipv6'
    PFCPAUSE = 'pfcpause'
    ETHERNETPAUSE = 'ethernetpause'
    TCP = 'tcp'
    UDP = 'udp'
    GRE = 'gre'
    GTPV1 = 'gtpv1'
    GTPV2 = 'gtpv2'

    def __init__(self):
        super(FlowHeader, self).__init__()

    @property
    def custom(self):
        # type: () -> FlowCustom
        """Factory method to create an instance of the FlowCustom class

        Custom packet header
        """
        if 'custom' not in self._properties or self._properties['custom'] is None:
            self._properties['custom'] = FlowCustom()
        self.choice = 'custom'
        return self._properties['custom']

    @property
    def ethernet(self):
        # type: () -> FlowEthernet
        """Factory method to create an instance of the FlowEthernet class

        Ethernet packet header
        """
        if 'ethernet' not in self._properties or self._properties['ethernet'] is None:
            self._properties['ethernet'] = FlowEthernet()
        self.choice = 'ethernet'
        return self._properties['ethernet']

    @property
    def vlan(self):
        # type: () -> FlowVlan
        """Factory method to create an instance of the FlowVlan class

        Vlan packet header
        """
        if 'vlan' not in self._properties or self._properties['vlan'] is None:
            self._properties['vlan'] = FlowVlan()
        self.choice = 'vlan'
        return self._properties['vlan']

    @property
    def vxlan(self):
        # type: () -> FlowVxlan
        """Factory method to create an instance of the FlowVxlan class

        Vxlan packet header
        """
        if 'vxlan' not in self._properties or self._properties['vxlan'] is None:
            self._properties['vxlan'] = FlowVxlan()
        self.choice = 'vxlan'
        return self._properties['vxlan']

    @property
    def ipv4(self):
        # type: () -> FlowIpv4
        """Factory method to create an instance of the FlowIpv4 class

        Ipv4 packet header
        """
        if 'ipv4' not in self._properties or self._properties['ipv4'] is None:
            self._properties['ipv4'] = FlowIpv4()
        self.choice = 'ipv4'
        return self._properties['ipv4']

    @property
    def ipv6(self):
        # type: () -> FlowIpv6
        """Factory method to create an instance of the FlowIpv6 class

        Ipv6 packet header
        """
        if 'ipv6' not in self._properties or self._properties['ipv6'] is None:
            self._properties['ipv6'] = FlowIpv6()
        self.choice = 'ipv6'
        return self._properties['ipv6']

    @property
    def pfcpause(self):
        # type: () -> FlowPfcPause
        """Factory method to create an instance of the FlowPfcPause class

        IEEE 802.1Qbb PFC Pause packet header. - dst: 01:80:C2:00:00:01 48bits - src: 48bits - ether_type: 0x8808 16bits - control_op_code: 0x0101 16bits - class_enable_vector: 16bits - pause_class_0: 0x0000 16bits - pause_class_1: 0x0000 16bits - pause_class_2: 0x0000 16bits - pause_class_3: 0x0000 16bits - pause_class_4: 0x0000 16bits - pause_class_5: 0x0000 16bits - pause_class_6: 0x0000 16bits - pause_class_7: 0x0000 16bits
        """
        if 'pfcpause' not in self._properties or self._properties['pfcpause'] is None:
            self._properties['pfcpause'] = FlowPfcPause()
        self.choice = 'pfcpause'
        return self._properties['pfcpause']

    @property
    def ethernetpause(self):
        # type: () -> FlowEthernetPause
        """Factory method to create an instance of the FlowEthernetPause class

        IEEE 802.3x Ethernet Pause packet header. - dst: 01:80:C2:00:00:01 48bits - src: 48bits - ether_type: 0x8808 16bits - control_op_code: 0x0001 16bits - time: 0x0000 16bits
        """
        if 'ethernetpause' not in self._properties or self._properties['ethernetpause'] is None:
            self._properties['ethernetpause'] = FlowEthernetPause()
        self.choice = 'ethernetpause'
        return self._properties['ethernetpause']

    @property
    def tcp(self):
        # type: () -> FlowTcp
        """Factory method to create an instance of the FlowTcp class

        Tcp packet header
        """
        if 'tcp' not in self._properties or self._properties['tcp'] is None:
            self._properties['tcp'] = FlowTcp()
        self.choice = 'tcp'
        return self._properties['tcp']

    @property
    def udp(self):
        # type: () -> FlowUdp
        """Factory method to create an instance of the FlowUdp class

        Udp packet header
        """
        if 'udp' not in self._properties or self._properties['udp'] is None:
            self._properties['udp'] = FlowUdp()
        self.choice = 'udp'
        return self._properties['udp']

    @property
    def gre(self):
        # type: () -> FlowGre
        """Factory method to create an instance of the FlowGre class

        Gre packet header
        """
        if 'gre' not in self._properties or self._properties['gre'] is None:
            self._properties['gre'] = FlowGre()
        self.choice = 'gre'
        return self._properties['gre']

    @property
    def gtpv1(self):
        # type: () -> FlowGtpv1
        """Factory method to create an instance of the FlowGtpv1 class

        GTPv1 packet header
        """
        if 'gtpv1' not in self._properties or self._properties['gtpv1'] is None:
            self._properties['gtpv1'] = FlowGtpv1()
        self.choice = 'gtpv1'
        return self._properties['gtpv1']

    @property
    def gtpv2(self):
        # type: () -> FlowGtpv2
        """Factory method to create an instance of the FlowGtpv2 class

        GTPv2 packet header
        """
        if 'gtpv2' not in self._properties or self._properties['gtpv2'] is None:
            self._properties['gtpv2'] = FlowGtpv2()
        self.choice = 'gtpv2'
        return self._properties['gtpv2']

    @property
    def choice(self):
        # type: () -> Union[custom, ethernet, vlan, vxlan, ipv4, ipv6, pfcpause, ethernetpause, tcp, udp, gre, gtpv1, gtpv2, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[custom, ethernet, vlan, vxlan, ipv4, ipv6, pfcpause, ethernetpause, tcp, udp, gre, gtpv1, gtpv2, choice, choice, choice]
        """
        return self._properties['choice']

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[custom, ethernet, vlan, vxlan, ipv4, ipv6, pfcpause, ethernetpause, tcp, udp, gre, gtpv1, gtpv2, choice, choice, choice]
        """
        self._properties['choice'] = value


class FlowCustom(SnappiObject):
    __slots__ = ()

    _TYPES = {
        'patterns': 'FlowBitPatternList',
    }

    def __init__(self, bytes=None):
        super(FlowCustom, self).__init__()
        self.bytes = bytes

    @property
    def bytes(self):
        # type: () -> str
        """bytes getter

        A custom packet header defined as a string of hex bytes. The string MUST contain valid hex characters. Spaces or colons can be part of the bytes but will be discarded This can be used to create a custom protocol from other inputs such as scapy, wireshark, pcap etc.. An example of ethernet/ipv4: '00000000000200000000000108004500001400010000400066e70a0000010a000002'

        Returns: str
        """
        return self._properties['bytes']

    @bytes.setter
    def bytes(self, value):
        """bytes setter

        A custom packet header defined as a string of hex bytes. The string MUST contain valid hex characters. Spaces or colons can be part of the bytes but will be discarded This can be used to create a custom protocol from other inputs such as scapy, wireshark, pcap etc.. An example of ethernet/ipv4: '00000000000200000000000108004500001400010000400066e70a0000010a000002'

        value: str
        """
        self._properties['bytes'] = value

    @property
    def patterns(self):
        # type: () -> FlowBitPatternList
        """patterns getter

        Modify the bytes with bit based patterns

        Returns: list[obj(snappi.FlowBitPattern)]
        """
        if 'patterns' not in self._properties or self._properties['patterns'] is None:
            self._properties['patterns'] = FlowBitPatternList()
        return self._properties['patterns']


class FlowBitPattern(SnappiObject):
    __slots__ = ()

    _TYPES = {
        'bitlist': 'FlowBitList',
        'bitcounter': 'FlowBitCounter',
    }

    BITLIST = 'bitlist'
    BITCOUNTER = 'bitcounter'

    def __init__(self):
        super(FlowBitPattern, self).__init__()

    @property
    def bitlist(self):
        # type: () -> FlowBitList
        """Factory method to create an instance of the FlowBitList class

        A pattern which is a list of values.
        """
        if 'bitlist' not in self._properties or self._properties['bitlist'] is None:
            self._properties['bitlist'] = FlowBitList()
        self.choice = 'bitlist'
        return self._properties['bitlist']

    @property
    def bitcounter(self):
        # type: () -> FlowBitCounter
        """Factory method to create an instance of the FlowBitCounter class

        An incrementing pattern
        """
        if 'bitcounter' not in self._properties or self._properties['bitcounter'] is None:
            self._properties['bitcounter'] = FlowBitCounter()
        self.choice = 'bitcounter'
        return self._properties['bitcounter']

    @property
    def choice(self):
        # type: () -> Union[bitlist, bitcounter, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[bitlist, bitcounter, choice, choice, choice]
        """
        return self._properties['choice']

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[bitlist, bitcounter, choice, choice, choice]
        """
        self._properties['choice'] = value


class FlowBitList(SnappiObject):
    __slots__ = ()

    def __init__(self, offset=None, length=None, count=None, values=None):
        super(FlowBitList, self).__init__()
        self.offset = offset
        self.length = length
        self.count = count
        self.values = values

    @property
    def offset(self):
        # type: () -> int
        """offset getter

        Bit offset in the packet at which the pattern will be applied

        Returns: int
        """
        return self._properties['offset']

    @offset.setter
    def offset(self, value):
        """offset setter

        Bit offset in the packet at which the pattern will be applied

        value: int
        """
        self._properties['offset'] = value

    @property
    def length(self):
        # type: () -> int
        """length getter

        The number of bits in the packet that the pattern will span

        Returns: int
        """
        return self._properties['length']

    @length.setter
    def length(self, value):
        """length setter

        The number of bits in the packet that the pattern will span

        value: int
        """
        self._properties['length'] = value

    @property
    def count(self):
        # type: () -> int
        """count getter

        The number of values to generate before repeating

        Returns: int
        """
        return self._properties['count']

    @count.setter
    def count(self, value):
        """count setter

        The number of values to generate before repeating

        value: int
        """
        self._properties['count'] = value

    @property
    def values(self):
        # type: () -> list[str]
        """values getter

        TBD

        Returns: list[str]
        """
        return self._properties['values']

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[str]
        """
        self._properties['values'] = value


class FlowBitCounter(SnappiObject):
    __slots__ = ()

    def __init__(self, offset=None, length=None, count=None, start=None, step=None):
        super(FlowBitCounter, self).__init__()
        self.offset = offset
        self.length = length
        self.count = count
        self.start = start
        self.step = step

    @property
    def offset(self):
        # type: () -> int
        """offset getter

        Bit offset in the packet at which the pattern will be applied

        Returns: int
        """
        return self._properties['offset']

    @offset.setter
    def offset(self, value):
        """offset setter

        Bit offset in the packet at which the pattern will be applied

        value: int
        """
        self._properties['offset'] = value

    @property
    def length(self):
        # type: () -> int
        """length getter

        The number of bits in the packet that the pattern will span

        Returns: int
        """
        return self._properties['length']

    @length.setter
    def length(self, value):
        """length setter

        The number of bits in the packet that the pattern will span

        value: int
        """
        self._properties['length'] = value

    @property
    def count(self):
        # type: () -> int
        """count getter

        The number of values to generate before repeating A value of 0 means the pattern will count continuously

        Returns: int
        """
        return self._properties['count']

    @count.setter
    def count(self, value):
        """count setter

        The number of values to generate before repeating A value of 0 means the pattern will count continuously

        value: int
        """
        self._properties['count'] = value

    @property
    def start(self):
        # type: () -> str
        """start getter

        The starting value of the pattern. If the value is greater than the length it will be truncated.

        Returns: str
        """
        return self._properties['start']

    @start.setter
    def start(self, value):
        """start setter

        The starting value of the pattern. If the value is greater than the length it will be truncated.

        value: str
        """
        self._properties['start'] = value

    @property
    def step(self):
        # type: () -> str
        """step getter

        The amount the start value will be incremented by If the value is greater than the length it will be truncated.

        Returns: str
        """
        return self._properties['step']

    @step.setter
    def step(self, value):
        """step setter

        The amount the start value will be incremented by If the value is greater than the length it will be truncated.

        value: str
        """
        self._properties['step'] = value


class FlowBitPatternList(SnappiList):
    __slots__ = ()

    def __init__(self):
        super(FlowBitPatternList, self).__init__()

    def __getitem__(self, key):
        # type: (int) -> FlowBitPattern
        return self._getitem(key)

    def __iter__(self):
        # type: () -> FlowBitPatternList
        return self._iter()

    def __next__(self):
        # type: () -> FlowBitPattern
        return self._next()

    def next(self):
        # type: () -> FlowBitPattern
        return self._next()

    def bitpattern(self):
        # type: () -> FlowBitPatternList
        """Factory method that creates an instance of FlowBitPattern class

        Container for a bit pattern
        """
        item = FlowBitPattern()
        self._add(item)
        return self

    def bitlist(self, offset=1, length=1, count=1, values=None):
        # type: () -> FlowBitPatternList
        """Factory method that creates an instance of FlowBitList class

        A pattern which is a list of values.
        """
        item = FlowBitPattern()
        item.bitlist
        self._add(item)
        return self

    def bitcounter(self, offset=0, length=32, count=1, start=0, step=0):
        # type: () -> FlowBitPatternList
        """Factory method that creates an instance of FlowBitCounter class

        An incrementing pattern
        """
        item = FlowBitPattern()
        item.bitcounter
        self._add(item)
        return self


class FlowEthernet(SnappiObject):
    __slots__ = ()

    _TYPES = {
        'dst': 'FlowPattern',
        'src': 'FlowPattern',
        'ether_type': 'FlowPattern',
        'pfc_queue': 'FlowPattern',
    }

    def __init__(self):
        super(FlowEthernet, self).__init__()

    @property
    def dst(self):
        # type: () -> FlowPattern
        """dst getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        if 'dst' not in self._properties or self._properties['dst'] is None:
            self._properties['dst'] = FlowPattern()
        return self._properties['dst']

    @property
    def src(self):
        # type: () -> FlowPattern
        """src getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        if 'src' not in self._properties or self._properties['src'] is None:
            self._properties['src'] = FlowPattern()
        return self._properties['src']

    @property
    def ether_type(self):
        # type: () -> FlowPattern
        """ether_type getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        if 'ether_type' not in self._properties or self._properties['ether_type'] is None:
            self._properties['ether_type'] = FlowPattern()
        return self._properties['ether_type']

    @property
    def pfc_queue(self):
        # type: () -> FlowPattern
        """pfc_queue getter

        A container for packet header field patterns.A container for packet header field patterns.Optional field of 3 bits

        Returns: obj(snappi.FlowPattern)
        """
        if 'pfc_queue' not in self._properties or self._properties['pfc_queue'] is None:
            self._properties['pfc_queue'] = FlowPattern()
        return self._properties['pfc_queue']


class FlowPattern(SnappiObject):
    __slots__ = ()

    _TYPES = {
        'increment': 'FlowCounter',
        'decrement': 'FlowCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, metric_group=None):
        super(FlowPattern, self).__init__()
        self.metric_group = metric_group

    @property
    def increment(self):
        # type: () -> FlowCounter
        """Factory method to create an instance of the FlowCounter class

        A counter pattern that can increment or decrement.
        """
        if 'increment' not in self._properties or self._properties['increment'] is None:
            self._properties['increment'] = FlowCounter()
        self.choice = 'increment'
        return self._properties['increment']

    @property
    def decrement(self):
        # type: () -> FlowCounter
        """Factory method to create an instance of the FlowCounter class

        A counter pattern that can increment or decrement.
        """
        if 'decrement' not in self._properties or self._properties['decrement'] is None:
            self._properties['decrement'] = FlowCounter()
        self.choice = 'decrement'
        return self._properties['decrement']

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._properties['choice']

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._properties['choice'] = value

    @property
    def value(self):
        # type: () -> Union[string,number]
        """value getter

        TBD

        Returns: Union[string,number]
        """
        return self._properties['value']

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: Union[string,number]
        """
        self._properties['choice'] = 'value'
        self._properties['value'] = value

    @property
    def values(self):
        # type: () -> list[Union[string,number]]
        """values getter

        TBD

        Returns: list[Union[string,number]]
        """
        return self._properties['values']

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[Union[string,number]]
        """
        self._properties['choice'] = 'values'
        self._properties['values'] = value

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._properties['metric_group']

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._properties['metric_group'] = value


class FlowCounter(SnappiObject):
    __slots__ = ()

    def __init__(self, start=None, step=None, count=None):
        super(FlowCounter, self).__init__()
        self.start = start
        self.step = step
        self.count = count

    @property
    def start(self):
        # type: () -> Union[string,number]
        """start getter

        The value at which the pattern will start.

        Returns: Union[string,number]
        """
        return self._properties['start']

    @start.setter
    def start(self, value):
        """start setter

        The value at which the pattern will start.

        value: Union[string,number]
        """
        self._properties['start'] = value

    @property
    def step(self):
        # type: () -> Union[string,number]
        """step getter

        The value at which the pattern will increment or decrement by.

        Returns: Union[string,number]
        """
        return self._properties['step']

    @step.setter
    def step(self, value):
        """step setter

        The value at which the pattern will increment or decrement by.

        value: Union[string,number]
        """
        self._properties['step'] = value

    @property
    def count(self):
        # type: () -> float
        """count getter

        The number of values in the pattern.

        Returns: float
        """
        return self._properties['count']

    @count.setter
    def count(self, value):
        """count setter

        The number of values in the pattern.

        value: float
        """
        self._properties['count'] = value


class FlowVlan(SnappiObject):
    __slots__ = ()

    _TYPES = {
        'priority': 'FlowPattern',
        'cfi': 'FlowPattern',
        'id': 'FlowPattern',
        'protocol': 'FlowPattern',
    }

    def __init__(self):
        super(FlowVlan, self).__init__()

    @property
    def priority(self):
        # type: () -> FlowPattern
        """priority getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        if 'priority' not in self._properties or self._properties['priority'] is None:
            self._properties['priority'] = FlowPattern()
        return self._properties['priority']

    @property
    def cfi(self):
        # type: () -> FlowPattern
        """cfi getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        if 'cfi' not in self._properties or self._properties['cfi'] is None:
            self._properties['cfi'] = FlowPattern()
        return self._properties['cfi']

    @property
    def id(self):
        # type: () -> FlowPattern
        """id getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        if 'id' not in self._properties or self._properties['id'] is None:
            self._properties['id'] = FlowPattern()
        return self._properties['id']

    @property
    def protocol(self):
        # type: () -> FlowPattern
        """protocol getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        if 'protocol' not in self._properties or self._properties['protocol'] is None:
            self._properties['protocol'] = FlowPattern()
        return self._properties['protocol']


class FlowVxlan(SnappiObject):
    __slots__ = ()

    _TYPES = {
        'flags': 'FlowPattern',
        'reserved0': 'FlowPattern',
        'vni': 'FlowPattern',
        'reserved1': 'FlowPattern',
    }

    def __init__(self):
        super(FlowVxlan, self).__init__()

    @property
    def flags(self):
        # type: () -> FlowPattern
        """flags getter

        A container for packet header field patterns.A container for packet header field patterns.RRRRIRRR Where the I flag MUST be set to 1 for a valid vxlan network id (VNI). The other 7 bits (designated "R") are reserved fields and MUST be set to zero on transmission and ignored on receipt. 8 bits.

        Returns: obj(snappi.FlowPattern)
        """
        if 'flags' not in self._properties or self._properties['flags'] is None:
            self._properties['flags'] = FlowPattern()
        return self._properties['flags']

    @property
    def reserved0(self):
        # type: () -> FlowPattern
        """reserved0 getter

        A container for packet header field patterns.A container for packet header field patterns.Set to 0. 24 bits.

        Returns: obj(snappi.FlowPattern)
        """
        if 'reserved0' not in self._properties or self._properties['reserved0'] is None:
            self._properties['reserved0'] = FlowPattern()
        return self._properties['reserved0']

    @property
    def vni(self):
        # type: () -> FlowPattern
        """vni getter

        A container for packet header field patterns.A container for packet header field patterns.Vxlan network id. 24 bits.

        Returns: obj(snappi.FlowPattern)
        """
        if 'vni' not in self._properties or self._properties['vni'] is None:
            self._properties['vni'] = FlowPattern()
        return self._properties['vni']

    @property
    def reserved1(self):
        # type: () -> FlowPattern
        """reserved1 getter

        A container for packet header field patterns.A container for packet header field patterns.Set to 0. 8 bits.

        Returns: obj(snappi.FlowPattern)
        """
        if 'reserved1' not in self._properties or self._properties['reserved1'] is None:
            self._properties['reserved1'] = FlowPattern()
        return self._properties['reserved1']


class FlowIpv4(SnappiObject):
    __slots__ = ()

    _TYPES = {
        'version': 'FlowPattern',
        'header_length': 'FlowPattern',
        'priority': 'FlowIpv4Priority',
        'total_length': 'FlowPattern',
        'identification': 'FlowPattern',
        'reserved': 'FlowPattern',
        'dont_fragment': 'FlowPattern',
        'more_fragments': 'FlowPattern',
        'fragment_offset': 'FlowPattern',
        'time_to_live': 'FlowPattern',
        'protocol': 'FlowPattern',
        'header_checksum': 'FlowPattern',
        'src': 'FlowPattern',
        'dst': 'FlowPattern',
    }

    def __init__(self):
        super(FlowIpv4, self).__init__()

    @property
    def version(self):
        # type: () -> FlowPattern
        """version getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        if 'version' not in self._properties or self._properties['version'] is None:
            self._properties['version'] = FlowPattern()
        return self._properties['version']

    @property
    def header_length(self):
        # type: () -> FlowPattern
        """header_length getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        if 'header_length' not in self._properties or self._properties['header_length'] is None:
            self._properties['header_length'] = FlowPattern()
        return self._properties['header_length']

    @property
    def priority(self):
        # type: () -> FlowIpv4Priority
        """priority getter

        A container for ipv4 raw, tos, dscp ip priorities.A container for ipv4 raw, tos, dscp ip priorities.

        Returns: obj(snappi.FlowIpv4Priority)
        """
        if 'priority' not in self._properties or self._properties['priority'] is None:
            self._properties['priority'] = FlowIpv4Priority()
        return self._properties['priority']

    @property
    def total_length(self):
        # type: () -> FlowPattern
        """total_length getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        if 'total_length' not in self._properties or self._properties['total_length'] is None:
            self._properties['total_length'] = FlowPattern()
        return self._properties['total_length']

    @property
    def identification(self):
        # type: () -> FlowPattern
        """identification getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        if 'identification' not in self._properties or self._properties['identification'] is None:
            self._properties['identification'] = FlowPattern()
        return self._properties['identification']

    @property
    def reserved(self):
        # type: () -> FlowPattern
        """reserved getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        if 'reserved' not in self._properties or self._properties['reserved'] is None:
            self._properties['reserved'] = FlowPattern()
        return self._properties['reserved']

    @property
    def dont_fragment(self):
        # type: () -> FlowPattern
        """dont_fragment getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        if 'dont_fragment' not in self._properties or self._properties['dont_fragment'] is None:
            self._properties['dont_fragment'] = FlowPattern()
        return self._properties['dont_fragment']

    @property
    def more_fragments(self):
        # type: () -> FlowPattern
        """more_fragments getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        if 'more_fragments' not in self._properties or self._properties['more_fragments'] is None:
            self._properties['more_fragments'] = FlowPattern()
        return self._properties['more_fragments']

    @property
    def fragment_offset(self):
        # type: () -> FlowPattern
        """fragment_offset getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        if 'fragment_offset' not in self._properties or self._properties['fragment_offset'] is None:
            self._properties['fragment_offset'] = FlowPattern()
        return self._properties['fragment_offset']

    @property
    def time_to_live(self):
        # type: () -> FlowPattern
        """time_to_live getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        if 'time_to_live' not in self._properties or self._properties['time_to_live'] is None:
            self._properties['time_to_live'] = FlowPattern()
        return self._properties['time_to_live']

    @property
    def protocol(self):
        # type: () -> FlowPattern
        """protocol getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        if 'protocol' not in self._properties or self._properties['protocol'] is None:
            self._properties['protocol'] = FlowPattern()
        return self._properties['protocol']

    @property
    def header_checksum(self):
        # type: () -> FlowPattern
        """header_checksum getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        if 'header_checksum' not in self._properties or self._properties['header_checksum'] is None:
            self._properties['header_checksum'] = FlowPattern()
        return self._properties['header_checksum']

    @property
    def src(self):
        # type: () -> FlowPattern
        """src getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        if 'src' not in self._properties or self._properties['src'] is None:
            self._properties['src'] = FlowPattern()
        return self._properties['src']

    @property
    def dst(self):
        # type: () -> FlowPattern
        """dst getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        if 'dst' not in self._properties or self._properties['dst'] is None:
            self._properties['dst'] = FlowPattern()
        return self._properties['dst']


class FlowIpv4Priority(SnappiObject):
    __slots__ = ()

    _TYPES = {
        'raw': 'FlowPattern',
        'tos': 'FlowIpv4Tos',
        'dscp': 'FlowIpv4Dscp',
    }

    PRIORITY_RAW = '0'

    RAW = 'raw'
    TOS = 'tos'
    DSCP = 'dscp'

    def __init__(self):
        super(FlowIpv4Priority, self).__init__()

    @property
    def raw(self):
        # type: () -> FlowPattern
        """Factory method to create an instance of the FlowPattern class

        A container for packet header field patterns.
        """
        if 'raw' not in self._properties or self._properties['raw'] is None:
            self._properties['raw'] = FlowPattern()
        self.choice = 'raw'
        return self._properties['raw']

    @property
    def tos(self):
        # type: () -> FlowIpv4Tos
        """Factory method to create an instance of the FlowIpv4Tos class

        Type of service (TOS) packet field.
        """
        if 'tos' not in self._properties or self._properties['tos'] is None:
            self._properties['tos'] = FlowIpv4Tos()
        self.choice = 'tos'
        return self._properties['tos']

    @property
    def dscp(self):
        # type: () -> FlowIpv4Dscp
        """Factory method to create an instance of the FlowIpv4Dscp class

        Differentiated services code point (DSCP) packet field.
        """
        if 'dscp' not in self._properties or self._properties['dscp'] is None:
            self._properties['dscp'] = FlowIpv4Dscp()
        self.choice = 'dscp'
        return self._properties['dscp']

    @property
    def choice(self):
        # type: () -> Union[raw, tos, dscp, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[raw, tos, dscp, choice, choice, choice]
        """
        return self._properties['choice']

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[raw, tos, dscp, choice, choice, choice]
        """
        self._properties['choice'] = value


class FlowIpv4Tos(SnappiObject):
    __slots__ = ()

    _TYPES = {
        'precedence': 'FlowPattern',
        'delay': 'FlowPattern',
        'throughput': 'FlowPattern',
        'reliability': 'FlowPattern',
        'monetary': 'FlowPattern',
        'unused': 'FlowPattern',
    }

    PRE_ROUTINE = '0'
    PRE_PRIORITY = '1'
    PRE_IMMEDIATE = '2'
    PRE_FLASH = '3'
    PRE_FLASH_OVERRIDE = '4'
    PRE_CRITIC_ECP = '5'
    PRE_INTERNETWORK_CONTROL = '6'
    PRE_NETWORK_CONTROL = '7'
    NORMAL = '0'
    LOW = '1'

    def __init__(self):
        super(FlowIpv4Tos, self).__init__()

    @property
    def precedence(self):
        # type: () -> FlowPattern
        """precedence getter

        A container for packet header field patterns.A container for packet header field patterns.Precedence value is 3 bits: >=0 precedence <=3

        Returns: obj(snappi.FlowPattern)
        """
        if 'precedence' not in self._properties or self._properties['precedence'] is None:
            self._properties['precedence'] = FlowPattern()
        return self._properties['precedence']

    @property
    def delay(self):
        # type: () -> FlowPattern
        """delay getter

        A container for packet header field patterns.A container for packet header field patterns.Delay value is 1 bit: >=0 delay <=1

        Returns: obj(snappi.FlowPattern)
        """
        if 'delay' not in self._properties or self._properties['delay'] is None:
            self._properties['delay'] = FlowPattern()
        return self._properties['delay']

    @property
    def throughput(self):
        # type: () -> FlowPattern
        """throughput getter

        A container for packet header field patterns.A container for packet header field patterns.Throughput value is 1 bit: >=0 throughput <=3

        Returns: obj(snappi.FlowPattern)
        """
        if 'throughput' not in self._properties or self._properties['throughput'] is None:
            self._properties['throughput'] = FlowPattern()
        return self._properties['throughput']

    @property
    def reliability(self):
        # type: () -> FlowPattern
        """reliability getter

        A container for packet header field patterns.A container for packet header field patterns.Reliability value is 1 bit: >=0 reliability <=1

        Returns: obj(snappi.FlowPattern)
        """
        if 'reliability' not in self._properties or self._properties['reliability'] is None:
            self._properties['reliability'] = FlowPattern()
        return self._properties['reliability']

    @property
    def monetary(self):
        # type: () -> FlowPattern
        """monetary getter

        A container for packet header field patterns.A container for packet header field patterns.Monetary value is 1 bit: >=0 monetary <=1

        Returns: obj(snappi.FlowPattern)
        """
        if 'monetary' not in self._properties or self._properties['monetary'] is None:
            self._properties['monetary'] = FlowPattern()
        return self._properties['monetary']

    @property
    def unused(self):
        # type: () -> FlowPattern
        """unused getter

        A container for packet header field patterns.A container for packet header field patterns.Unused value is 1 bit: >=0 unused <=1

        Returns: obj(snappi.FlowPattern)
        """
        if 'unused' not in self._properties or self._properties['unused'] is None:
            self._properties['unused'] = FlowPattern()
        return self._properties['unused']


class FlowIpv4Dscp(SnappiObject):
    __slots__ = ()

    _TYPES = {
        'phb': 'FlowPattern',
        'ecn': 'FlowPattern',
    }

    PHB_DEFAULT = '0'
    PHB_CS1 = '8'
    PHB_CS2 = '16'
    PHB_CS3 = '24'
    PHB_CS4 = '32'
    PHB_CS5 = '40'
    PHB_CS6 = '48'
    PHB_CS7 = '56'
    PHB_AF11 = '10'
    PHB_AF12 = '12'
    PHB_AF13 = '14'
    PHB_AF21 = '18'
    PHB_AF22 = '20'
    PHB_AF23 = '22'
    PHB_AF31 = '26'
    PHB_AF32 = '28'
    PHB_AF33 = '30'
    PHB_AF41 = '34'
    PHB_AF42 = '36'
    PHB_AF43 = '38'
    PHB_EF46 = '46'
    ECN_NON_CAPABLE = '0'
    ECN_CAPABLE_TRANSPORT_0 = '1'
    ECN_CAPABLE_TRANSPORT_1 = '2'
    ECN_CONGESTION_ENCOUNTERED = '3'

    def __init__(self):
        super(FlowIpv4Dscp, self).__init__()

    @property
    def phb(self):
        # type: () -> FlowPattern
        """phb getter

        A container for packet header field patterns.A container for packet header field patterns.phb (per-hop-behavior) value is 6 bits: >=0 PHB <=63.

        Returns: obj(snappi.FlowPattern)
        """
        if 'phb' not in self._properties or self._properties['phb'] is None:
            self._properties['phb'] = FlowPattern()
        return self._properties['phb']

    @property
    def ecn(self):
        # type: () -> FlowPattern
        """ecn getter

        A container for packet header field patterns.A container for packet header field patterns.ecn (explicit-congestion-notification) value is 2 bits: >=0 ecn <=3

        Returns: obj(snappi.FlowPattern)
        """
        if 'ecn' not in self._properties or self._properties['ecn'] is None:
            self._properties['ecn'] = FlowPattern()
        return self._properties['ecn']


class FlowIpv6(SnappiObject):
    __slots__ = ()

    _TYPES = {
        'version': 'FlowPattern',
        'traffic_class': 'FlowPattern',
        'flow_label': 'FlowPattern',
        'payload_length': 'FlowPattern',
        'next_header': 'FlowPattern',
        'hop_limit': 'FlowPattern',
        'src': 'FlowPattern',
        'dst': 'FlowPattern',
    }

    def __init__(self):
        super(FlowIpv6, self).__init__()

    @property
    def version(self):
        # type: () -> FlowPattern
        """version getter

        A container for packet header field patterns.A container for packet header field patterns.Default version number is 6 (bit sequence 0110) 4 bits.

        Returns: obj(snappi.FlowPattern)
        """
        if 'version' not in self._properties or self._properties['version'] is None:
            self._properties['version'] = FlowPattern()
        return self._properties['version']

    @property
    def traffic_class(self):
        # type: () -> FlowPattern
        """traffic_class getter

        A container for packet header field patterns.A container for packet header field patterns.8 bits.

        Returns: obj(snappi.FlowPattern)
        """
        if 'traffic_class' not in self._properties or self._properties['traffic_class'] is None:
            self._properties['traffic_class'] = FlowPattern()
        return self._properties['traffic_class']

    @property
    def flow_label(self):
        # type: () -> FlowPattern
        """flow_label getter

        A container for packet header field patterns.A container for packet header field patterns.20 bits.

        Returns: obj(snappi.FlowPattern)
        """
        if 'flow_label' not in self._properties or self._properties['flow_label'] is None:
            self._properties['flow_label'] = FlowPattern()
        return self._properties['flow_label']

    @property
    def payload_length(self):
        # type: () -> FlowPattern
        """payload_length getter

        A container for packet header field patterns.A container for packet header field patterns.16 bits.

        Returns: obj(snappi.FlowPattern)
        """
        if 'payload_length' not in self._properties or self._properties['payload_length'] is None:
            self._properties['payload_length'] = FlowPattern()
        return self._properties['payload_length']

    @property
    def next_header(self):
        # type: () -> FlowPattern
        """next_header getter

        A container for packet header field patterns.A container for packet header field patterns.8 bits.

        Returns: obj(snappi.FlowPattern)
        """
        if 'next_header' not in self._properties or self._properties['next_header'] is None:
            self._properties['next_header'] = FlowPattern()
        return self._properties['next_header']

    @property
    def hop_limit(self):
        # type: () -> FlowPattern
        """hop_limit getter

        A container for packet header field patterns.A container for packet header field patterns.8 bits.

        Returns: obj(snappi.FlowPattern)
        """
        if 'hop_limit' not in self._properties or self._properties['hop_limit'] is None:
            self._properties['hop_limit'] = FlowPattern()
        return self._properties['hop_limit']

    @property
    def src(self):
        # type: () -> FlowPattern
        """src getter

        A container for packet header field patterns.A container for packet header field patterns.128 bits.

        Returns: obj(snappi.FlowPattern)
        """
        if 'src' not in self._properties or self._properties['src'] is None:
            self._properties['src'] = FlowPattern()
        return self._properties['src']

    @property
    def dst(self):
        # type: () -> FlowPattern
        """dst getter

        A container for packet header field patterns.A container for packet header field patterns.128 bits

        Returns: obj(snappi.FlowPattern)
        """
        if 'dst' not in self._properties or self._properties['dst'] is None:
            self._properties['dst'] = FlowPattern()
        return self._properties['dst']


class FlowPfcPause(SnappiObject):
    __slots__ = ()

    _TYPES = {
        'dst': 'FlowPattern',
        'src': 'FlowPattern',
        'ether_type': 'FlowPattern',
        'control_op_code': 'FlowPattern',
        'class_enable_vector': 'FlowPattern',
        'pause_class_0': 'FlowPattern',
        'pause_class_1': 'FlowPattern',
        'pause_class_2': 'FlowPattern',
        'pause_class_3': 'FlowPattern',
        'pause_class_4': 'FlowPattern',
        'pause_class_5': 'FlowPattern',
        'pause_class_6': 'FlowPattern',
        'pause_class_7': 'FlowPattern',
    }

    def __init__(self):
        super(FlowPfcPause, self).__init__()

    @property
    def dst(self):
        # type: () -> FlowPattern
        """dst getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        if 'dst' not in self._properties or self._properties['dst'] is None:
            self._properties['dst'] = FlowPattern()
        return self._properties['dst']

    @property
    def src(self):
        # type: () -> FlowPattern
        """src getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        if 'src' not in self._properties or self._properties['src'] is None:
            self._properties['src'] = FlowPattern()
        return self._properties['src']

    @property
    def ether_type(self):
        # type: () -> FlowPattern
        """ether_type getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        if 'ether_type' not in self._properties or self._properties['ether_type'] is None:
            self._properties['ether_type'] = FlowPattern()
        return self._properties['ether_type']

    @property
    def control_op_code(self):
        # type: () -> FlowPattern
        """control_op_code getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        if 'control_op_code' not in self._properties or self._properties['control_op_code'] is None:
            self._properties['control_op_code'] = FlowPattern()
        return self._properties['control_op_code']

    @property
    def class_enable_vector(self):
        # type: () -> FlowPattern
        """class_enable_vector getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        if 'class_enable_vector' not in self._properties or self._properties['class_enable_vector'] is None:
            self._properties['class_enable_vector'] = FlowPattern()
        return self._properties['class_enable_vector']

    @property
    def pause_class_0(self):
        # type: () -> FlowPattern
        """pause_class_0 getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        if 'pause_class_0' not in self._properties or self._properties['pause_class_0'] is None:
            self._properties['pause_class_0'] = FlowPattern()
        return self._properties['pause_class_0']

    @property
    def pause_class_1(self):
        # type: () -> FlowPattern
        """pause_class_1 getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        if 'pause_class_1' not in self._properties or self._properties['pause_class_1'] is None:
            self._properties['pause_class_1'] = FlowPattern()
        return self._properties['pause_class_1']

    @property
    def pause_class_2(self):
        # type: () -> FlowPattern
        """pause_class_2 getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        if 'pause_class_2' not in self._properties or self._properties['pause_class_2'] is None:
            self._properties['pause_class_2'] = FlowPattern()
        return self._properties['pause_class_2']

    @property
    def pause_class_3(self):
        # type: () -> FlowPattern
        """pause_class_3 getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        if 'pause_class_3' not in self._properties or self._properties['pause_class_3'] is None:
            self._properties['pause_class_3'] = FlowPattern()
        return self._properties['pause_class_3']

    @property
    def pause_class_4(self):
        # type: () -> FlowPattern
        """pause_class_4 getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        if 'pause_class_4' not in self._properties or self._properties['pause_class_4'] is None:
            self._properties['pause_class_4'] = FlowPattern()
        return self._properties['pause_class_4']

    @property
    def pause_class_5(self):
        # type: () -> FlowPattern
        """pause_class_5 getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        if 'pause_class_5' not in self._properties or self._properties['pause_class_5'] is None:
            self._properties['pause_class_5'] = FlowPattern()
        return self._properties['pause_class_5']

    @property
    def pause_class_6(self):
        # type: () -> FlowPattern
        """pause_class_6 getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        if 'pause_class_6' not in self._properties or self._properties['pause_class_6'] is None:
            self._properties['pause_class_6'] = FlowPattern()
        return self._properties['pause_class_6']

    @property
    def pause_class_7(self):
        # type: () -> FlowPattern
        """pause_class_7 getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        if 'pause_class_7' not in self._properties or self._properties['pause_class_7'] is None:
            self._properties['pause_class_7'] = FlowPattern()
        return self._properties['pause_class_7']


class FlowEthernetPause(SnappiObject):
    __slots__ = ()

    _TYPES = {
        'dst': 'FlowPattern',
        'src': 'FlowPattern',
        'ether_type': 'FlowPattern',
        'control_op_code': 'FlowPattern',
        'time': 'FlowPattern',
    }

    def __init__(self):
        super(FlowEthernetPause, self).__init__()

    @property
    def dst(self):
        # type: () -> FlowPattern
        """dst getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        if 'dst' not in self._properties or self._properties['dst'] is None:
            self._properties['dst'] = FlowPattern()
        return self._properties['dst']

    @property
    def src(self):
        # type: () -> FlowPattern
        """src getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        if 'src' not in self._properties or self._properties['src'] is None:
            self._properties['src'] = FlowPattern()
        return self._properties['src']

    @property
    def ether_type(self):
        # type: () -> FlowPattern
        """ether_type getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        if 'ether_type' not in self._properties or self._properties['ether_type'] is None:
            self._properties['ether_type'] = FlowPattern()
        return self._properties['ether_type']

    @property
    def control_op_code(self):
        # type: () -> FlowPattern
        """control_op_code getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        if 'control_op_code' not in self._properties or self._properties['control_op_code'] is None:
            self._properties['control_op_code'] = FlowPattern()
        return self._properties['control_op_code']

    @property
    def time(self):
        # type: () -> FlowPattern
        """time getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        if 'time' not in self._properties or self._properties['time'] is None:
            self._properties['time'] = FlowPattern()
        return self._properties['time']


class FlowTcp(SnappiObject):
    __slots__ = ()

    _TYPES = {
        'src_port': 'FlowPattern',
        'dst_port': 'FlowPattern',
        'seq_num': 'FlowPattern',
        'ack_num': 'FlowPattern',
        'data_offset': 'FlowPattern',
        'ecn_ns': 'FlowPattern',
        'ecn_cwr': 'FlowPattern',
        'ecn_echo': 'FlowPattern',
        'ctl_urg': 'FlowPattern',
        'ctl_ack': 'FlowPattern',
        'ctl_psh': 'FlowPattern',
        'ctl_rst': 'FlowPattern',
        'ctl_syn': 'FlowPattern',
        'ctl_fin': 'FlowPattern',
        'window': 'FlowPattern',
    }

    def __init__(self):
        super(FlowTcp, self).__init__()

    @property
    def src_port(self):
        # type: () -> FlowPattern
        """src_port getter

        A container for packet header field patterns.A container for packet header field patterns.Tcp source port. Max length is 2 bytes.

        Returns: obj(snappi.FlowPattern)
        """
        if 'src_port' not in self._properties or self._properties['src_port'] is None:
            self._properties['src_port'] = FlowPattern()
        return self._properties['src_port']

    @property
    def dst_port(self):
        # type: () -> FlowPattern
        """dst_port getter

        A container for packet header field patterns.A container for packet header field patterns.Tcp destination port. Max length is 2 bytes.

        Returns: obj(snappi.FlowPattern)
        """
        if 'dst_port' not in self._properties or self._properties['dst_port'] is None:
            self._properties['dst_port'] = FlowPattern()
        return self._properties['dst_port']

    @property
    def seq_num(self):
        # type: () -> FlowPattern
        """seq_num getter

        A container for packet header field patterns.A container for packet header field patterns.Tcp Sequence Number. Max length is 4 bytes.

        Returns: obj(snappi.FlowPattern)
        """
        if 'seq_num' not in self._properties or self._properties['seq_num'] is None:
            self._properties['seq_num'] = FlowPattern()
        return self._properties['seq_num']

    @property
    def ack_num(self):
        # type: () -> FlowPattern
        """ack_num getter

        A container for packet header field patterns.A container for packet header field patterns.Tcp Acknowledgement Number. Max length is 4 bytes.

        Returns: obj(snappi.FlowPattern)
        """
        if 'ack_num' not in self._properties or self._properties['ack_num'] is None:
            self._properties['ack_num'] = FlowPattern()
        return self._properties['ack_num']

    @property
    def data_offset(self):
        # type: () -> FlowPattern
        """data_offset getter

        A container for packet header field patterns.A container for packet header field patterns.The number of 32 bit words in the TCP header. This indicates where the data begins. Max length is 4 bits.

        Returns: obj(snappi.FlowPattern)
        """
        if 'data_offset' not in self._properties or self._properties['data_offset'] is None:
            self._properties['data_offset'] = FlowPattern()
        return self._properties['data_offset']

    @property
    def ecn_ns(self):
        # type: () -> FlowPattern
        """ecn_ns getter

        A container for packet header field patterns.A container for packet header field patterns.Explicit congestion notification, concealment protection. Max length is 1 bit.

        Returns: obj(snappi.FlowPattern)
        """
        if 'ecn_ns' not in self._properties or self._properties['ecn_ns'] is None:
            self._properties['ecn_ns'] = FlowPattern()
        return self._properties['ecn_ns']

    @property
    def ecn_cwr(self):
        # type: () -> FlowPattern
        """ecn_cwr getter

        A container for packet header field patterns.A container for packet header field patterns.Explicit congestion notification, congestion window reduced. Max length is 1 bit.

        Returns: obj(snappi.FlowPattern)
        """
        if 'ecn_cwr' not in self._properties or self._properties['ecn_cwr'] is None:
            self._properties['ecn_cwr'] = FlowPattern()
        return self._properties['ecn_cwr']

    @property
    def ecn_echo(self):
        # type: () -> FlowPattern
        """ecn_echo getter

        A container for packet header field patterns.A container for packet header field patterns.Explicit congestion notification, echo. 1 indicates the peer is ecn capable. 0 indicates that a packet with ipv4.ecn = 11 in the ip header was received during normal transmission. Max length is 1 bit.

        Returns: obj(snappi.FlowPattern)
        """
        if 'ecn_echo' not in self._properties or self._properties['ecn_echo'] is None:
            self._properties['ecn_echo'] = FlowPattern()
        return self._properties['ecn_echo']

    @property
    def ctl_urg(self):
        # type: () -> FlowPattern
        """ctl_urg getter

        A container for packet header field patterns.A container for packet header field patterns.A value of 1 indicates that the urgent pointer field is significant. Max length is 1 bit.

        Returns: obj(snappi.FlowPattern)
        """
        if 'ctl_urg' not in self._properties or self._properties['ctl_urg'] is None:
            self._properties['ctl_urg'] = FlowPattern()
        return self._properties['ctl_urg']

    @property
    def ctl_ack(self):
        # type: () -> FlowPattern
        """ctl_ack getter

        A container for packet header field patterns.A container for packet header field patterns.A value of 1 indicates that the ackknowledgment field is significant. Max length is 1 bit.

        Returns: obj(snappi.FlowPattern)
        """
        if 'ctl_ack' not in self._properties or self._properties['ctl_ack'] is None:
            self._properties['ctl_ack'] = FlowPattern()
        return self._properties['ctl_ack']

    @property
    def ctl_psh(self):
        # type: () -> FlowPattern
        """ctl_psh getter

        A container for packet header field patterns.A container for packet header field patterns.Asks to push the buffered data to the receiving application. Max length is 1 bit.

        Returns: obj(snappi.FlowPattern)
        """
        if 'ctl_psh' not in self._properties or self._properties['ctl_psh'] is None:
            self._properties['ctl_psh'] = FlowPattern()
        return self._properties['ctl_psh']

    @property
    def ctl_rst(self):
        # type: () -> FlowPattern
        """ctl_rst getter

        A container for packet header field patterns.A container for packet header field patterns.Reset the connection. Max length is 1 bit.

        Returns: obj(snappi.FlowPattern)
        """
        if 'ctl_rst' not in self._properties or self._properties['ctl_rst'] is None:
            self._properties['ctl_rst'] = FlowPattern()
        return self._properties['ctl_rst']

    @property
    def ctl_syn(self):
        # type: () -> FlowPattern
        """ctl_syn getter

        A container for packet header field patterns.A container for packet header field patterns.Synchronize sequenece numbers. Max length is 1 bit.

        Returns: obj(snappi.FlowPattern)
        """
        if 'ctl_syn' not in self._properties or self._properties['ctl_syn'] is None:
            self._properties['ctl_syn'] = FlowPattern()
        return self._properties['ctl_syn']

    @property
    def ctl_fin(self):
        # type: () -> FlowPattern
        """ctl_fin getter

        A container for packet header field patterns.A container for packet header field patterns.Last packet from the sender. Max length is 1 bit.

        Returns: obj(snappi.FlowPattern)
        """
        if 'ctl_fin' not in self._properties or self._properties['ctl_fin'] is None:
            self._properties['ctl_fin'] = FlowPattern()
        return self._properties['ctl_fin']

    @property
    def window(self):
        # type: () -> FlowPattern
        """window getter

        A container for packet header field patterns.A container for packet header field patterns.Tcp connection window. Max length is 2 bytes.

        Returns: obj(snappi.FlowPattern)
        """
        if 'window' not in self._properties or self._properties['window'] is None:
            self._properties['window'] = FlowPattern()
        return self._properties['window']


class FlowUdp(SnappiObject):
    __slots__ = ()

    _TYPES = {
        'src_port': 'FlowPattern',
        'dst_port': 'FlowPattern',
        'length': 'FlowPattern',
        'checksum': 'FlowPattern',
    }

    def __init__(self):
        super(FlowUdp, self).__init__()

    @property
    def src_port(self):
        # type: () -> FlowPattern
        """src_port getter

        A container for packet header field patterns.A container for packet header field patterns.Udp source port. Max length is 2 bytes.

        Returns: obj(snappi.FlowPattern)
        """
        if 'src_port' not in self._properties or self._properties['src_port'] is None:
            self._properties['src_port'] = FlowPattern()
        return self._properties['src_port']

    @property
    def dst_port(self):
        # type: () -> FlowPattern
        """dst_port getter

        A container for packet header field patterns.A container for packet header field patterns.Tcp destination port. Max length is 2 bytes.

        Returns: obj(snappi.FlowPattern)
        """
        if 'dst_port' not in self._properties or self._properties['dst_port'] is None:
            self._properties['dst_port'] = FlowPattern()
        return self._properties['dst_port']

    @property
    def length(self):
        # type: () -> FlowPattern
        """length getter

        A container for packet header field patterns.A container for packet header field patterns.Length in bytes of the udp header and yudp data. Max length is 2 bytes.

        Returns: obj(snappi.FlowPattern)
        """
        if 'length' not in self._properties or self._properties['length'] is None:
            self._properties['length'] = FlowPattern()
        return self._properties['length']

    @property
    def checksum(self):
        # type: () -> FlowPattern
        """checksum getter

        A container for packet header field patterns.A container for packet header field patterns.Checksum field used for error checking of header and data. Max length is 2 bytes.

        Returns: obj(snappi.FlowPattern)
        """
        if 'checksum' not in self._properties or self._properties['checksum'] is None:
            self._properties['checksum'] = FlowPattern()
        return self._properties['checksum']


class FlowGre(SnappiObject):
    __slots__ = ()

    _TYPES = {
        'checksum_present': 'FlowPattern',
        'key_present': 'FlowPattern',
        'seq_number_present': 'FlowPattern',
        'reserved0': 'FlowPattern',
        'version': 'FlowPattern',
        'protocol': 'FlowPattern',
        'checksum': 'FlowPattern',
        'reserved1': 'FlowPattern',
        'key': 'FlowPattern',
        'sequence_number': 'FlowPattern',
    }

    def __init__(self):
        super(FlowGre, self).__init__()

    @property
    def checksum_present(self):
        # type: () -> FlowPattern
        """checksum_present getter

        A container for packet header field patterns.A container for packet header field patterns.Checksum bit. Set to 1 if a checksum is present.

        Returns: obj(snappi.FlowPattern)
        """
        if 'checksum_present' not in self._properties or self._properties['checksum_present'] is None:
            self._properties['checksum_present'] = FlowPattern()
        return self._properties['checksum_present']

    @property
    def key_present(self):
        # type: () -> FlowPattern
        """key_present getter

        A container for packet header field patterns.A container for packet header field patterns.Key bit. Set to 1 if a key is present.

        Returns: obj(snappi.FlowPattern)
        """
        if 'key_present' not in self._properties or self._properties['key_present'] is None:
            self._properties['key_present'] = FlowPattern()
        return self._properties['key_present']

    @property
    def seq_number_present(self):
        # type: () -> FlowPattern
        """seq_number_present getter

        A container for packet header field patterns.A container for packet header field patterns.Sequence number bit. Set to 1 if a sequence number is present.

        Returns: obj(snappi.FlowPattern)
        """
        if 'seq_number_present' not in self._properties or self._properties['seq_number_present'] is None:
            self._properties['seq_number_present'] = FlowPattern()
        return self._properties['seq_number_present']

    @property
    def reserved0(self):
        # type: () -> FlowPattern
        """reserved0 getter

        A container for packet header field patterns.A container for packet header field patterns.Reserved bits. Set to 0. 9 bits.

        Returns: obj(snappi.FlowPattern)
        """
        if 'reserved0' not in self._properties or self._properties['reserved0'] is None:
            self._properties['reserved0'] = FlowPattern()
        return self._properties['reserved0']

    @property
    def version(self):
        # type: () -> FlowPattern
        """version getter

        A container for packet header field patterns.A container for packet header field patterns.Gre version number. Set to 0. 3 bits.

        Returns: obj(snappi.FlowPattern)
        """
        if 'version' not in self._properties or self._properties['version'] is None:
            self._properties['version'] = FlowPattern()
        return self._properties['version']

    @property
    def protocol(self):
        # type: () -> FlowPattern
        """protocol getter

        A container for packet header field patterns.A container for packet header field patterns.Indicates the ether protocol type of the encapsulated payload. - 0x0800 ipv4 - 0x86DD ipv6

        Returns: obj(snappi.FlowPattern)
        """
        if 'protocol' not in self._properties or self._properties['protocol'] is None:
            self._properties['protocol'] = FlowPattern()
        return self._properties['protocol']

    @property
    def checksum(self):
        # type: () -> FlowPattern
        """checksum getter

        A container for packet header field patterns.A container for packet header field patterns.Present if the checksum_present bit is set. Contains the checksum for the gre header and payload. 16 bits.

        Returns: obj(snappi.FlowPattern)
        """
        if 'checksum' not in self._properties or self._properties['checksum'] is None:
            self._properties['checksum'] = FlowPattern()
        return self._properties['checksum']

    @property
    def reserved1(self):
        # type: () -> FlowPattern
        """reserved1 getter

        A container for packet header field patterns.A container for packet header field patterns.Reserved bits. Set to 0. 16 bits.

        Returns: obj(snappi.FlowPattern)
        """
        if 'reserved1' not in self._properties or self._properties['reserved1'] is None:
            self._properties['reserved1'] = FlowPattern()
        return self._properties['reserved1']

    @property
    def key(self):
        # type: () -> FlowPattern
        """key getter

        A container for packet header field patterns.A container for packet header field patterns.Present if the key_present bit is set. Contains an application specific key value. 32 bits

        Returns: obj(snappi.FlowPattern)
        """
        if 'key' not in self._properties or self._properties['key'] is None:
            self._properties['key'] = FlowPattern()
        return self._properties['key']

    @property
    def sequence_number(self):
        # type: () -> FlowPattern
        """sequence_number getter

        A container for packet header field patterns.A container for packet header field patterns.Present if the seq_number_present bit is set. Contains a sequence number for the gre packet. 32 bits

        Returns: obj(snappi.FlowPattern)
        """
        if 'sequence_number' not in self._properties or self._properties['sequence_number'] is None:
            self._properties['sequence_number'] = FlowPattern()
        return self._properties['sequence_number']


class FlowGtpv1(SnappiObject):
    __slots__ = ()

    _TYPES = {
        'version': 'FlowPattern',
        'protocol_type': 'FlowPattern',
        'reserved': 'FlowPattern',
        'e_flag': 'FlowPattern',
        's_flag': 'FlowPattern',
        'pn_flag': 'FlowPattern',
        'message_type': 'FlowPattern',
        'message_length': 'FlowPattern',
        'teid': 'FlowPattern',
        'squence_number': 'FlowPattern',
        'n_pdu_number': 'FlowPattern',
        'next_extension_header_type': 'FlowPattern',
        'extension_headers': 'FlowGtpExtensionList',
    }

    def __init__(self):
        super(FlowGtpv1, self).__init__()

    @property
    def version(self):
        # type: () -> FlowPattern
        """version getter

        A container for packet header field patterns.A container for packet header field patterns.It is a 3-bit field. For GTPv1, this has a value of 1.

        Returns: obj(snappi.FlowPattern)
        """
        if 'version' not in self._properties or self._properties['version'] is None:
            self._properties['version'] = FlowPattern()
        return self._properties['version']

    @property
    def protocol_type(self):
        # type: () -> FlowPattern
        """protocol_type getter

        A container for packet header field patterns.A container for packet header field patterns.A 1-bit value that differentiates GTP (value 1) from GTP' (value 0).

        Returns: obj(snappi.FlowPattern)
        """
        if 'protocol_type' not in self._properties or self._properties['protocol_type'] is None:
            self._properties['protocol_type'] = FlowPattern()
        return self._properties['protocol_type']

    @property
    def reserved(self):
        # type: () -> FlowPattern
        """reserved getter

        A container for packet header field patterns.A container for packet header field patterns.A 1-bit reserved field (must be 0).

        Returns: obj(snappi.FlowPattern)
        """
        if 'reserved' not in self._properties or self._properties['reserved'] is None:
            self._properties['reserved'] = FlowPattern()
        return self._properties['reserved']

    @property
    def e_flag(self):
        # type: () -> FlowPattern
        """e_flag getter

        A container for packet header field patterns.A container for packet header field patterns.A 1-bit value that states whether there is an extension header optional field.

        Returns: obj(snappi.FlowPattern)
        """
        if 'e_flag' not in self._properties or self._properties['e_flag'] is None:
            self._properties['e_flag'] = FlowPattern()
        return self._properties['e_flag']

    @property
    def s_flag(self):
        # type: () -> FlowPattern
        """s_flag getter

        A container for packet header field patterns.A container for packet header field patterns.A 1-bit value that states whether there is a Sequence Number optional field.

        Returns: obj(snappi.FlowPattern)
        """
        if 's_flag' not in self._properties or self._properties['s_flag'] is None:
            self._properties['s_flag'] = FlowPattern()
        return self._properties['s_flag']

    @property
    def pn_flag(self):
        # type: () -> FlowPattern
        """pn_flag getter

        A container for packet header field patterns.A container for packet header field patterns.A 1-bit value that states whether there is a N-PDU number optional field.

        Returns: obj(snappi.FlowPattern)
        """
        if 'pn_flag' not in self._properties or self._properties['pn_flag'] is None:
            self._properties['pn_flag'] = FlowPattern()
        return self._properties['pn_flag']

    @property
    def message_type(self):
        # type: () -> FlowPattern
        """message_type getter

        A container for packet header field patterns.A container for packet header field patterns.An 8-bit field that indicates the type of GTP message. Different types of messages are defined in 3GPP TS 29.060 section 7.1

        Returns: obj(snappi.FlowPattern)
        """
        if 'message_type' not in self._properties or self._properties['message_type'] is None:
            self._properties['message_type'] = FlowPattern()
        return self._properties['message_type']

    @property
    def message_length(self):
        # type: () -> FlowPattern
        """message_length getter

        A container for packet header field patterns.A container for packet header field patterns.A 16-bit field that indicates the length of the payload in bytes (rest of the packet following the mandatory 8-byte GTP header). Includes the optional fields.

        Returns: obj(snappi.FlowPattern)
        """
        if 'message_length' not in self._properties or self._properties['message_length'] is None:
            self._properties['message_length'] = FlowPattern()
        return self._properties['message_length']

    @property
    def teid(self):
        # type: () -> FlowPattern
        """teid getter

        A container for packet header field patterns.A container for packet header field patterns.Tunnel endpoint identifier. A 32-bit(4-octet) field used to multiplex different connections in the same GTP tunnel.

        Returns: obj(snappi.FlowPattern)
        """
        if 'teid' not in self._properties or self._properties['teid'] is None:
            self._properties['teid'] = FlowPattern()
        return self._properties['teid']

    @property
    def squence_number(self):
        # type: () -> FlowPattern
        """squence_number getter

        A container for packet header field patterns.A container for packet header field patterns.An (optional) 16-bit field. This field exists if any of the e_flag, s_flag, or pn_flag bits are on. The field must be interpreted only if the s_flag bit is on.

        Returns: obj(snappi.FlowPattern)
        """
        if 'squence_number' not in self._properties or self._properties['squence_number'] is None:
            self._properties['squence_number'] = FlowPattern()
        return self._properties['squence_number']

    @property
    def n_pdu_number(self):
        # type: () -> FlowPattern
        """n_pdu_number getter

        A container for packet header field patterns.A container for packet header field patterns.An (optional) 8-bit field. This field exists if any of the e_flag, s_flag, or pn_flag bits are on. The field must be interpreted only if the pn_flag bit is on.

        Returns: obj(snappi.FlowPattern)
        """
        if 'n_pdu_number' not in self._properties or self._properties['n_pdu_number'] is None:
            self._properties['n_pdu_number'] = FlowPattern()
        return self._properties['n_pdu_number']

    @property
    def next_extension_header_type(self):
        # type: () -> FlowPattern
        """next_extension_header_type getter

        A container for packet header field patterns.A container for packet header field patterns.An (optional) 8-bit field. This field exists if any of the e_flag, s_flag, or pn_flag bits are on. The field must be interpreted only if the e_flag bit is on.

        Returns: obj(snappi.FlowPattern)
        """
        if 'next_extension_header_type' not in self._properties or self._properties['next_extension_header_type'] is None:
            self._properties['next_extension_header_type'] = FlowPattern()
        return self._properties['next_extension_header_type']

    @property
    def extension_headers(self):
        # type: () -> FlowGtpExtensionList
        """extension_headers getter

        A list of optional extension headers.

        Returns: list[obj(snappi.FlowGtpExtension)]
        """
        if 'extension_headers' not in self._properties or self._properties['extension_headers'] is None:
            self._properties['extension_headers'] = FlowGtpExtensionList()
        return self._properties['extension_headers']


class FlowGtpExtension(SnappiObject):
    __slots__ = ()

    _TYPES = {
        'extension_length': 'FlowPattern',
        'contents': 'FlowPattern',
        'next_extension_header': 'FlowPattern',
    }

    def __init__(self):
        super(FlowGtpExtension, self).__init__()

    @property
    def extension_length(self):
        # type: () -> FlowPattern
        """extension_length getter

        A container for packet header field patterns.An 8-bit field. This field states the length of this extension header, including the length, the contents, and the next extension header field, in 4-octet units, so the length of the extension must always be a multiple of 4.

        Returns: obj(snappi.FlowPattern)
        """
        if 'extension_length' not in self._properties or self._properties['extension_length'] is None:
            self._properties['extension_length'] = FlowPattern()
        return self._properties['extension_length']

    @property
    def contents(self):
        # type: () -> FlowPattern
        """contents getter

        A container for packet header field patterns.The extension header contents.

        Returns: obj(snappi.FlowPattern)
        """
        if 'contents' not in self._properties or self._properties['contents'] is None:
            self._properties['contents'] = FlowPattern()
        return self._properties['contents']

    @property
    def next_extension_header(self):
        # type: () -> FlowPattern
        """next_extension_header getter

        A container for packet header field patterns.An 8-bit field. It states the type of the next extension, or 0 if no next extension exists. This permits chaining several next extension headers.

        Returns: obj(snappi.FlowPattern)
        """
        if 'next_extension_header' not in self._properties or self._properties['next_extension_header'] is None:
            self._properties['next_extension_header'] = FlowPattern()
        return self._properties['next_extension_header']


class FlowGtpExtensionList(SnappiList):
    __slots__ = ()

    def __init__(self):
        super(FlowGtpExtensionList, self).__init__()

    def __getitem__(self, key):
        # type: (int) -> FlowGtpExtension
        return self._getitem(key)

    def __iter__(self):
        # type: () -> FlowGtpExtensionList
        return self._iter()

    def __next__(self):
        # type: () -> FlowGtpExtension
        return self._next()

    def next(self):
        # type: () -> FlowGtpExtension
        return self._next()

    def gtpextension(self):
        # type: () -> FlowGtpExtensionList
        """Factory method that creates an instance of FlowGtpExtension class

        TBD
        """
        item = FlowGtpExtension()
        self._add(item)
        return self


class FlowGtpv2(SnappiObject):
    __slots__ = ()

    _TYPES = {
        'version': 'FlowPattern',
        'piggybacking_flag': 'FlowPattern',
        'teid_flag': 'FlowPattern',
        'spare1': 'FlowPattern',
        'message_type': 'FlowPattern',
        'message_length': 'FlowPattern',
        'teid': 'FlowPattern',
        'sequence_number': 'FlowPattern',
        'spare2': 'FlowPattern',
    }

    def __init__(self):
        super(FlowGtpv2, self).__init__()

    @property
    def version(self):
        # type: () -> FlowPattern
        """version getter

        A container for packet header field patterns.A container for packet header field patterns.It is a 3-bit field. For GTPv2, this has a value of 2.

        Returns: obj(snappi.FlowPattern)
        """
        if 'version' not in self._properties or self._properties['version'] is None:
            self._properties['version'] = FlowPattern()
        return self._properties['version']

    @property
    def piggybacking_flag(self):
        # type: () -> FlowPattern
        """piggybacking_flag getter

        A container for packet header field patterns.A container for packet header field patterns.If this bit is set to 1 then another GTP-C message with its own header shall be present at the end of the current message.

        Returns: obj(snappi.FlowPattern)
        """
        if 'piggybacking_flag' not in self._properties or self._properties['piggybacking_flag'] is None:
            self._properties['piggybacking_flag'] = FlowPattern()
        return self._properties['piggybacking_flag']

    @property
    def teid_flag(self):
        # type: () -> FlowPattern
        """teid_flag getter

        A container for packet header field patterns.A container for packet header field patterns.If this bit is set to 1 then the TEID field will be present between the message length and the sequence number. All messages except Echo and Echo reply require TEID to be present.

        Returns: obj(snappi.FlowPattern)
        """
        if 'teid_flag' not in self._properties or self._properties['teid_flag'] is None:
            self._properties['teid_flag'] = FlowPattern()
        return self._properties['teid_flag']

    @property
    def spare1(self):
        # type: () -> FlowPattern
        """spare1 getter

        A container for packet header field patterns.A container for packet header field patterns.A 3-bit reserved field (must be 0).

        Returns: obj(snappi.FlowPattern)
        """
        if 'spare1' not in self._properties or self._properties['spare1'] is None:
            self._properties['spare1'] = FlowPattern()
        return self._properties['spare1']

    @property
    def message_type(self):
        # type: () -> FlowPattern
        """message_type getter

        A container for packet header field patterns.A container for packet header field patterns.An 8-bit field that indicates the type of GTP message. Different types of messages are defined in 3GPP TS 29.060 section 7.1

        Returns: obj(snappi.FlowPattern)
        """
        if 'message_type' not in self._properties or self._properties['message_type'] is None:
            self._properties['message_type'] = FlowPattern()
        return self._properties['message_type']

    @property
    def message_length(self):
        # type: () -> FlowPattern
        """message_length getter

        A container for packet header field patterns.A container for packet header field patterns.A 16-bit field that indicates the length of the payload in bytes (excluding the mandatory GTP-c header (first 4 bytes). Includes the TEID and sequence_number if they are present.

        Returns: obj(snappi.FlowPattern)
        """
        if 'message_length' not in self._properties or self._properties['message_length'] is None:
            self._properties['message_length'] = FlowPattern()
        return self._properties['message_length']

    @property
    def teid(self):
        # type: () -> FlowPattern
        """teid getter

        A container for packet header field patterns.A container for packet header field patterns.Tunnel endpoint identifier. A 32-bit (4-octet) field used to multiplex different connections in the same GTP tunnel. Is present only if the teid_flag is set.

        Returns: obj(snappi.FlowPattern)
        """
        if 'teid' not in self._properties or self._properties['teid'] is None:
            self._properties['teid'] = FlowPattern()
        return self._properties['teid']

    @property
    def sequence_number(self):
        # type: () -> FlowPattern
        """sequence_number getter

        A container for packet header field patterns.A container for packet header field patterns.A 24-bit field.

        Returns: obj(snappi.FlowPattern)
        """
        if 'sequence_number' not in self._properties or self._properties['sequence_number'] is None:
            self._properties['sequence_number'] = FlowPattern()
        return self._properties['sequence_number']

    @property
    def spare2(self):
        # type: () -> FlowPattern
        """spare2 getter

        A container for packet header field patterns.A container for packet header field patterns.An 8-bit reserved field (must be 0).

        Returns: obj(snappi.FlowPattern)
        """
        if 'spare2' not in self._properties or self._properties['spare2'] is None:
            self._properties['spare2'] = FlowPattern()
        return self._properties['spare2']


class FlowHeaderList(SnappiList):
    __slots__ = ()

    def __init__(self):
        super(FlowHeaderList, self).__init__()

    def __getitem__(self, key):
        # type: (int) -> FlowHeader
        return self._getitem(key)

    def __iter__(self):
        # type: () -> FlowHeaderList
        return self._iter()

    def __next__(self):
        # type: () -> FlowHeader
        return self._next()

    def next(self):
        # type: () -> FlowHeader
        return self._next()

    def header(self):
        # type: () -> FlowHeaderList
        """Factory method that creates an instance of FlowHeader class

        Container for all traffic packet headers
        """
        item = FlowHeader()
        self._add(item)
        return self

    def custom(self, bytes=None):
        # type: () -> FlowHeaderList
        """Factory method that creates an instance of FlowCustom class

        Custom packet header
        """
        item = FlowHeader()
        item.custom
        self._add(item)
        return self

    def ethernet(self):
        # type: () -> FlowHeaderList
        """Factory method that creates an instance of FlowEthernet class

        Ethernet packet header
        """
        item = FlowHeader()
        item.ethernet
        self._add(item)
        return self

    def vlan(self):
        # type: () -> FlowHeaderList
        """Factory method that creates an instance of FlowVlan class

        Vlan packet header
        """
        item = FlowHeader()
        item.vlan
        self._add(item)
        return self

    def vxlan(self):
        # type: () -> FlowHeaderList
        """Factory method that creates an instance of FlowVxlan class

        Vxlan packet header
        """
        item = FlowHeader()
        item.vxlan
        self._add(item)
        return self

    def ipv4(self):
        # type: () -> FlowHeaderList
        """Factory method that creates an instance of FlowIpv4 class

        Ipv4 packet header
        """
        item = FlowHeader()
        item.ipv4
        self._add(item)
        return self

    def ipv6(self):
        # type: () -> FlowHeaderList
        """Factory method that creates an instance of FlowIpv6 class

        Ipv6 packet header
        """
        item = FlowHeader()
        item.ipv6
        self._add(item)
        return self

    def pfcpause(self):
        # type: () -> FlowHeaderList
        """Factory method that creates an instance of FlowPfcPause class

        IEEE 802.1Qbb PFC Pause packet header. - dst: 01:80:C2:00:00:01 48bits - src: 48bits - ether_type: 0x8808 16bits - control_op_code: 0x0101 16bits - class_enable_vector: 16bits - pause_class_0: 0x0000 16bits - pause_class_1: 0x0000 16bits - pause_class_2: 0x0000 16bits - pause_class_3: 0x0000 16bits - pause_class_4: 0x0000 16bits - pause_class_5: 0x0000 16bits - pause_class_6: 0x0000 16bits - pause_class_7: 0x0000 16bits
        """
        item = FlowHeader()
        item.pfcpause
        self._add(item)
        return self

    def ethernetpause(self):
        # type: () -> FlowHeaderList
        """Factory method that creates an instance of FlowEthernetPause class

        IEEE 802.3x Ethernet Pause packet header. - dst: 01:80:C2:00:00:01 48bits - src: 48bits - ether_type: 0x8808 16bits - control_op_code: 0x0001 16bits - time: 0x0000 16bits
        """
        item = FlowHeader()
        item.ethernetpause
        self._add(item)
        return self

    def tcp(self):
        # type: () -> FlowHeaderList
        """Factory method that creates an instance of FlowTcp class

        Tcp packet header
        """
        item = FlowHeader()
        item.tcp
        self._add(item)
        return self

    def udp(self):
        # type: () -> FlowHeaderList
        """Factory method that creates an instance of FlowUdp class

        Udp packet header
        """
        item = FlowHeader()
        item.udp
        self._add(item)
        return self

    def gre(self):
        # type: () -> FlowHeaderList
        """Factory method that creates an instance of FlowGre class

        Gre packet header
        """
        item = FlowHeader()
        item.gre
        self._add(item)
        return self

    def gtpv1(self):
        # type: () -> FlowHeaderList
        """Factory method that creates an instance of FlowGtpv1 class

        GTPv1 packet header
        """
        item = FlowHeader()
        item.gtpv1
        self._add(item)
        return self

    def gtpv2(self):
        # type: () -> FlowHeaderList
        """Factory method that creates an instance of FlowGtpv2 class

        GTPv2 packet header
        """
        item = FlowHeader()
        item.gtpv2
        self._add(item)
        return self


class FlowSize(SnappiObject):
    __slots__ = ()

    _TYPES = {
        'increment': 'FlowSizeIncrement',
        'random': 'FlowSizeRandom',
    }

    FIXED = 'fixed'
    INCREMENT = 'increment'
    RANDOM = 'random'

    def __init__(self):
        super(FlowSize, self).__init__()

    @property
    def increment(self):
        # type: () -> FlowSizeIncrement
        """Factory method to create an instance of the FlowSizeIncrement class

        Frame size that increments from a starting size to an ending size incrementing by a step size.
        """
        if 'increment' not in self._properties or self._properties['increment'] is None:
            self._properties['increment'] = FlowSizeIncrement()
        self.choice = 'increment'
        return self._properties['increment']

    @property
    def random(self):
        # type: () -> FlowSizeRandom
        """Factory method to create an instance of the FlowSizeRandom class

        Random frame size from a min value to a max value.
        """
        if 'random' not in self._properties or self._properties['random'] is None:
            self._properties['random'] = FlowSizeRandom()
        self.choice = 'random'
        return self._properties['random']

    @property
    def choice(self):
        # type: () -> Union[fixed, increment, random, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[fixed, increment, random, choice, choice, choice]
        """
        return self._properties['choice']

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[fixed, increment, random, choice, choice, choice]
        """
        self._properties['choice'] = value

    @property
    def fixed(self):
        # type: () -> int
        """fixed getter

        TBD

        Returns: int
        """
        return self._properties['fixed']

    @fixed.setter
    def fixed(self, value):
        """fixed setter

        TBD

        value: int
        """
        self._properties['choice'] = 'fixed'
        self._properties['fixed'] = value


class FlowSizeIncrement(SnappiObject):
    __slots__ = ()

    def __init__(self, start=None, end=None, step=None):
        super(FlowSizeIncrement, self).__init__()
        self.start = start
        self.end = end
        self.step = step

    @property
    def start(self):
        # type: () -> int
        """start getter

        Starting frame size in bytes

        Returns: int
        """
        return self._properties['start']

    @start.setter
    def start(self, value):
        """start setter

        Starting frame size in bytes

        value: int
        """
        self._properties['start'] = value

    @property
    def end(self):
        # type: () -> int
        """end getter

        Ending frame size in bytes

        Returns: int
        """
        return self._properties['end']

    @end.setter
    def end(self, value):
        """end setter

        Ending frame size in bytes

        value: int
        """
        self._properties['end'] = value

    @property
    def step(self):
        # type: () -> int
        """step getter

        Step frame size in bytes

        Returns: int
        """
        return self._properties['step']

    @step.setter
    def step(self, value):
        """step setter

        Step frame size in bytes

        value: int
        """
        self._properties['step'] = value


class FlowSizeRandom(SnappiObject):
    __slots__ = ()

    def __init__(self, min=None, max=None):
        super(FlowSizeRandom, self).__init__()
        self.min = min
        self.max = max

    @property
    def min(self):
        # type: () -> int
        """min getter

        TBD

        Returns: int
        """
        return self._properties['min']

    @min.setter
    def min(self, value):
        """min setter

        TBD

        value: int
        """
        self._properties['min'] = value

    @property
    def max(self):
        # type: () -> int
        """max getter

        TBD

        Returns: int
        """
        return self._properties['max']

    @max.setter
    def max(self, value):
        """max setter

        TBD

        value: int
        """
        self._properties['max'] = value


class FlowRate(SnappiObject):
    __slots__ = ()

    PPS = 'pps'
    BPS = 'bps'
    KBPS = 'kbps'
    MBPS = 'mbps'
    GBPS = 'gbps'
    PERCENTAGE = 'percentage'

    def __init__(self):
        super(FlowRate, self).__init__()

    @property
    def choice(self):
        # type: () -> Union[pps, bps, kbps, mbps, gbps, percentage, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[pps, bps, kbps, mbps, gbps, percentage, choice, choice, choice]
        """
        return self._properties['choice']

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[pps, bps, kbps, mbps, gbps, percentage, choice, choice, choice]
        """
        self._properties['choice'] = value

    @property
    def pps(self):
        # type: () -> int
        """pps getter

        Packets per second.

        Returns: int
        """
        return self._properties['pps']

    @pps.setter
    def pps(self, value):
        """pps setter

        Packets per second.

        value: int
        """
        self._properties['choice'] = 'pps'
        self._properties['pps'] = value

    @property
    def bps(self):
        # type: () -> int
        """bps getter

        Bits per second.

        Returns: int
        """
        return self._properties['bps']

    @bps.setter
    def bps(self, value):
        """bps setter

        Bits per second.

        value: int
        """
        self._properties['choice'] = 'bps'
        self._properties['bps'] = value

    @property
    def kbps(self):
        # type: () -> int
        """kbps getter

        Kilobits per second.

        Returns: int
        """
        return self._properties['kbps']

    @kbps.setter
    def kbps(self, value):
        """kbps setter

        Kilobits per second.

        value: int
        """
        self._properties['choice'] = 'kbps'
        self._properties['kbps'] = value

    @property
    def mbps(self):
        # type: () -> int
        """mbps getter

        Megabits per second.

        Returns: int
        """
        return self._properties['mbps']

    @mbps.setter
    def mbps(self, value):
        """mbps setter

        Megabits per second.

        value: int
        """
        self._properties['choice'] = 'mbps'
        self._properties['mbps'] = value

    @property
    def gbps(self):
        # type: () -> int
        """gbps getter

        Gigabits per second.

        Returns: int
        """
        return self._properties['gbps']

    @gbps.setter
    def gbps(self, value):
        """gbps setter

        Gigabits per second.

        value: int
        """
        self._properties['choice'] = 'gbps'
        self._properties['gbps'] = value

    @property
    def percentage(self):
        # type: () -> float
        """percentage getter

        The percentage of a port location's available bandwidth.

        Returns: float
        """
        return self._properties['percentage']

    @percentage.setter
    def percentage(self, value):
        """percentage setter

        The percentage of a port location's available bandwidth.

        value: float
        """
        self._properties['choice'] = 'percentage'
        self._properties['percentage'] = value


class FlowDuration(SnappiObject):
    __slots__ = ()

    _TYPES = {
        'fixed_packets': 'FlowFixedPackets',
        'fixed_seconds': 'FlowFixedSeconds',
        'burst': 'FlowBurst',
        'continuous': 'FlowContinuous',
    }

    FIXED_PACKETS = 'fixed_packets'
    FIXED_SECONDS = 'fixed_seconds'
    BURST = 'burst'
    CONTINUOUS = 'continuous'

    def __init__(self):
        super(FlowDuration, self).__init__()

    @property
    def fixed_packets(self):
        # type: () -> FlowFixedPackets
        """Factory method to create an instance of the FlowFixedPackets class

        Transmit a fixed number of packets after which the flow will stop.
        """
        if 'fixed_packets' not in self._properties or self._properties['fixed_packets'] is None:
            self._properties['fixed_packets'] = FlowFixedPackets()
        self.choice = 'fixed_packets'
        return self._properties['fixed_packets']

    @property
    def fixed_seconds(self):
        # type: () -> FlowFixedSeconds
        """Factory method to create an instance of the FlowFixedSeconds class

        Transmit for a fixed number of seconds after which the flow will stop.
        """
        if 'fixed_seconds' not in self._properties or self._properties['fixed_seconds'] is None:
            self._properties['fixed_seconds'] = FlowFixedSeconds()
        self.choice = 'fixed_seconds'
        return self._properties['fixed_seconds']

    @property
    def burst(self):
        # type: () -> FlowBurst
        """Factory method to create an instance of the FlowBurst class

        A continuous burst of packets that will not automatically stop.
        """
        if 'burst' not in self._properties or self._properties['burst'] is None:
            self._properties['burst'] = FlowBurst()
        self.choice = 'burst'
        return self._properties['burst']

    @property
    def continuous(self):
        # type: () -> FlowContinuous
        """Factory method to create an instance of the FlowContinuous class

        Transmit will be continuous and will not stop automatically. 
        """
        if 'continuous' not in self._properties or self._properties['continuous'] is None:
            self._properties['continuous'] = FlowContinuous()
        self.choice = 'continuous'
        return self._properties['continuous']

    @property
    def choice(self):
        # type: () -> Union[fixed_packets, fixed_seconds, burst, continuous, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[fixed_packets, fixed_seconds, burst, continuous, choice, choice, choice]
        """
        return self._properties['choice']

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[fixed_packets, fixed_seconds, burst, continuous, choice, choice, choice]
        """
        self._properties['choice'] = value


class FlowFixedPackets(SnappiObject):
    __slots__ = ()

    BYTES = 'bytes'
    NANOSECONDS = 'nanoseconds'

    def __init__(self, packets=None, gap=None, delay=None, delay_unit=None):
        super(FlowFixedPackets, self).__init__()
        self.packets = packets
        self.gap = gap
        self.delay = delay
        self.delay_unit = delay_unit

    @property
    def packets(self):
        # type: () -> int
        """packets getter

        Stop transmit of the flow after this number of packets.

        Returns: int
        """
        return self._properties['packets']

    @packets.setter
    def packets(self, value):
        """packets setter

        Stop transmit of the flow after this number of packets.

        value: int
        """
        self._properties['packets'] = value

    @property
    def gap(self):
        # type: () -> int
        """gap getter

        The minimum gap between packets expressed as bytes.

        Returns: int
        """
        return self._properties['gap']

    @gap.setter
    def gap(self, value):
        """gap setter

        The minimum gap between packets expressed as bytes.

        value: int
        """
        self._properties['gap'] = value

    @property
    def delay(self):
        # type: () -> int
        """delay getter

        The delay before starting transmission of packets.

        Returns: int
        """
        return self._properties['delay']

    @delay.setter
    def delay(self, value):
        """delay setter

        The delay before starting transmission of packets.

        value: int
        """
        self._properties['delay'] = value

    @property
    def delay_unit(self):
        # type: () -> Union[bytes, nanoseconds]
        """delay_unit getter

        The delay expressed as a number of this value.

        Returns: Union[bytes, nanoseconds]
        """
        return self._properties['delay_unit']

    @delay_unit.setter
    def delay_unit(self, value):
        """delay_unit setter

        The delay expressed as a number of this value.

        value: Union[bytes, nanoseconds]
        """
        self._properties['delay_unit'] = value


class FlowFixedSeconds(SnappiObject):
    __slots__ = ()

    BYTES = 'bytes'
    NANOSECONDS = 'nanoseconds'

    def __init__(self, seconds=None, gap=None, delay=None, delay_unit=None):
        super(FlowFixedSeconds, self).__init__()
        self.seconds = seconds
        self.gap = gap
        self.delay = delay
        self.delay_unit = delay_unit

    @property
    def seconds(self):
        # type: () -> float
        """seconds getter

        Stop transmit of the flow after this number of seconds.

        Returns: float
        """
        return self._properties['seconds']

    @seconds.setter
    def seconds(self, value):
        """seconds setter

        Stop transmit of the flow after this number of seconds.

        value: float
        """
        self._properties['seconds'] = value

    @property
    def gap(self):
        # type: () -> int
        """gap getter

        The minimum gap between packets expressed as bytes.

        Returns: int
        """
        return self._properties['gap']

    @gap.setter
    def gap(self, value):
        """gap setter

        The minimum gap between packets expressed as bytes.

        value: int
        """
        self._properties['gap'] = value

    @property
    def delay(self):
        # type: () -> int
        """delay getter

        The delay before starting transmission of packets.

        Returns: int
        """
        return self._properties['delay']

    @delay.setter
    def delay(self, value):
        """delay setter

        The delay before starting transmission of packets.

        value: int
        """
        self._properties['delay'] = value

    @property
    def delay_unit(self):
        # type: () -> Union[bytes, nanoseconds]
        """delay_unit getter

        The delay expressed as a number of this value.

        Returns: Union[bytes, nanoseconds]
        """
        return self._properties['delay_unit']

    @delay_unit.setter
    def delay_unit(self, value):
        """delay_unit setter

        The delay expressed as a number of this value.

        value: Union[bytes, nanoseconds]
        """
        self._properties['delay_unit'] = value


class FlowBurst(SnappiObject):
    __slots__ = ()

    BYTES = 'bytes'
    NANOSECONDS = 'nanoseconds'

    def __init__(self, packets=None, gap=None, inter_burst_gap=None, inter_burst_gap_unit=None):
        super(FlowBurst, self).__init__()
        self.packets = packets
        self.gap = gap
        self.inter_burst_gap = inter_burst_gap
        self.inter_burst_gap_unit = inter_burst_gap_unit

    @property
    def packets(self):
        # type: () -> int
        """packets getter

        The number of packets transmitted per burst.

        Returns: int
        """
        return self._properties['packets']

    @packets.setter
    def packets(self, value):
        """packets setter

        The number of packets transmitted per burst.

        value: int
        """
        self._properties['packets'] = value

    @property
    def gap(self):
        # type: () -> int
        """gap getter

        The minimum gap between packets expressed as bytes.

        Returns: int
        """
        return self._properties['gap']

    @gap.setter
    def gap(self, value):
        """gap setter

        The minimum gap between packets expressed as bytes.

        value: int
        """
        self._properties['gap'] = value

    @property
    def inter_burst_gap(self):
        # type: () -> int
        """inter_burst_gap getter

        The gap between the transmission of each burst. A value of 0 means there is no gap between bursts.

        Returns: int
        """
        return self._properties['inter_burst_gap']

    @inter_burst_gap.setter
    def inter_burst_gap(self, value):
        """inter_burst_gap setter

        The gap between the transmission of each burst. A value of 0 means there is no gap between bursts.

        value: int
        """
        self._properties['inter_burst_gap'] = value

    @property
    def inter_burst_gap_unit(self):
        # type: () -> Union[bytes, nanoseconds]
        """inter_burst_gap_unit getter

        The inter burst gap expressed as a number of this value.

        Returns: Union[bytes, nanoseconds]
        """
        return self._properties['inter_burst_gap_unit']

    @inter_burst_gap_unit.setter
    def inter_burst_gap_unit(self, value):
        """inter_burst_gap_unit setter

        The inter burst gap expressed as a number of this value.

        value: Union[bytes, nanoseconds]
        """
        self._properties['inter_burst_gap_unit'] = value


class FlowContinuous(SnappiObject):
    __slots__ = ()

    BYTES = 'bytes'
    NANOSECONDS = 'nanoseconds'

    def __init__(self, gap=None, delay=None, delay_unit=None):
        super(FlowContinuous, self).__init__()
        self.gap = gap
        self.delay = delay
        self.delay_unit = delay_unit

    @property
    def gap(self):
        # type: () -> int
        """gap getter

        The minimum gap between packets expressed as bytes.

        Returns: int
        """
        return self._properties['gap']

    @gap.setter
    def gap(self, value):
        """gap setter

        The minimum gap between packets expressed as bytes.

        value: int
        """
        self._properties['gap'] = value

    @property
    def delay(self):
        # type: () -> int
        """delay getter

        The delay before starting transmission of packets.

        Returns: int
        """
        return self._properties['delay']

    @delay.setter
    def delay(self, value):
        """delay setter

        The delay before starting transmission of packets.

        value: int
        """
        self._properties['delay'] = value

    @property
    def delay_unit(self):
        # type: () -> Union[bytes, nanoseconds]
        """delay_unit getter

        The delay expressed as a number of this value.

        Returns: Union[bytes, nanoseconds]
        """
        return self._properties['delay_unit']

    @delay_unit.setter
    def delay_unit(self, value):
        """delay_unit setter

        The delay expressed as a number of this value.

        value: Union[bytes, nanoseconds]
        """
        self._properties['delay_unit'] = value


class FlowList(SnappiList):
    __slots__ = ()

    def __init__(self):
        super(FlowList, self).__init__()

    def __getitem__(self, key):
        # type: (int) -> Flow
        return self._getitem(key)

    def __iter__(self):
        # type: () -> FlowList
        return self._iter()

    def __next__(self):
        # type: () -> Flow
        return self._next()

    def next(self):
        # type: () -> Flow
        return self._next()

    def flow(self, name=None):
        # type: () -> FlowList
        """Factory method that creates an instance of Flow class

        A high level data plane traffic flow. Acts as a container for endpoints, packet headers, packet size, transmit rate and transmit duration.
        """
        item = Flow(name)
        self._add(item)
        return self


class ConfigOptions(SnappiObject):
    __slots__ = ()

    _TYPES = {
        'port_options': 'PortOptions',
    }

    def __init__(self):
        super(ConfigOptions, self).__init__()

    @property
    def port_options(self):
        # type: () -> PortOptions
        """port_options getter

        Common port options that apply to all configured Port objects. 

        Returns: obj(snappi.PortOptions)
        """
        if 'port_options' not in self._properties or self._properties['port_options'] is None:
            self._properties['port_options'] = PortOptions()
        return self._properties['port_options']


class PortOptions(SnappiObject):
    __slots__ = ()

    def __init__(self, location_preemption=None):
        super(PortOptions, self).__init__()
        self.location_preemption = location_preemption

    @property
    def location_preemption(self):
        # type: () -> boolean
        """location_preemption getter

        Preempt all the test port locations as defined by the Port.Port.properties.location. If the test ports defined by their location values are in use and this value is true, the test ports will be preempted.

        Returns: boolean
        """
        return self._properties['location_preemption']

    @location_preemption.setter
    def location_preemption(self, value):
        """location_preemption setter

        Preempt all the test port locations as defined by the Port.Port.properties.location. If the test ports defined by their location values are in use and this value is true, the test ports will be preempted.

        value: boolean
        """
        self._properties['location_preemption'] = value


class TransmitState(SnappiObject):
    __slots__ = ()

    START = 'start'
    STOP = 'stop'
    PAUSE = 'pause'

    def __init__(self, flow_names=None, state=None):
        super(TransmitState, self).__init__()
        self.flow_names = flow_names
        self.state = state

    @property
    def flow_names(self):
        # type: () -> list[str]
        """flow_names getter

        The names of flows to set transmit state on. If the list of flow_names is empty or null the state will be applied to all configured flows.

        Returns: list[str]
        """
        return self._properties['flow_names']

    @flow_names.setter
    def flow_names(self, value):
        """flow_names setter

        The names of flows to set transmit state on. If the list of flow_names is empty or null the state will be applied to all configured flows.

        value: list[str]
        """
        self._properties['flow_names'] = value

    @property
    def state(self):
        # type: () -> Union[start, stop, pause]
        """state getter

        The transmit state.

        Returns: Union[start, stop, pause]
        """
        return self._properties['state']

    @state.setter
    def state(self, value):
        """state setter

        The transmit state.

        value: Union[start, stop, pause]
        """
        self._properties['state'] = value


class LinkState(SnappiObject):
    __slots__ = ()

    UP = 'up'
    DOWN = 'down'

    def __init__(self, port_names=None, state=None):
        super(LinkState, self).__init__()
        self.port_names = port_names
        self.state = state

    @property
    def port_names(self):
        # type: () -> list[str]
        """port_names getter

        The names of port objects to. An empty or null list will control all port objects.

        Returns: list[str]
        """
        return self._properties['port_names']

    @port_names.setter
    def port_names(self, value):
        """port_names setter

        The names of port objects to. An empty or null list will control all port objects.

        value: list[str]
        """
        self._properties['port_names'] = value

    @property
    def state(self):
        # type: () -> Union[up, down]
        """state getter

        The link state.

        Returns: Union[up, down]
        """
        return self._properties['state']

    @state.setter
    def state(self, value):
        """state setter

        The link state.

        value: Union[up, down]
        """
        self._properties['state'] = value


class CaptureState(SnappiObject):
    __slots__ = ()

    START = 'start'
    STOP = 'stop'

    def __init__(self, port_names=None, state=None):
        super(CaptureState, self).__init__()
        self.port_names = port_names
        self.state = state

    @property
    def port_names(self):
        # type: () -> list[str]
        """port_names getter

        The name of ports to start capturing packets on. An empty or null list will control all port objects.

        Returns: list[str]
        """
        return self._properties['port_names']

    @port_names.setter
    def port_names(self, value):
        """port_names setter

        The name of ports to start capturing packets on. An empty or null list will control all port objects.

        value: list[str]
        """
        self._properties['port_names'] = value

    @property
    def state(self):
        # type: () -> Union[start, stop]
        """state getter

        The capture state.

        Returns: Union[start, stop]
        """
        return self._properties['state']

    @state.setter
    def state(self, value):
        """state setter

        The capture state.

        value: Union[start, stop]
        """
        self._properties['state'] = value


class StateMetrics(SnappiObject):
    __slots__ = ()

    _TYPES = {
        'port_state': 'PortStateList',
        'flow_state': 'FlowStateList',
    }

    def __init__(self):
        super(StateMetrics, self).__init__()

    @property
    def port_state(self):
        # type: () -> PortStateList
        """port_state getter

        TBD

        Returns: list[obj(snappi.PortState)]
        """
        if 'port_state' not in self._properties or self._properties['port_state'] is None:
            self._properties['port_state'] = PortStateList()
        return self._properties['port_state']

    @property
    def flow_state(self):
        # type: () -> FlowStateList
        """flow_state getter

        TBD

        Returns: list[obj(snappi.FlowState)]
        """
        if 'flow_state' not in self._properties or self._properties['flow_state'] is None:
            self._properties['flow_state'] = FlowStateList()
        return self._properties['flow_state']


class PortState(SnappiObject):
    __slots__ = ()

    UP = 'up'
    DOWN = 'down'

    STARTED = 'started'
    STOPPED = 'stopped'

    def __init__(self, name=None, link=None, capture=None):
        super(PortState, self).__init__()
        self.name = name
        self.link = link
        self.capture = capture

    @property
    def name(self):
        # type: () -> str
        """name getter

        TBD

        Returns: str
        """
        return self._properties['name']

    @name.setter
    def name(self, value):
        """name setter

        TBD

        value: str
        """
        self._properties['name'] = value

    @property
    def link(self):
        # type: () -> Union[up, down]
        """link getter

        TBD

        Returns: Union[up, down]
        """
        return self._properties['link']

    @link.setter
    def link(self, value):
        """link setter

        TBD

        value: Union[up, down]
        """
        self._properties['link'] = value

    @property
    def capture(self):
        # type: () -> Union[started, stopped]
        """capture getter

        TBD

        Returns: Union[started, stopped]
        """
        return self._properties['capture']

    @capture.setter
    def capture(self, value):
        """capture setter

        TBD

        value: Union[started, stopped]
        """
        self._properties['capture'] = value


class PortStateList(SnappiList):
    __slots__ = ()

    def __init__(self):
        super(PortStateList, self).__init__()

    def __getitem__(self, key):
        # type: (int) -> PortState
        return self._getitem(key)

    def __iter__(self):
        # type: () -> PortStateList
        return self._iter()

    def __next__(self):
        # type: () -> PortState
        return self._next()

    def next(self):
        # type: () -> PortState
        return self._next()

    def state(self, name=None, link='None', capture='None'):
        # type: () -> PortStateList
        """Factory method that creates an instance of PortState class

        TBD
        """
        item = PortState(name, link, capture)
        self._add(item)
        return self


class FlowState(SnappiObject):
    __slots__ = ()

    STARTED = 'started'
    STOPPED = 'stopped'
    PAUSED = 'paused'

    def __init__(self, name=None, transmit=None):
        super(FlowState, self).__init__()
        self.name = name
        self.transmit = transmit

    @property
    def name(self):
        # type: () -> str
        """name getter

        TBD

        Returns: str
        """
        return self._properties['name']

    @name.setter
    def name(self, value):
        """name setter

        TBD

        value: str
        """
        self._properties['name'] = value

    @property
    def transmit(self):
        # type: () -> Union[started, stopped, paused]
        """transmit getter

        TBD

        Returns: Union[started, stopped, paused]
        """
        return self._properties['transmit']

    @transmit.setter
    def transmit(self, value):
        """transmit setter

        TBD

        value: Union[started, stopped, paused]
        """
        self._properties['transmit'] = value


class FlowStateList(SnappiList):
    __slots__ = ()

    def __init__(self):
        super(FlowStateList, self).__init__()

    def __getitem__(self, key):
        # type: (int) -> FlowState
        return self._getitem(key)

    def __iter__(self):
        # type: () -> FlowStateList
        return self._iter()

    def __next__(self):
        # type: () -> FlowState
        return self._next()

    def next(self):
        # type: () -> FlowState
        return self._next()

    def state(self, name=None, transmit='None'):
        # type: () -> FlowStateList
        """Factory method that creates an instance of FlowState class

        TBD
        """
        item = FlowState(name, transmit)
        self._add(item)
        return self


class Capabilities(SnappiObject):
    __slots__ = ()

    def __init__(self, unsupported=None, formats=None):
        super(Capabilities, self).__init__()
        self.unsupported = unsupported
        self.formats = formats

    @property
    def unsupported(self):
        # type: () -> list[str]
        """unsupported getter

        A list of /components/schemas/... paths that are not supported.

        Returns: list[str]
        """
        return self._properties['unsupported']

    @unsupported.setter
    def unsupported(self, value):
        """unsupported setter

        A list of /components/schemas/... paths that are not supported.

        value: list[str]
        """
        self._properties['unsupported'] = value

    @property
    def formats(self):
        # type: () -> list[str]
        """formats getter

        A /components/schemas/... path and specific format details regarding the path. Specific model format details can be additional objects and properties represented as a hashmap. For example layer1 models are defined as a hashmap key to object with each object consisting of a specific name/value property pairs. This list of items will detail any specific formats, properties, enums.

        Returns: list[str]
        """
        return self._properties['formats']

    @formats.setter
    def formats(self, value):
        """formats setter

        A /components/schemas/... path and specific format details regarding the path. Specific model format details can be additional objects and properties represented as a hashmap. For example layer1 models are defined as a hashmap key to object with each object consisting of a specific name/value property pairs. This list of items will detail any specific formats, properties, enums.

        value: list[str]
        """
        self._properties['formats'] = value


class PortMetricsRequest(SnappiObject):
    __slots__ = ()

    TRANSMIT = 'transmit'
    LOCATION = 'location'
    LINK = 'link'
    CAPTURE = 'capture'
    FRAMES_TX = 'frames_tx'
    FRAMES_RX = 'frames_rx'
    BYTES_TX = 'bytes_tx'
    BYTES_RX = 'bytes_rx'
    FRAMES_TX_RATE = 'frames_tx_rate'
    FRAMES_RX_RATE = 'frames_rx_rate'
    BYTES_TX_RATE = 'bytes_tx_rate'
    BYTES_RX_RATE = 'bytes_rx_rate'

    def __init__(self, port_names=None, column_names=None):
        super(PortMetricsRequest, self).__init__()
        self.port_names = port_names
        self.column_names = column_names

    @property
    def port_names(self):
        # type: () -> list[str]
        """port_names getter

        The names of objects to return results for. An empty list will return all port row results.

        Returns: list[str]
        """
        return self._properties['port_names']

    @port_names.setter
    def port_names(self, value):
        """port_names setter

        The names of objects to return results for. An empty list will return all port row results.

        value: list[str]
        """
        self._properties['port_names'] = value

    @property
    def column_names(self):
        # type: () -> list[Union[transmit, location, link, capture, frames_tx, frames_rx, bytes_tx, bytes_rx, frames_tx_rate, frames_rx_rate, bytes_tx_rate, bytes_rx_rate]]
        """column_names getter

        The list of column names that the returned result set will contain. If the list is empty then all columns will be returned. The name of the port cannot be excluded.

        Returns: list[Union[transmit, location, link, capture, frames_tx, frames_rx, bytes_tx, bytes_rx, frames_tx_rate, frames_rx_rate, bytes_tx_rate, bytes_rx_rate]]
        """
        return self._properties['column_names']

    @column_names.setter
    def column_names(self, value):
        """column_names setter

        The list of column names that the returned result set will contain. If the list is empty then all columns will be returned. The name of the port cannot be excluded.

        value: list[Union[transmit, location, link, capture, frames_tx, frames_rx, bytes_tx, bytes_rx, frames_tx_rate, frames_rx_rate, bytes_tx_rate, bytes_rx_rate]]
        """
        self._properties['column_names'] = value


class PortMetricList(SnappiList):
    __slots__ = ()

    def __init__(self):
        super(PortMetricList, self).__init__()

    def __getitem__(self, key):
        # type: (int) -> PortMetric
        return self._getitem(key)

    def __iter__(self):
        # type: () -> PortMetricList
        return self._iter()

    def __next__(self):
        # type: () -> PortMetric
        return self._next()

    def next(self):
        # type: () -> PortMetric
        return self._next()

    def metric(self, name=None, location=None, link='None', capture='None', frames_tx=None, frames_rx=None, bytes_tx=None, bytes_rx=None, frames_tx_rate=None, frames_rx_rate=None, bytes_tx_rate=None, bytes_rx_rate=None):
        # type: () -> PortMetricList
        """Factory method that creates an instance of PortMetric class

        TBD
        """
        item = PortMetric(name, location, link, capture, frames_tx, frames_rx, bytes_tx, bytes_rx, frames_tx_rate, frames_rx_rate, bytes_tx_rate, bytes_rx_rate)
        self._add(item)
        return self


class PortMetric(SnappiObject):
    __slots__ = ()

    UP = 'up'
    DOWN = 'down'

    STARTED = 'started'
    STOPPED = 'stopped'

    def __init__(self, name=None, location=None, link=None, capture=None, frames_tx=None, frames_rx=None, bytes_tx=None, bytes_rx=None, frames_tx_rate=None, frames_rx_rate=None, bytes_tx_rate=None, bytes_rx_rate=None):
        super(PortMetric, self).__init__()
        self.name = name
        self.location = location
        self.link = link
        self.capture = capture
        self.frames_tx = frames_tx
        self.frames_rx = frames_rx
        self.bytes_tx = bytes_tx
        self.bytes_rx = bytes_rx
        self.frames_tx_rate = frames_tx_rate
        self.frames_rx_rate = frames_rx_rate
        self.bytes_tx_rate = bytes_tx_rate
        self.bytes_rx_rate = bytes_rx_rate

    @property
    def name(self):
        # type: () -> str
        """name getter

        The name of a configured port

        Returns: str
        """
        return self._properties['name']

    @name.setter
    def name(self, value):
        """name setter

        The name of a configured port

        value: str
        """
        self._properties['name'] = value

    @property
    def location(self):
        # type: () -> str
        """location getter

        The state of the connection to the test port location. The format should be the configured port location along with any custom connection state message.

        Returns: str
        """
        return self._properties['location']

    @location.setter
    def location(self, value):
        """location setter

        The state of the connection to the test port location. The format should be the configured port location along with any custom connection state message.

        value: str
        """
        self._properties['location'] = value

    @property
    def link(self):
        # type: () -> Union[up, down]
        """link getter

        The state of the test port link The string can be up, down or a custom error message.

        Returns: Union[up, down]
        """
        return self._properties['link']

    @link.setter
    def link(self, value):
        """link setter

        The state of the test port link The string can be up, down or a custom error message.

        value: Union[up, down]
        """
        self._properties['link'] = value

    @property
    def capture(self):
        # type: () -> Union[started, stopped]
        """capture getter

        The state of the test port capture infrastructure. The string can be started, stopped or a custom error message.

        Returns: Union[started, stopped]
        """
        return self._properties['capture']

    @capture.setter
    def capture(self, value):
        """capture setter

        The state of the test port capture infrastructure. The string can be started, stopped or a custom error message.

        value: Union[started, stopped]
        """
        self._properties['capture'] = value

    @property
    def frames_tx(self):
        # type: () -> int
        """frames_tx getter

        The current total number of frames transmitted

        Returns: int
        """
        return self._properties['frames_tx']

    @frames_tx.setter
    def frames_tx(self, value):
        """frames_tx setter

        The current total number of frames transmitted

        value: int
        """
        self._properties['frames_tx'] = value

    @property
    def frames_rx(self):
        # type: () -> int
        """frames_rx getter

        The current total number of valid frames received

        Returns: int
        """
        return self._properties['frames_rx']

    @frames_rx.setter
    def frames_rx(self, value):
        """frames_rx setter

        The current total number of valid frames received

        value: int
        """
        self._properties['frames_rx'] = value

    @property
    def bytes_tx(self):
        # type: () -> int
        """bytes_tx getter

        The current total number of bytes transmitted

        Returns: int
        """
        return self._properties['bytes_tx']

    @bytes_tx.setter
    def bytes_tx(self, value):
        """bytes_tx setter

        The current total number of bytes transmitted

        value: int
        """
        self._properties['bytes_tx'] = value

    @property
    def bytes_rx(self):
        # type: () -> int
        """bytes_rx getter

        The current total number of valid bytes received

        Returns: int
        """
        return self._properties['bytes_rx']

    @bytes_rx.setter
    def bytes_rx(self, value):
        """bytes_rx setter

        The current total number of valid bytes received

        value: int
        """
        self._properties['bytes_rx'] = value

    @property
    def frames_tx_rate(self):
        # type: () -> float
        """frames_tx_rate getter

        The current rate of frames transmitted

        Returns: float
        """
        return self._properties['frames_tx_rate']

    @frames_tx_rate.setter
    def frames_tx_rate(self, value):
        """frames_tx_rate setter

        The current rate of frames transmitted

        value: float
        """
        self._properties['frames_tx_rate'] = value

    @property
    def frames_rx_rate(self):
        # type: () -> float
        """frames_rx_rate getter

        The current rate of valid frames received

        Returns: float
        """
        return self._properties['frames_rx_rate']

    @frames_rx_rate.setter
    def frames_rx_rate(self, value):
        """frames_rx_rate setter

        The current rate of valid frames received

        value: float
        """
        self._properties['frames_rx_rate'] = value

    @property
    def bytes_tx_rate(self):
        # type: () -> float
        """bytes_tx_rate getter

        The current rate of bytes transmitted

        Returns: float
        """
        return self._properties['bytes_tx_rate']

    @bytes_tx_rate.setter
    def bytes_tx_rate(self, value):
        """bytes_tx_rate setter

        The current rate of bytes transmitted

        value: float
        """
        self._properties['bytes_tx_rate'] = value

    @property
    def bytes_rx_rate(self):
        # type: () -> float
        """bytes_rx_rate getter

        The current rate of bytes received

        Returns: float
        """
        return self._properties['bytes_rx_rate']

    @bytes_rx_rate.setter
    def bytes_rx_rate(self, value):
        """bytes_rx_rate setter

        The current rate of bytes received

        value: float
        """
        self._properties['bytes_rx_rate'] = value


class CaptureRequest(SnappiObject):
    __slots__ = ()

    def __init__(self, port_name=None):
        super(CaptureRequest, self).__init__()
        self.port_name = port_name

    @property
    def port_name(self):
        # type: () -> str
        """port_name getter

        The name of a port a capture is started on.

        Returns: str
        """
        return self._properties['port_name']

    @port_name.setter
    def port_name(self, value):
        """port_name setter

        The name of a port a capture is started on.

        value: str
        """
        self._properties['port_name'] = value


class FlowMetricsRequest(SnappiObject):
    __slots__ = ()

    TRANSMIT = 'transmit'
    PORT_TX = 'port_tx'
    PORT_RX = 'port_rx'
    FRAMES_TX = 'frames_tx'
    FRAMES_RX = 'frames_rx'
    BYTES_TX = 'bytes_tx'
    BYTES_RX = 'bytes_rx'
    FRAMES_TX_RATE = 'frames_tx_rate'
    FRAMES_RX_RATE = 'frames_rx_rate'
    LOSS = 'loss'

    def __init__(self, flow_names=None, column_names=None, metric_group_names=None):
        super(FlowMetricsRequest, self).__init__()
        self.flow_names = flow_names
        self.column_names = column_names
        self.metric_group_names = metric_group_names

    @property
    def flow_names(self):
        # type: () -> list[str]
        """flow_names getter

        The names of flow objects to return results for. An empty list will return results for all flows.

        Returns: list[str]
        """
        return self._properties['flow_names']

    @flow_names.setter
    def flow_names(self, value):
        """flow_names setter

        The names of flow objects to return results for. An empty list will return results for all flows.

        value: list[str]
        """
        self._properties['flow_names'] = value

    @property
    def column_names(self):
        # type: () -> list[Union[transmit, port_tx, port_rx, frames_tx, frames_rx, bytes_tx, bytes_rx, frames_tx_rate, frames_rx_rate, loss]]
        """column_names getter

        The list of column names that the returned result set will contain. If the list is empty then all columns will be returned except for any result_groups. The name of the flow cannot be excluded.

        Returns: list[Union[transmit, port_tx, port_rx, frames_tx, frames_rx, bytes_tx, bytes_rx, frames_tx_rate, frames_rx_rate, loss]]
        """
        return self._properties['column_names']

    @column_names.setter
    def column_names(self, value):
        """column_names setter

        The list of column names that the returned result set will contain. If the list is empty then all columns will be returned except for any result_groups. The name of the flow cannot be excluded.

        value: list[Union[transmit, port_tx, port_rx, frames_tx, frames_rx, bytes_tx, bytes_rx, frames_tx_rate, frames_rx_rate, loss]]
        """
        self._properties['column_names'] = value

    @property
    def metric_group_names(self):
        # type: () -> list[str]
        """metric_group_names getter

        Extend the details of flow metrics by specifying any configured flow packet header field metric_group names.

        Returns: list[str]
        """
        return self._properties['metric_group_names']

    @metric_group_names.setter
    def metric_group_names(self, value):
        """metric_group_names setter

        Extend the details of flow metrics by specifying any configured flow packet header field metric_group names.

        value: list[str]
        """
        self._properties['metric_group_names'] = value


class FlowMetricList(SnappiList):
    __slots__ = ()

    def __init__(self):
        super(FlowMetricList, self).__init__()

    def __getitem__(self, key):
        # type: (int) -> FlowMetric
        return self._getitem(key)

    def __iter__(self):
        # type: () -> FlowMetricList
        return self._iter()

    def __next__(self):
        # type: () -> FlowMetric
        return self._next()

    def next(self):
        # type: () -> FlowMetric
        return self._next()

    def metric(self, name=None, transmit='None', port_tx=None, port_rx=None, frames_tx=None, frames_rx=None, bytes_tx=None, bytes_rx=None, frames_tx_rate=None, frames_rx_rate=None, loss=None):
        # type: () -> FlowMetricList
        """Factory method that creates an instance of FlowMetric class

        TBD
        """
        item = FlowMetric(name, transmit, port_tx, port_rx, frames_tx, frames_rx, bytes_tx, bytes_rx, frames_tx_rate, frames_rx_rate, loss)
        self._add(item)
        return self


class FlowMetric(SnappiObject):
    __slots__ = ()

    _TYPES = {
        'metric_groups': 'FlowMetricGroupList',
    }

    STARTED = 'started'
    STOPPED = 'stopped'
    PAUSED = 'paused'

    def __init__(self, name=None, transmit=None, port_tx=None, port_rx=None, frames_tx=None, frames_rx=None, bytes_tx=None, bytes_rx=None, frames_tx_rate=None, frames_rx_rate=None, loss=None):
        super(FlowMetric, self).__init__()
        self.name = name
        self.transmit = transmit
        self.port_tx = port_tx
        self.port_rx = port_rx
        self.frames_tx = frames_tx
        self.frames_rx = frames_rx
        self.bytes_tx = bytes_tx
        self.bytes_rx = bytes_rx
        self.frames_tx_rate = frames_tx_rate
        self.frames_rx_rate = frames_rx_rate
        self.loss = loss

    @property
    def name(self):
        # type: () -> str
        """name getter

        The name of a configured flow.

        Returns: str
        """
        return self._properties['name']

    @name.setter
    def name(self, value):
        """name setter

        The name of a configured flow.

        value: str
        """
        self._properties['name'] = value

    @property
    def transmit(self):
        # type: () -> Union[started, stopped, paused]
        """transmit getter

        The transmit state of the flow.

        Returns: Union[started, stopped, paused]
        """
        return self._properties['transmit']

    @transmit.setter
    def transmit(self, value):
        """transmit setter

        The transmit state of the flow.

        value: Union[started, stopped, paused]
        """
        self._properties['transmit'] = value

    @property
    def port_tx(self):
        # type: () -> str
        """port_tx getter

        The name of a configured port

        Returns: str
        """
        return self._properties['port_tx']

    @port_tx.setter
    def port_tx(self, value):
        """port_tx setter

        The name of a configured port

        value: str
        """
        self._properties['port_tx'] = value

    @property
    def port_rx(self):
        # type: () -> str
        """port_rx getter

        The name of a configured port

        Returns: str
        """
        return self._properties['port_rx']

    @port_rx.setter
    def port_rx(self, value):
        """port_rx setter

        The name of a configured port

        value: str
        """
        self._properties['port_rx'] = value

    @property
    def frames_tx(self):
        # type: () -> int
        """frames_tx getter

        The current total number of frames transmitted

        Returns: int
        """
        return self._properties['frames_tx']

    @frames_tx.setter
    def frames_tx(self, value):
        """frames_tx setter

        The current total number of frames transmitted

        value: int
        """
        self._properties['frames_tx'] = value

    @property
    def frames_rx(self):
        # type: () -> int
        """frames_rx getter

        The current total number of valid frames received

        Returns: int
        """
        return self._properties['frames_rx']

    @frames_rx.setter
    def frames_rx(self, value):
        """frames_rx setter

        The current total number of valid frames received

        value: int
        """
        self._properties['frames_rx'] = value

    @property
    def bytes_tx(self):
        # type: () -> int
        """bytes_tx getter

        The current total number of bytes transmitted

        Returns: int
        """
        return self._properties['bytes_tx']

    @bytes_tx.setter
    def bytes_tx(self, value):
        """bytes_tx setter

        The current total number of bytes transmitted

        value: int
        """
        self._properties['bytes_tx'] = value

    @property
    def bytes_rx(self):
        # type: () -> int
        """bytes_rx getter

        The current total number of bytes received

        Returns: int
        """
        return self._properties['bytes_rx']

    @bytes_rx.setter
    def bytes_rx(self, value):
        """bytes_rx setter

        The current total number of bytes received

        value: int
        """
        self._properties['bytes_rx'] = value

    @property
    def frames_tx_rate(self):
        # type: () -> float
        """frames_tx_rate getter

        The current rate of frames transmitted

        Returns: float
        """
        return self._properties['frames_tx_rate']

    @frames_tx_rate.setter
    def frames_tx_rate(self, value):
        """frames_tx_rate setter

        The current rate of frames transmitted

        value: float
        """
        self._properties['frames_tx_rate'] = value

    @property
    def frames_rx_rate(self):
        # type: () -> float
        """frames_rx_rate getter

        The current rate of valid frames received

        Returns: float
        """
        return self._properties['frames_rx_rate']

    @frames_rx_rate.setter
    def frames_rx_rate(self, value):
        """frames_rx_rate setter

        The current rate of valid frames received

        value: float
        """
        self._properties['frames_rx_rate'] = value

    @property
    def loss(self):
        # type: () -> float
        """loss getter

        The percentage of lost frames

        Returns: float
        """
        return self._properties['loss']

    @loss.setter
    def loss(self, value):
        """loss setter

        The percentage of lost frames

        value: float
        """
        self._properties['loss'] = value

    @property
    def metric_groups(self):
        # type: () -> FlowMetricGroupList
        """metric_groups getter

        Any configured flow packet header field metric_group names will appear as additional name/value pairs.

        Returns: list[obj(snappi.FlowMetricGroup)]
        """
        if 'metric_groups' not in self._properties or self._properties['metric_groups'] is None:
            self._properties['metric_groups'] = FlowMetricGroupList()
        return self._properties['metric_groups']


class FlowMetricGroup(SnappiObject):
    __slots__ = ()

    def __init__(self, name=None, value=None):
        super(FlowMetricGroup, self).__init__()
        self.name = name
        self.value = value

    @property
    def name(self):
        # type: () -> str
        """name getter

        Name provided as part of a flow packet header field metric group

        Returns: str
        """
        return self._properties['name']

    @name.setter
    def name(self, value):
        """name setter

        Name provided as part of a flow packet header field metric group

        value: str
        """
        self._properties['name'] = value

    @property
    def value(self):
        # type: () -> float
        """value getter

        The value of the flow packet header field

        Returns: float
        """
        return self._properties['value']

    @value.setter
    def value(self, value):
        """value setter

        The value of the flow packet header field

        value: float
        """
        self._properties['value'] = value


class FlowMetricGroupList(SnappiList):
    __slots__ = ()

    def __init__(self):
        super(FlowMetricGroupList, self).__init__()

    def __getitem__(self, key):
        # type: (int) -> FlowMetricGroup
        return self._getitem(key)

    def __iter__(self):
        # type: () -> FlowMetricGroupList
        return self._iter()

    def __next__(self):
        # type: () -> FlowMetricGroup
        return self._next()

    def next(self):
        # type: () -> FlowMetricGroup
        return self._next()

    def metricgroup(self, name=None, value=None):
        # type: () -> FlowMetricGroupList
        """Factory method that creates an instance of FlowMetricGroup class

        A metric group
        """
        item = FlowMetricGroup(name, value)
        self._add(item)
        return self


class Bgpv4MetricsRequest(SnappiObject):
    __slots__ = ()

    def __init__(self, names=None):
        super(Bgpv4MetricsRequest, self).__init__()
        self.names = names

    @property
    def names(self):
        # type: () -> list[str]
        """names getter

        The names of BGP objects to return results for. An empty list will return results for all BGP.

        Returns: list[str]
        """
        return self._properties['names']

    @names.setter
    def names(self, value):
        """names setter

        The names of BGP objects to return results for. An empty list will return results for all BGP.

        value: list[str]
        """
        self._properties['names'] = value


class Bgpv4Metrics(SnappiObject):
    __slots__ = ()

    _TYPES = {
        'ports': 'Bgpv4MetricList',
    }

    def __init__(self):
        super(Bgpv4Metrics, self).__init__()

    @property
    def ports(self):
        # type: () -> Bgpv4MetricList
        """ports getter

        TBD

        Returns: list[obj(snappi.Bgpv4Metric)]
        """
        if 'ports' not in self._properties or self._properties['ports'] is None:
            self._properties['ports'] = Bgpv4MetricList()
        return self._properties['ports']


class Bgpv4Metric(SnappiObject):
    __slots__ = ()

    def __init__(self, name=None, sessions_total=None, sessions_up=None, sessions_down=None, sessions_not_started=None, routes_advertised=None, routes_withdrawn=None):
        super(Bgpv4Metric, self).__init__()
        self.name = name
        self.sessions_total = sessions_total
        self.sessions_up = sessions_up
        self.sessions_down = sessions_down
        self.sessions_not_started = sessions_not_started
        self.routes_advertised = routes_advertised
        self.routes_withdrawn = routes_withdrawn

    @property
    def name(self):
        # type: () -> str
        """name getter

        The name of a configured BGPv4 Object.

        Returns: str
        """
        return self._properties['name']

    @name.setter
    def name(self, value):
        """name setter

        The name of a configured BGPv4 Object.

        value: str
        """
        self._properties['name'] = value

    @property
    def sessions_total(self):
        # type: () -> int
        """sessions_total getter

        Total number of session

        Returns: int
        """
        return self._properties['sessions_total']

    @sessions_total.setter
    def sessions_total(self, value):
        """sessions_total setter

        Total number of session

        value: int
        """
        self._properties['sessions_total'] = value

    @property
    def sessions_up(self):
        # type: () -> int
        """sessions_up getter

        Sessions are in active state

        Returns: int
        """
        return self._properties['sessions_up']

    @sessions_up.setter
    def sessions_up(self, value):
        """sessions_up setter

        Sessions are in active state

        value: int
        """
        self._properties['sessions_up'] = value

    @property
    def sessions_down(self):
        # type: () -> int
        """sessions_down getter

        Sessions are not active state

        Returns: int
        """
        return self._properties['sessions_down']

    @sessions_down.setter
    def sessions_down(self, value):
        """sessions_down setter

        Sessions are not active state

        value: int
        """
        self._properties['sessions_down'] = value

    @property
    def sessions_not_started(self):
        # type: () -> int
        """sessions_not_started getter

        Sessions not able to start due to some internal issue

        Returns: int
        """
        return self._properties['sessions_not_started']

    @sessions_not_started.setter
    def sessions_not_started(self, value):
        """sessions_not_started setter

        Sessions not able to start due to some internal issue

        value: int
        """
        self._properties['sessions_not_started'] = value

    @property
    def routes_advertised(self):
        # type: () -> int
        """routes_advertised getter

        Number of advertised routes sent

        Returns: int
        """
        return self._properties['routes_advertised']

    @routes_advertised.setter
    def routes_advertised(self, value):
        """routes_advertised setter

        Number of advertised routes sent

        value: int
        """
        self._properties['routes_advertised'] = value

    @property
    def routes_withdrawn(self):
        # type: () -> int
        """routes_withdrawn getter

        Number of routes withdrawn

        Returns: int
        """
        return self._properties['routes_withdrawn']

    @routes_withdrawn.setter
    def routes_withdrawn(self, value):
        """routes_withdrawn setter

        Number of routes withdrawn

        value: int
        """
        self._properties['routes_withdrawn'] = value


class Bgpv4MetricList(SnappiList):
    __slots__ = ()

    def __init__(self):
        super(Bgpv4MetricList, self).__init__()

    def __getitem__(self, key):
        # type: (int) -> Bgpv4Metric
        return self._getitem(key)

    def __iter__(self):
        # type: () -> Bgpv4MetricList
        return self._iter()

    def __next__(self):
        # type: () -> Bgpv4Metric
        return self._next()

    def next(self):
        # type: () -> Bgpv4Metric
        return self._next()

    def metric(self, name=None, sessions_total=None, sessions_up=None, sessions_down=None, sessions_not_started=None, routes_advertised=None, routes_withdrawn=None):
        # type: () -> Bgpv4MetricList
        """Factory method that creates an instance of Bgpv4Metric class

        BGP Router statistics and learned routing information
        """
        item = Bgpv4Metric(name, sessions_total, sessions_up, sessions_down, sessions_not_started, routes_advertised, routes_withdrawn)
        self._add(item)
        return self
