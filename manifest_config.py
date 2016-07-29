# Config file for TMMS (The Machine Manifesting Server), neeed by Manifesting
# scripts setup_*, manifest_api.py, and tm_manifest.py.  The values in
# this file as delivered will almost certainly NOT work for you.  Copy
# this file and edit the copy as appropriate.  Then move the custom copy to
# 1) /etc/tmms, where it will be used by default by all the commands.  This
#    is the system default location expected by the systems service startup.
# 2) /some/where/else/mytmms.  All five commands listed above must be started
#    with "--config /some/where/else/mytmms".  This allows you to run
#    multiple TMMS environments on a single system although you must setup
#    and start them by hand.

# Values below control not only API and image aspects, but configuration
# for the PXE serving combination of DHCP and TFTP.

# Global topology config file for an instance of The Machine (giant JSON file)
TMCONFIG='/etc/tmconfig'

# IP address in this system on which the Manifest API listens
HOST = '0.0.0.0'    # 0.0.0.0 means all interfaces in the system
PORT = 31178        # listen on this port

# Top-level directory for TMMS infrastructure
MANIFESTING_ROOT = '/var/lib/tmms'

# The TFTP part of PXE booting has files that live under here.  TFTP is
# served by a dnsmasq instance configured by TMMS.
TFTP_ROOT = MANIFESTING_ROOT + '/tftp'

# L4TM repo information, needed to build file system images for nodes
L4TM_MIRROR = 'http://hlinux-deejay.us.rdlabs.hpecorp.net/l4tm'
L4TM_RELEASE = 'catapult'

# Remove 'main' for a much faster start (3 seconds vs 20), however you
# will be working with a partial repo.
L4TM_AREAS = ( 'contrib', 'non-free' )

# NIC connected to the node network on which DHCP and TFTP will be served
# (usually something like ethX)
PXE_INTERFACE = 'net_accessP'

# Domain name for nodes in this instance.  Forty nodes are configured,
# meaning TMMS must generate a list of 40 IP addresses.  Four formats
# exist for this variable:
# 1. Domain name only.  Example:
#    TMDOMAIN = 'have.it.your.way'
#    TMMS performs a DNS lookup on node01.<domain> through node40.<domain>
#    and configures DHCP appropriately.  The netmask is discerned from the
#    PXE_INTERFACE.  This is the "official" method but requires site IT
#    support to configure your DNS.  No DNS, no TMMS.
#
#    The remaining formats support static assignment (ie, DNS per format 1
#    is not available).  YOU are responsible for insuring these addresses
#    are legal in your environemnt.
#
# 2. Domain name,ipaddr.  Example:
#    TMDOMAIN = 'have.it.your.way,10.11.12.42'
#    TMMS will generate 40 IP addresses starting at the given address.
#    node01 is assigned the given IP address, node02 the next, etc.
#    A 24-bit network / 8-bit host netmask of 255.255.255.0 is assumed.
#
# 3. Domain name,ipaddr1-ipaddr2.  Example:
#    TMDOMAIN = 'have.it.your.way,10.11.12.42-10.11.12.100''
#    A minor variation on format 2.  It still assumes a 24-bit network.
#
# 4. Domain name,CIDR bits. Example:
#    TMDOMAIN = 'have.it.your.way,10.11.12.64/26'
#    Assign sequential addresses x.y.z.(base + 1), x.y.z.(base + 2)....
#    where "base" is the start of the CIDR subnet (in the example, 64).
#    The host part must be at least 6 bits (64 addresses) and the netmask
#    is directly calculated.

TMDOMAIN = 'have.it.your.way,10.11.10.0/24'
