# CEE Event Standard Field Mixins and Tag Names
#
# The following attributes can be mixed into the CEE Event, either by setting
# the field individually or by using a mixin function to apply the selected mixins
# with a selected object or class.   If a mixin function is used, please add the
# name of the field attribute group to the object's "mixed_in" or "groups" list.
#
# NOTE: Any mixed in attributes will be included in the serialized event, including those
# with a null value, so don't mixin an attribute group unless it's needed.  Feel free to
# include invidual fields at will.
#

# CEE Field Groups (Attributes)

# Field groups can be selected for a new CEE Event Object.  They are python tuple lists. 
# The first tuple entry is the field name, the second tuple element is the CEE field type.
# The field types are as folllows:
# (The types suffixed by an ASCII vertical bar indicate a string-encoded type)
# "s|", string
# "b|", binary
# "g|", tag
# "i", integer  # never explicitly indicated when serialized
# "f", float    #
# "1", boolean  #
# "t|", ISO 8601 time stamp
# "d|", duration
# "4|", IPV4 address
# "6|", IPV6 address
# "m|", MAC Address

# Except for the core fields, The field groups are not defined within the CEE standard,
# but are defined here to more convienently construct a new CEE event object.

# Core Fields (Required)
# (these are mandatory fields that must appear in the following order)

ceeCore = [ ("id","s|"),		# event id assigned by location, ie: <refstd>_<event type> "org_warn"
    ("time","t|"),
    ("action","g|"),	        # action tag, indicates what action was being performed
    ("status","g|"),	        # status tag, "success", "failure", "error", "ongoing", "cancel", "unknown"
    ("p_sys_id","s|"),	        # IP address or hostname of originating system
    ("p_prod_id","s|")	        # producer ID.  consistent within logging system, ie: <app>_<event id>
]

# CEE augmentation core attributes (only used for augmenting forwarded events)
ceeAugmented = [
    ("time","t|"),		        # ISO 8601-1988 standard timestamp is time of event
    ("p_sys_id","s|"),	        # IP address or hostname of originating system
    ("p_prod_id","s|") 	        # producer ID.  consistent across logging system, ie: <app>_<event id>
]

# additional attributes and tags that appear in event descriptors following the core attributes

# CEE base attributes: useful, but not required
ceeBase = [ ("host","s|"), ("name","s|"), ("sev","i"), ("text","s|"), ("tags","s|") ]
ceeNet = [ ("ip","s|"), ("ipv4","4|"), ("ipv6","6|"), ("fqdn","s|"), ("mac","m|") ]
ceeTime = [ ("dur","d|"), ("endtime","t|"), ("eventtime","t|"), ("prodtime","t|"), ("recvtime","t|") ]
ceeMeta = [ ("confidence","s|"), ("count","i"), ("msgid","s|"), ("pri","i") ]
ceeSys = [ ("cwd","s|"), ("os","s|") ]


# CEE domain-specific attribute sets (optional)

# Account Fields

acctBase = [ ("acct_grp","s|"), ("acct_name","s|")]
acctExtend = [ ("acct_effgrp","s|"), ("acct_effgrpid","s|"), ("acct_effid","s|"), ("acct_effname","s|"), ("acct_grp","s|"), ("acct_grpid","s|"), ("acct_id","s|")]
acctPrivs = [ ("acct_priv","s|"), ("acct_role","s|"), ("acct_type","s|")]
acctMeta = [ ("acct_audit","s|") ]
acctSub = [("sub_acct","s|"), ("sub_acctid","s|"), ("sub_acctype","s|")]

# Application Fields

appBase = [ ("app_name","s|"), ("app_ver","s|") ]
appExtend = [ ("app_vend","s|"), ("app_cpe","s|")]

# Configuration Fields

configBase = [ ("config_name","s|"), ("config_val","s|") ]
configChange = [ ("config_oldname","s|"), ("config_oldval","s|") ]

# Internetworking Fields

inetBase = [ ("src_ip","s|"), ("src_port","i"), ("src_name","s|"), ("dst_ip","s|"), ("dst_port","i"), ("dst_name","s|") ]
inetExtend = [ ("src_ipv4","4|"), ("src_ipv6","6|"), ("src_mac","m|"), ("dst_ipv4","4|"), ("dst_ipv6","6|"), ("dst_mac","m|") ]
inetRange = [ ("src_ipv4cidr","s|"), ("dst_ipv6cidr","s|") ]
inetInterface = [ ("src_intf","s|"), ("dst_intf","s|") ]
inetNames = [ ("src_sysname","s|"), ("src_fqdn","s|"), ("src_domain","s|"), ("src_host","s|"),
              ("dst_sysname","s|"), ("dst_fqdn","s|"), ("dst_domain","s|"), ("dst_host","s|")]
inetNamesNT = [ ("src_ntdomain","s|"), ("dst_ntdomain","s|")]
inetGeo = [ ("src_country","s|"), ("src_ctrycode","s|"), ("src_geodms","s|"), ("src_loc","s|"), ("dst_country","s|"), ("dst_ctrycode","s|"), ("dst_geodms","s|"), ("dst_loc","s|")]
inetLayersBase = [ ("net_app","s|"), ("net_trans","s|") ]
inetLayersExt = [ ("net_pres","s|"), ("net_sess","s|") ]
inetTransfer = [ ("src_brecv","i"), ("src_bsent","i"), ("dst_brecv","i"), ("dst_bsent","s|")]
inetMisc = [ ("src_id","s|"), ("dst_id","s|") ]

