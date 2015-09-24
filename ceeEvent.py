import ceeFields
import time, os
from datetime import datetime as dt
import json

# The CEE Event Class.  Usage pattern is 'myev = CEEEvent(id="<id>",time=<ISO datetime>,action,status)
# You then set any additional attributes.   This base class is meant to be expanded and the __str__
# method overriden for the specific CEE output format.

# NOTE: (1) This class should be mixed with CEE field attribute groups from ceeFields
#	(2) This class doesn't support augmentation fields yet
#	(3) This class was created for event generation, not parsing

# some support defs

class dotdict(dict):
    def __getattr__(self, attr):
        return self.get(attr, None)

    def dot_setitem(self,attr,val):
        dict.__setitem__(self.__dict__,attr,val)
        
    def dot_delitem(self,attr):
        dict.__delitem__(self.__dict__,attr)

    __setattr__= dot_setitem
    __delattr__= dot_delitem


# event initialization strings should be UTF-8, but ascii will be converted
        
class CEEEvent():
    # field name/value dictionary. accessible as: myev.field.<field name> =
    field = dotdict() 
    # type of the field name.  tuple like this: (<CEETypeIndicator string>, <isOptionalField bool>)
    ftype = {}
    # JSON / XML string encoders.  Initially not allocated
    jcoder = None
    xcoder = None
    def __init__(self, id=None, time=None, action=None, status=None, p_sys_id=None, p_prod_id=None, text=None, render='json', use_fields = []):
        # initialize core fields and mark them as non-optional
        for (name, typ) in ceeFields.ceeCore:
            self.field.__dict__[name] = None
            self.ftype[name] = (typ, False)
        
        # populate core fields, with None if necessary
        self.field.id = id
        self.field.time = time
        self.field.action = action
        self.field.status = status
        self.field.p_sys_id = p_sys_id
        self.field.p_prod_id = p_prod_id

        
        # "text" is not a core field, but so common that we will autopopulate if present
        if text:
            self.addField('text')   # will set type to string
            self.field.text = text
            
        # initialize optional fields and mark them as such
        for (name, typ) in use_fields:
            self.field.__dict__[name] = 0
            self.ftype[name] = (typ, True)
        
        # if time isn't already populated by default, mark it now
        if self.field.time is None: self.mark()
            
        # if p_sys_id isn't already populated, set it to the hostname
        if self.field.p_sys_id is None: self.field.p_sys_id = os.uname()[1]

        # set the default rendering syntax to json, with implied string types
        if render == 'xml':
	    self.useXML()
        else:
            self.useJSON()
    
    # add a field to the event (type defaults to string)
    # by default, the field is assumed to be optional
    def addField(self, name, typ = "s|"):
        self.field.__dict__[name] = None
        self.ftype[name] = (typ, True)

    # sets the time parameter to now, utc
    # append Z for explicit Zulu (UTC) time
    def mark(self):
        self.field.time = dt.isoformat(dt.utcnow()) + "Z"

    # Returns a Javascript string representation of CEE value
    # based on the CEE type.
    #
    #  1. if string type, will escape specials and surround with double quotes
    #  2. if non-string type, will simply return the value
    #  3. if assertTypes is true, string types are pre-pended with type
    #  4. if non-existant, returns an empty array
    #
    def jstring(self,s,t):
        if s:
            if len(t) == 2:
                if self.assertTypes: return self.jcoder.encode(t+s)
                else: return self.jcoder.encode(s)
            else:
                return s
        return '[]'

    # the python serialization of the object
    def __repr__(self):
        return self.field.__dict__.__repr__()

    # the json rendering of the object, type implied
    def __json_str__(self):
        jstring = self.jstring
        # serialize the core fields, jstring generates a javascript string or [] if its null
        json_out = '{"Event":{"id":%s,"time":%s,"action":%s,"status":%s,"p_sys_id":%s,"p_prod_id":%s' % ( jstring(self.field.id,"s|"), jstring(self.field.time,"t|"), jstring(self.field.action,"g|"), jstring(self.field.status,"g|"), jstring(self.field.p_sys_id,"s|"), jstring(self.field.p_prod_id,"s|") )
        # serialize the optional fields
        for (name, val) in self.field.__dict__.iteritems():
	    # is it optional?
            if self.ftype[name][1]:
                json_out += ',"%s":%s' % (name, jstring(val,self.ftype[name][0]))
        # close field array and event
        json_out += '}}'
        return json_out

    # the xml rendering of the object
    def __xml_str__(self):
        # serialize the core fields
        return '</not implemented>'

    # alters the default renderer, but logging appenders will generally either call the 
    # specific syntax renderer/serializer directly or simply let it default to __str__

    # alters default to render with CEE JSON Syntax
    def useJSON(self,typed=False):
        self.__str__ = self.__json_str__
	self.assertTypes = typed
	if not self.jcoder:
            self.jcoder = json.JSONEncoder(ensure_ascii=True)

    # alters default to render with CEE XML Syntax
    def useXML(self, typed=False):
        self.__str__ = self.__xml_str__
        self.assertTypes = typed
        #if not self.xcoder:
        #    self.xcoder = xml.XMLEncoder()


