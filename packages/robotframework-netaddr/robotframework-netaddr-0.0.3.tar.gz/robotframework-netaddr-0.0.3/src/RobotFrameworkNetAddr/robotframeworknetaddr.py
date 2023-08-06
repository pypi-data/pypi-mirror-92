import netaddr


class RobotFrameworkNetAddr():
    ''' Wrapper functions to access a selection of the python netaddr library from robot framework.

    Most of the functionality from the netaddr IPNetwork, IPAddress and EUI classes are implemented
    along with a couple of extra functions to provide more ease of use in robot framework.
    '''

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    # netaddr.IPNetwork class
    @staticmethod
    def ipnetwork_broadcast(addr, implicit_prefix=False, version=None, flags=0):
        return netaddr.IPNetwork(addr, implicit_prefix, version, flags).broadcast

    @staticmethod
    def ipnetwork_cidr(addr, implicit_prefix=False, version=None, flags=0):
        return netaddr.IPNetwork(addr, implicit_prefix, version, flags).cidr

    @staticmethod
    def ipnetwork_hostmask(addr, implicit_prefix=False, version=None, flags=0):
        return netaddr.IPNetwork(addr, implicit_prefix, version, flags).hostmask

    @staticmethod
    def ipnetwork_info(addr, implicit_prefix=False, version=None, flags=0):
        return netaddr.IPNetwork(addr, implicit_prefix, version, flags).info

    @staticmethod
    def ipnetwork_ip(addr, implicit_prefix=False, version=None, flags=0):
        return netaddr.IPNetwork(addr, implicit_prefix, version, flags).ip

    @staticmethod
    def ipnetwork_is_link_local(addr, implicit_prefix=False, version=None, flags=0):
        return netaddr.IPNetwork(addr, implicit_prefix, version, flags).is_link_local()

    @staticmethod
    def ipnetwork_is_loopback(addr, implicit_prefix=False, version=None, flags=0):
        return netaddr.IPNetwork(addr, implicit_prefix, version, flags).is_loopback()

    @staticmethod
    def ipnetwork_is_multicast(addr, implicit_prefix=False, version=None, flags=0):
        return netaddr.IPNetwork(addr, implicit_prefix, version, flags).is_multicast()

    @staticmethod
    def ipnetwork_is_private(addr, implicit_prefix=False, version=None, flags=0):
        return netaddr.IPNetwork(addr, implicit_prefix, version, flags).is_private()

    @staticmethod
    def ipnetwork_is_reserved(addr, implicit_prefix=False, version=None, flags=0):
        return netaddr.IPNetwork(addr, implicit_prefix, version, flags).is_reserved()

    @staticmethod
    def ipnetwork_is_unicast(addr, implicit_prefix=False, version=None, flags=0):
        return netaddr.IPNetwork(addr, implicit_prefix, version, flags).is_unicast()

    @staticmethod
    def ipnetwork_netmask(addr, implicit_prefix=False, version=None, flags=0):
        return netaddr.IPNetwork(addr, implicit_prefix, version, flags).netmask

    @staticmethod
    def ipnetwork_network(addr, implicit_prefix=False, version=None, flags=0):
        return netaddr.IPNetwork(addr, implicit_prefix, version, flags).network

    @staticmethod
    def ipnetwork_prefixlen(addr, implicit_prefix=False, version=None, flags=0):
        return netaddr.IPNetwork(addr, implicit_prefix, version, flags).prefixlen

    @staticmethod
    def ipnetwork_size(addr, implicit_prefix=False, version=None, flags=0):
        return netaddr.IPNetwork(addr, implicit_prefix, version, flags).size

    @staticmethod
    def ipnetwork_version(addr, implicit_prefix=False, version=None, flags=0):
        return netaddr.IPNetwork(addr, implicit_prefix, version, flags).version

    @staticmethod
    def ipnetwork_is_network_addr(addr, implicit_prefix=False, version=None, flags=0):
        net = netaddr.IPNetwork(addr, implicit_prefix, version, flags)
        return net.ip == net.network

    @staticmethod
    def ipnetwork_is_valid_ipv4(addr):
        try:
            netaddr.IPNetwork(addr, version=4)
        except:
            return False
        else:
            return True

    @staticmethod
    def ipnetwork_is_valid_ipv6(addr):
        try:
            netaddr.IPNetwork(addr, version=6)
        except:
            return False
        else:
            return True

    @staticmethod
    def ipnetwork_previous(addr, implicit_prefix=False, version=None, flags=0):
        try:
            prev_net = netaddr.IPNetwork(addr, implicit_prefix, version, flags).previous()
        except:
            return False
        else:
            return prev_net

    @staticmethod
    def ipnetwork_next(addr, implicit_prefix=False, version=None, flags=0):
        try:
            next_net = netaddr.IPNetwork(addr, implicit_prefix, version, flags).next()
        except:
            return False
        else:
            return next_net

    @staticmethod
    def ipnetwork_in_network(addr, addr2):
        return netaddr.IPNetwork(addr) in netaddr.IPNetwork(addr2)

    # netaddr.IPAddress class
    @staticmethod
    def ipaddress_bin(addr, version=None, flags=0):
        return netaddr.IPAddress(addr, version, flags).bin

    @staticmethod
    def ipaddress_bits(addr, version=None, flags=0):
        return netaddr.IPAddress(addr, version, flags).bits()

    @staticmethod
    def ipaddress_info(addr, version=None, flags=0):
        return netaddr.IPAddress(addr, version, flags).info

    @staticmethod
    def ipaddress_is_hostmask(addr, version=None, flags=0):
        return netaddr.IPAddress(addr, version, flags).is_hostmask()

    @staticmethod
    def ipaddress_is_link_local(addr, version=None, flags=0):
        return netaddr.IPAddress(addr, version, flags).is_link_local()

    @staticmethod
    def ipaddress_is_loopback(addr, version=None, flags=0):
        return netaddr.IPAddress(addr, version, flags).is_loopback()

    @staticmethod
    def ipaddress_is_multicast(addr, version=None, flags=0):
        return netaddr.IPAddress(addr, version, flags).is_multicast()

    @staticmethod
    def ipaddress_is_netmask(addr, version=None, flags=0):
        return netaddr.IPAddress(addr, version, flags).is_netmask()

    @staticmethod
    def ipaddress_is_private(addr, version=None, flags=0):
        return netaddr.IPAddress(addr, version, flags).is_private()

    @staticmethod
    def ipaddress_is_reserved(addr, version=None, flags=0):
        return netaddr.IPAddress(addr, version, flags).is_reserved()

    @staticmethod
    def ipaddress_is_unicast(addr, version=None, flags=0):
        return netaddr.IPAddress(addr, version, flags).is_unicast()

    @staticmethod
    def ipaddress_reverse_dns(addr, version=None, flags=0):
        return netaddr.IPAddress(addr, version, flags).reverse_dns

    @staticmethod
    def ipaddress_version(addr, version=None, flags=0):
        return netaddr.IPAddress(addr, version, flags).version

    @staticmethod
    def ipaddress_words(addr, version=None, flags=0):
        return netaddr.IPAddress(addr, version, flags).words

    @staticmethod
    def ipaddress_add(addr, amount, version=None, flags=0):
        return netaddr.IPAddress(addr, version, flags) + amount

    @staticmethod
    def ipaddress_is_valid_ipv4(addr):
        return netaddr.valid_ipv4(addr)

    @staticmethod
    def ipaddress_is_valid_ipv6(addr):
        return netaddr.valid_ipv6(addr)

    @staticmethod
    def ipaddress_in_network(addr, cidr):
        return netaddr.IPAddress(addr) in netaddr.IPNetwork(cidr)

    # netaddr.EUI class
    @staticmethod
    def eui_bin(addr, version=None):
        return netaddr.EUI(addr, version).bin

    @staticmethod
    def eui_bits(addr, version=None):
        return netaddr.EUI(addr, version).bits()

    @staticmethod
    def eui_ei(addr, version=None):
        return netaddr.EUI(addr, version).ei

    @staticmethod
    def eui_eui64(addr, version=None):
        return netaddr.EUI(addr, version).eui64()

    @staticmethod
    def eui_iab(addr, version=None):
        return netaddr.EUI(addr, version).iab

    @staticmethod
    def eui_info(addr, version=None):
        return netaddr.EUI(addr, version).info

    @staticmethod
    def eui_ipv6(addr, prefix, version=None):
        return netaddr.EUI(addr, version).ipv6(prefix)

    @staticmethod
    def eui_ipv6_link_local(addr, version=None):
        return netaddr.EUI(addr, version).ipv6_link_local()

    @staticmethod
    def eui_is_iab(addr, version=None):
        return netaddr.EUI(addr, version).is_iab()

    @staticmethod
    def eui_modified_eui64(addr, version=None):
        return netaddr.EUI(addr, version).modified_eui64()

    @staticmethod
    def eui_oui(addr, version=None):
        return netaddr.EUI(addr, version).oui

    @staticmethod
    def eui_packed(addr, version=None):
        return netaddr.EUI(addr, version).packed

    @staticmethod
    def eui_value(addr, version=None):
        return netaddr.EUI(addr, version).value

    @staticmethod
    def eui_version(addr, version=None):
        return netaddr.EUI(addr, version).version

    @staticmethod
    def eui_words(addr, version=None):
        return netaddr.EUI(addr, version).words

    @staticmethod
    def eui_is_valid(addr):
        return netaddr.valid_mac(addr)