# Email Fields

emailBase = [ ("email_from","s|"), ("email_to","s|"), ("email_subject","s|") ]

# File Fields

fileBase = [ ("file_name","s|"), ("file_size","i")]
filePath = [ ("file_path","s|"), ("file_devid","s|"), ("file_uri","s|")]
fileAccess = [ ("file_owner","s|"), ("file_grp","s|"), ("file_mode","s|"), ("file_perm","s|")]
fileTime = [ ("file_ctime","t|"), ("file_atime","t|"), ("file_mtime","s|") ]
fileID = [ ("file_inode","s|"), ("file_hash","b|"), ("file_hashalg","s|") ]
fileOldBase = [ ("file_oldname","s|"), ("file_oldsize","s|")]
fileOldPath = [ ("file_oldpath","s|"), ("file_olduri","s|") ]
fileOldTime = [ ("file_oldctime","s|"), ("file_oldmtime","s|")]
fileOldAccess = [ ("file_oldperm","s|")  ]
fileOldID = [ ("file_oldhash","s|") ]
fileMeta = [ ("file_sysid","s|") ]

# Firewall Fields

firewallBase = [ ("fw_rule","s|"), ("fw_ruleid","s|") ]
firewallChange = [ ("fw_oldrule","s|"), ("fw_oldruleid","s|") ]

# Disk Fields

diskBase = [ ("inode_devid","s|"), ("inode_id","s|"), ("inode_links","i") ]
diskUser = [ ("inode_aid","s|"), ("inode_gid","s|") ]

# Product Fields

prodBase = [ ("prod_id","s|"), ("prod_name","s|") ]
prodNet = [ ("prod_ip","s|"), ("prod_domain","s|") ]
prodExt = [ ("prod_ipv4","4|"), ("prod_ipv6","6|"), ("prod_fqdn","s|"), ("prod_mac","m|")]
prodGeo = [ ("prod_country","s|"), ("prod_ctrycode","s|"), ("prod_geodms","s|"), ("prod_loc","s|")  ]
prodOS = [ ("prod_proc","s|"), ("prod_procid","s|") ]
prodNT = [ ("prod_ntdomain","s|") ]
prodMeta = [ ("prod_cpe","s|") ]

# Target Fields

tgtBase = [ ("tgt_acct","s|"), ("tgt_acctid","s|")  ]
tgtPrivs =  [ ("tgt_acctpriv","s|"), ("tgt_acctgrp","s|"), ("tgt_acctgrpid","s|") ]
tgtApp = [ ("tgt_app","s|"), ("tgt_appcpe","s|") ]

# Vulnerability Fields

vulnBase = [ ("vuln_name","s|"), ("vuln_cve","s|") ]

# Web Fields

webClientBase = [ ("web_client","s|"), ("web_clienttype","s|") ]
webClientStatus = [ ("web_constatus","s|"), ("web_procdur","d|") ]
webClientMeta =  [ ("web_clientcpe","s|") ]
webConnectBase = [ ("http_url","s|"), ("http_method","s|"), ("http_rsp","s|") ]
webConnectData = [ ("http_query","s|"), ("http_1line","s|"), ("http_ref","s|") ]
webConnectStatus = [ ("http_contype","s|"), ("http_keepalive","i"), ("http_useragent","s|") ]

# Wifi Fields

wifiBase = [ ("wifi_chan","i"), ("wifi_proto","s|") ]
wifiExtend = [ ("wifi_enc","s|"), ("wifi_mod","s|") ]

# Windows Fields

winBase = [ ("prod_ntdomain","s|") ]
winRegistry = [ ("reg_hive","s|"), ("reg_key","s|"), ("reg_name","s|"), ("reg_val","s|"), ("reg_type","s|") ]
winObjBase = [ ("winobj_name","s|"), ("winobj_type","s|") ]
winObjFile = [ ("winobj_dir","s|"), ("winobj_handle","s|"), ("winobj_handlecnt","s|") ]
winObjStat = [ ("winobj_refcnt","s|"), ("winobj_charges","s|"), ("winobj_secdsc","s|") ]

# Tag Values
# NOTE: The 'action' and 'status' tag values are mandatory and are discussed
# at the beginning of this document.  They are encoded independently of field designators.
# Any other user-specified tags can be included in a comma-separated list value in a 
# field called "tags".

actionTags = [
'access',
'alert',
'allocate',
'allow',
'audit',
'backup',
'bind',
'block',
'clean',
'close',
'compress',
'connect',
'copy',
'create',
'decode',
'decompress',
'decrypt',
'depress',
'detect',
'disconnect',
'download',
'encode',
'encrypt',
'execute',
'filter',
'find',
'free',
'get',
'initialize',
'initiate',
'install',
'lock',
'login',
'logout',
'modify',
'move',
'open',
'read',
'release',
'remove',
'replicate',
'resume',
'save',
'scan',
'search',
'start',
'stop',
'suspend',
'uninstall',
'unlock',
'update',
'upgrade',
'upload',
'violate' ]

statusTags = [
'write',
'cancel',
'error',
'failure',
'ongoing',
'success',
'unknown'
]

