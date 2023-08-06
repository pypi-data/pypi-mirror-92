from .base import *


@dataclass
class ApikeyElement:
    """Represents an attribute for any authorization method provided by Postman. For example
    `username` and `password` are set as auth attributes for Basic Authentication method.
    """
    key: str
    value: Any
    type: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ApikeyElement':
        assert isinstance(obj, dict)
        key = from_str(obj.get("key"))
        value = obj.get("value")
        type = from_union([from_str, from_none], obj.get("type"))
        return ApikeyElement(key, value, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["key"] = from_str(self.key)
        result["value"] = self.value
        result["type"] = from_union([from_str, from_none], self.type)
        return {k:result[k] for k in result if k in self.get_changed_keys()}


class AuthType(Enum):
    APIKEY = "apikey"
    AWSV4 = "awsv4"
    BASIC = "basic"
    BEARER = "bearer"
    DIGEST = "digest"
    HAWK = "hawk"
    NOAUTH = "noauth"
    NTLM = "ntlm"
    OAUTH1 = "oauth1"
    OAUTH2 = "oauth2"


@dataclass
class Auth(DataClassMixin):
    """Represents authentication helpers provided by Postman"""
    noauth: Any
    type: AuthType
    """The attributes for API Key Authentication."""
    apikey: Optional[List[ApikeyElement]] = None
    """The attributes for [AWS
    Auth](http://docs.aws.amazon.com/AmazonS3/latest/dev/RESTAuthentication.html).
    """
    awsv4: Optional[List[ApikeyElement]] = None
    """The attributes for [Basic
    Authentication](https://en.wikipedia.org/wiki/Basic_access_authentication).
    """
    basic: Optional[List[ApikeyElement]] = None
    """The helper attributes for [Bearer Token
    Authentication](https://tools.ietf.org/html/rfc6750)
    """
    bearer: Optional[List[ApikeyElement]] = None
    """The attributes for [Digest
    Authentication](https://en.wikipedia.org/wiki/Digest_access_authentication).
    """
    digest: Optional[List[ApikeyElement]] = None
    """The attributes for [Hawk Authentication](https://github.com/hueniverse/hawk)"""
    hawk: Optional[List[ApikeyElement]] = None
    """The attributes for [NTLM
    Authentication](https://msdn.microsoft.com/en-us/library/cc237488.aspx)
    """
    ntlm: Optional[List[ApikeyElement]] = None
    """The attributes for [OAuth2](https://oauth.net/1/)"""
    oauth1: Optional[List[ApikeyElement]] = None
    """Helper attributes for [OAuth2](https://oauth.net/2/)"""
    oauth2: Optional[List[ApikeyElement]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Auth':
        assert isinstance(obj, dict)
        noauth = obj.get("noauth")
        type = AuthType(obj.get("type"))
        apikey = from_union([lambda x: from_list(ApikeyElement.from_dict, x), from_none], obj.get("apikey"))
        awsv4 = from_union([lambda x: from_list(ApikeyElement.from_dict, x), from_none], obj.get("awsv4"))
        basic = from_union([lambda x: from_list(ApikeyElement.from_dict, x), from_none], obj.get("basic"))
        bearer = from_union([lambda x: from_list(ApikeyElement.from_dict, x), from_none], obj.get("bearer"))
        digest = from_union([lambda x: from_list(ApikeyElement.from_dict, x), from_none], obj.get("digest"))
        hawk = from_union([lambda x: from_list(ApikeyElement.from_dict, x), from_none], obj.get("hawk"))
        ntlm = from_union([lambda x: from_list(ApikeyElement.from_dict, x), from_none], obj.get("ntlm"))
        oauth1 = from_union([lambda x: from_list(ApikeyElement.from_dict, x), from_none], obj.get("oauth1"))
        oauth2 = from_union([lambda x: from_list(ApikeyElement.from_dict, x), from_none], obj.get("oauth2"))
        return Auth(noauth, type, apikey, awsv4, basic, bearer, digest, hawk, ntlm, oauth1, oauth2)

    def to_dict(self) -> dict:
        result: dict = {}
        result["noauth"] = self.noauth
        result["type"] = to_enum(AuthType, self.type)
        result["apikey"] = from_union([lambda x: from_list(lambda x: to_class(ApikeyElement, x), x), from_none],
                                      self.apikey)
        result["awsv4"] = from_union([lambda x: from_list(lambda x: to_class(ApikeyElement, x), x), from_none],
                                     self.awsv4)
        result["basic"] = from_union([lambda x: from_list(lambda x: to_class(ApikeyElement, x), x), from_none],
                                     self.basic)
        result["bearer"] = from_union([lambda x: from_list(lambda x: to_class(ApikeyElement, x), x), from_none],
                                      self.bearer)
        result["digest"] = from_union([lambda x: from_list(lambda x: to_class(ApikeyElement, x), x), from_none],
                                      self.digest)
        result["hawk"] = from_union([lambda x: from_list(lambda x: to_class(ApikeyElement, x), x), from_none],
                                    self.hawk)
        result["ntlm"] = from_union([lambda x: from_list(lambda x: to_class(ApikeyElement, x), x), from_none],
                                    self.ntlm)
        result["oauth1"] = from_union([lambda x: from_list(lambda x: to_class(ApikeyElement, x), x), from_none],
                                      self.oauth1)
        result["oauth2"] = from_union([lambda x: from_list(lambda x: to_class(ApikeyElement, x), x), from_none],
                                      self.oauth2)
        return {k:result[k] for k in result if k in self.get_changed_keys()}


@dataclass
class PathClass(DataClassMixin):
    type: Optional[str] = None
    value: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'PathClass':
        assert isinstance(obj, dict)
        type = from_union([from_str, from_none], obj.get("type"))
        value = from_union([from_str, from_none], obj.get("value"))
        return PathClass(type, value)

    def to_dict(self) -> dict:
        result: dict = {}
        result["type"] = from_union([from_str, from_none], self.type)
        result["value"] = from_union([from_str, from_none], self.value)
        return {k:result[k] for k in result if k in self.get_changed_keys()}


@dataclass
class Description(DataClassMixin):
    """Description can have versions associated with it, which should be put in this property."""
    version: Any
    """The content of the description goes here, as a raw string."""
    content: Optional[str] = None
    """Holds the mime type of the raw description content. E.g: 'text/markdown' or 'text/html'.
    The type is used to correctly render the description when generating documentation, or in
    the Postman app.
    """
    type: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Description':
        assert isinstance(obj, dict)
        version = obj.get("version")
        content = from_union([from_str, from_none], obj.get("content"))
        type = from_union([from_str, from_none], obj.get("type"))
        return Description(version, content, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["version"] = self.version
        result["content"] = from_union([from_str, from_none], self.content)
        result["type"] = from_union([from_str, from_none], self.type)
        return {k:result[k] for k in result if k in self.get_changed_keys()}


@dataclass
class QueryParam(DataClassMixin):
    description: Union[Description, None, str] = None
    """If set to true, the current query parameter will not be sent with the request."""
    disabled: Optional[bool] = None
    key: Optional[str] = None
    value: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'QueryParam':
        assert isinstance(obj, dict)
        description = from_union([Description.from_dict, from_none, from_str], obj.get("description"))
        disabled = from_union([from_bool, from_none], obj.get("disabled"))
        key = from_union([from_none, from_str], obj.get("key"))
        value = from_union([from_none, from_str], obj.get("value"))
        return QueryParam(description, disabled, key, value)

    def to_dict(self) -> dict:
        result: dict = {}
        result["description"] = from_union([lambda x: to_class(Description, x), from_none, from_str], self.description)
        result["disabled"] = from_union([from_bool, from_none], self.disabled)
        result["key"] = from_union([from_none, from_str], self.key)
        result["value"] = from_union([from_none, from_str], self.value)
        return {k:result[k] for k in result if k in self.get_changed_keys()}


class VariableType(Enum):
    """A variable may have multiple types. This field specifies the type of the variable."""
    ANY = "any"
    BOOLEAN = "boolean"
    NUMBER = "number"
    STRING = "string"


@dataclass
class Variable(DataClassMixin):
    """Collection variables allow you to define a set of variables, that are a *part of the
    collection*, as opposed to environments, which are separate entities.
    *Note: Collection variables must not contain any sensitive information.*

    Using variables in your Postman requests eliminates the need to duplicate requests, which
    can save a lot of time. Variables can be defined, and referenced to from any part of a
    request.
    """
    description: Union[Description, None, str] = None
    """The value that a variable holds in this collection. Ultimately, the variables will be
    replaced by this value, when say running a set of requests from a collection
    """
    value: Any = None
    disabled: Optional[bool] = None
    """A variable ID is a unique user-defined value that identifies the variable within a
    collection. In traditional terms, this would be a variable name.
    """
    id: Optional[str] = None
    """A variable key is a human friendly value that identifies the variable within a
    collection. In traditional terms, this would be a variable name.
    """
    key: Optional[str] = None
    """Variable name"""
    name: Optional[str] = None
    """When set to true, indicates that this variable has been set by Postman"""
    system: Optional[bool] = None
    """A variable may have multiple types. This field specifies the type of the variable."""
    type: Optional[VariableType] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Variable':
        assert isinstance(obj, dict)
        description = from_union([Description.from_dict, from_none, from_str], obj.get("description"))
        value = obj.get("value")
        disabled = from_union([from_bool, from_none], obj.get("disabled"))
        id = from_union([from_str, from_none], obj.get("id"))
        key = from_union([from_str, from_none], obj.get("key"))
        name = from_union([from_str, from_none], obj.get("name"))
        system = from_union([from_bool, from_none], obj.get("system"))
        type = from_union([VariableType, from_none], obj.get("type"))
        return Variable(description, value, disabled, id, key, name, system, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["description"] = from_union([lambda x: to_class(Description, x), from_none, from_str], self.description)
        result["value"] = self.value
        result["disabled"] = from_union([from_bool, from_none], self.disabled)
        result["id"] = from_union([from_str, from_none], self.id)
        result["key"] = from_union([from_str, from_none], self.key)
        result["name"] = from_union([from_str, from_none], self.name)
        result["system"] = from_union([from_bool, from_none], self.system)
        result["type"] = from_union([lambda x: to_enum(VariableType, x), from_none], self.type)
        return {k:result[k] for k in result if k in self.get_changed_keys()}


@dataclass
class URLClass(DataClassMixin):
    """The host for the URL, E.g: api.yourdomain.com. Can be stored as a string or as an array
    of strings.
    """
    host: Union[List[str], None, str]
    path: Union[List[Union[PathClass, str]], None, str]
    """Contains the URL fragment (if any). Usually this is not transmitted over the network, but
    it could be useful to store this in some cases.
    """
    hash: Optional[str] = None
    """The port number present in this URL. An empty value implies 80/443 depending on whether
    the protocol field contains http/https.
    """
    port: Optional[str] = None
    """The protocol associated with the request, E.g: 'http'"""
    protocol: Optional[str] = None
    """An array of QueryParams, which is basically the query string part of the URL, parsed into
    separate variables
    """
    query: Optional[List[QueryParam]] = None
    """The string representation of the request URL, including the protocol, host, path, hash,
    query parameter(s) and path variable(s).
    """
    raw: Optional[str] = None
    """Postman supports path variables with the syntax `/path/:variableName/to/somewhere`. These
    variables are stored in this field.
    """
    variable: Optional[List[Variable]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'URLClass':
        assert isinstance(obj, dict)
        host = from_union([lambda x: from_list(from_str, x), from_str, from_none], obj.get("host"))
        path = from_union(
            [lambda x: from_list(lambda x: from_union([PathClass.from_dict, from_str], x), x), from_str, from_none],
            obj.get("path"))
        hash = from_union([from_str, from_none], obj.get("hash"))
        port = from_union([from_str, from_none], obj.get("port"))
        protocol = from_union([from_str, from_none], obj.get("protocol"))
        query = from_union([lambda x: from_list(QueryParam.from_dict, x), from_none], obj.get("query"))
        raw = from_union([from_str, from_none], obj.get("raw"))
        variable = from_union([lambda x: from_list(Variable.from_dict, x), from_none], obj.get("variable"))
        return URLClass(host, path, hash, port, protocol, query, raw, variable)

    def to_dict(self) -> dict:
        result: dict = {}
        result["host"] = from_union([lambda x: from_list(from_str, x), from_str, from_none], self.host)
        result["path"] = from_union(
            [lambda x: from_list(lambda x: from_union([lambda x: to_class(PathClass, x), from_str], x), x), from_str,
             from_none], self.path)
        result["hash"] = from_union([from_str, from_none], self.hash)
        result["port"] = from_union([from_str, from_none], self.port)
        result["protocol"] = from_union([from_str, from_none], self.protocol)
        result["query"] = from_union([lambda x: from_list(lambda x: to_class(QueryParam, x), x), from_none], self.query)
        result["raw"] = from_union([from_str, from_none], self.raw)
        result["variable"] = from_union([lambda x: from_list(lambda x: to_class(Variable, x), x), from_none],
                                        self.variable)
        return {k: result[k] for k in result if k in self.get_changed_keys()}

    def get_params(self):
        res = {}
        if self.query:
            for i in self.query:
                if not i.disabled:
                    res[i.key] = i.value
        return res

    def get_easy_url(self):
        if type(self.host) is list and len(self.host) >= 1:
            host = self.host[0]
        else:
            host = self.host
        if type(self.path) is list and len(self.path) >= 1:
            path = '/'.join(self.path)
        elif type(self.path) is str:
            path = self.path
        else:
            path = ''
        return '%s://%s/%s' % (self.protocol or 'http', host, path)

    def get_url(self):
        url = self.raw or ((self.host or "") + '/' + (self.path or ""))
        if not url.startswith('http'):
            protocol = self.protocol or 'http'
            url = "%s://%s" % (protocol, url)
        return url


@dataclass
class Script(DataClassMixin):
    """A script is a snippet of Javascript code that can be used to to perform setup or teardown
    operations on a particular response.
    """
    exec: Union[List[str], None, str]
    src: Union[URLClass, None, str]
    """A unique, user defined identifier that can  be used to refer to this script from requests."""
    id: Optional[str] = None
    """Script name"""
    name: Optional[str] = None
    """Type of the script. E.g: 'text/javascript'"""
    type: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Script':
        assert isinstance(obj, dict)
        exec = from_union([lambda x: from_list(from_str, x), from_str, from_none], obj.get("exec"))
        src = from_union([URLClass.from_dict, from_str, from_none], obj.get("lib"))
        id = from_union([from_str, from_none], obj.get("id"))
        name = from_union([from_str, from_none], obj.get("name"))
        type = from_union([from_str, from_none], obj.get("type"))
        return Script(exec, src, id, name, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["exec"] = from_union([lambda x: from_list(from_str, x), from_str, from_none], self.exec)
        result["lib"] = from_union([lambda x: to_class(URLClass, x), from_str, from_none], self.src)
        result["id"] = from_union([from_str, from_none], self.id)
        result["name"] = from_union([from_str, from_none], self.name)
        result["type"] = from_union([from_str, from_none], self.type)
        return {k:result[k] for k in result if k in self.get_changed_keys()}


@dataclass
class Event(DataClassMixin):
    """Postman allows you to configure scripts to run when specific events occur. These scripts
    are stored here, and can be referenced in the collection by their ID.

    Defines a script associated with an associated event name
    """
    """Can be set to `test` or `prerequest` for test scripts or pre-request scripts respectively."""
    listen: str
    """Indicates whether the event is disabled. If absent, the event is assumed to be enabled."""
    disabled: Optional[bool] = None
    """A unique identifier for the enclosing event."""
    id: Optional[str] = None
    script: Optional[Script] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Event':
        assert isinstance(obj, dict)
        listen = from_str(obj.get("listen"))
        disabled = from_union([from_bool, from_none], obj.get("disabled"))
        id = from_union([from_str, from_none], obj.get("id"))
        script = from_union([Script.from_dict, from_none], obj.get("script"))
        return Event(listen, disabled, id, script)

    def to_dict(self) -> dict:
        result: dict = {}
        result["listen"] = from_str(self.listen)
        result["disabled"] = from_union([from_bool, from_none], self.disabled)
        result["id"] = from_union([from_str, from_none], self.id)
        result["script"] = from_union([lambda x: to_class(Script, x), from_none], self.script)
        return {k:result[k] for k in result if k in self.get_changed_keys()}


@dataclass
class CollectionVersionClass(DataClassMixin):
    """Increment this number if you make changes to the collection that changes its behaviour.
    E.g: Removing or adding new test scripts. (partly or completely).
    """
    major: int
    meta: Any
    """You should increment this number if you make changes that will not break anything that
    uses the collection. E.g: removing a folder.
    """
    minor: int
    """Ideally, minor changes to a collection should result in the increment of this number."""
    patch: int
    """A human friendly identifier to make sense of the version numbers. E.g: 'beta-3'"""
    identifier: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'CollectionVersionClass':
        assert isinstance(obj, dict)
        major = from_int(obj.get("major"))
        meta = obj.get("meta")
        minor = from_int(obj.get("minor"))
        patch = from_int(obj.get("patch"))
        identifier = from_union([from_str, from_none], obj.get("identifier"))
        return CollectionVersionClass(major, meta, minor, patch, identifier)

    def to_dict(self) -> dict:
        result: dict = {}
        result["major"] = from_int(self.major)
        result["meta"] = self.meta
        result["minor"] = from_int(self.minor)
        result["patch"] = from_int(self.patch)
        result["identifier"] = from_union([from_str, from_none], self.identifier)
        return {k:result[k] for k in result if k in self.get_changed_keys()}


@dataclass
class Information(DataClassMixin):
    """Detailed description of the info block"""
    description: Union[Description, None, str] = None
    """A collection's friendly name is defined by this field. You would want to set this field
    to a value that would allow you to easily identify this collection among a bunch of other
    collections, as such outlining its usage or content.
    """
    name: str = ""
    """This should ideally hold a link to the Postman schema that is used to validate this
    collection. E.g: https://schema.getpostman.com/collection/v1
    """
    schema: str = ""
    version: Union[CollectionVersionClass, None, str] = None
    """Every collection is identified by the unique value of this field. The value of this field
    is usually easiest to generate using a UID generator function. If you already have a
    collection, it is recommended that you maintain the same id since changing the id usually
    implies that is a different collection than it was originally.
    *Note: This field exists for compatibility reasons with Collection Format V1.*
    """
    postman_id: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Information':
        assert isinstance(obj, dict)
        description = from_union([Description.from_dict, from_none, from_str], obj.get("description"))
        name = from_str(obj.get("name"))
        schema = from_str(obj.get("schema"))
        version = from_union([CollectionVersionClass.from_dict, from_str, from_none], obj.get("version"))
        postman_id = from_union([from_str, from_none], obj.get("_postman_id"))
        return Information(description, name, schema, version, postman_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["description"] = from_union([lambda x: to_class(Description, x), from_none, from_str], self.description)
        result["name"] = from_str(self.name)
        result["schema"] = from_str(self.schema)
        result["version"] = from_union([lambda x: to_class(CollectionVersionClass, x), from_str, from_none],
                                       self.version)
        result["_postman_id"] = from_union([from_str, from_none], self.postman_id)
        return {k:result[k] for k in result if k in self.get_changed_keys()}


@dataclass
class File(DataClassMixin):
    content: Optional[str] = None
    src: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'File':
        assert isinstance(obj, dict)
        content = from_union([from_str, from_none], obj.get("content"))
        src = from_union([from_none, from_str], obj.get("lib"))
        return File(content, src)

    def to_dict(self) -> dict:
        result: dict = {}
        result["content"] = from_union([from_str, from_none], self.content)
        result["lib"] = from_union([from_none, from_str], self.src)
        return {k:result[k] for k in result if k in self.get_changed_keys()}


class FormParameterType(Enum):
    FILE = "file"
    TEXT = "text"


@dataclass
class FormParameter(DataClassMixin):
    description: Union[Description, None, str] = None
    key: str = None
    src: Union[List[Any], None, str] = None
    """Override Content-Type header of this form data entity."""
    content_type: Optional[str] = None
    """When set to true, prevents this form data entity from being sent."""
    disabled: Optional[bool] = None
    type: Optional[FormParameterType] = None
    value: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'FormParameter':
        assert isinstance(obj, dict)
        description = from_union([Description.from_dict, from_none, from_str], obj.get("description"))
        key = from_str(obj.get("key"))
        src = from_union([from_none, lambda x: from_list(lambda x: x, x), from_str], obj.get("lib"))
        content_type = from_union([from_str, from_none], obj.get("contentType"))
        disabled = from_union([from_bool, from_none], obj.get("disabled"))
        type = from_union([FormParameterType, from_none], obj.get("type"))
        value = from_union([from_str, from_none], obj.get("value"))
        return FormParameter(description, key, src, content_type, disabled, type, value)

    def to_dict(self) -> dict:
        result: dict = {}
        result["description"] = from_union([lambda x: to_class(Description, x), from_none, from_str], self.description)
        result["key"] = from_str(self.key)
        result["lib"] = from_union([from_none, lambda x: from_list(lambda x: x, x), from_str], self.src)
        result["contentType"] = from_union([from_str, from_none], self.content_type)
        result["disabled"] = from_union([from_bool, from_none], self.disabled)
        result["type"] = from_union([lambda x: to_enum(FormParameterType, x), from_none], self.type)
        result["value"] = from_union([from_str, from_none], self.value)
        return {k:result[k] for k in result if k in self.get_changed_keys()}


class Mode(Enum):
    """Postman stores the type of data associated with this request in this field."""
    FILE = "file"
    FORMDATA = "formdata"
    GRAPHQL = "graphql"
    RAW = "raw"
    URLENCODED = "urlencoded"


@dataclass
class URLEncodedParameter(DataClassMixin):
    description: Union[Description, None, str] = None
    key: str = ""
    disabled: Optional[bool] = None
    value: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'URLEncodedParameter':
        assert isinstance(obj, dict)
        description = from_union([Description.from_dict, from_none, from_str], obj.get("description"))
        key = from_str(obj.get("key"))
        disabled = from_union([from_bool, from_none], obj.get("disabled"))
        value = from_union([from_str, from_none], obj.get("value"))
        return URLEncodedParameter(description, key, disabled, value)

    def to_dict(self) -> dict:
        result: dict = {}
        result["description"] = from_union([lambda x: to_class(Description, x), from_none, from_str], self.description)
        result["key"] = from_str(self.key)
        result["disabled"] = from_union([from_bool, from_none], self.disabled)
        result["value"] = from_union([from_str, from_none], self.value)
        return {k:result[k] for k in result if k in self.get_changed_keys()}


@dataclass
class Body(DataClassMixin):
    """This field contains the data usually contained in the request body."""
    """When set to true, prevents request body from being sent."""
    disabled: Optional[bool] = None
    file: Optional[File] = None
    formdata: Optional[List[FormParameter]] = None
    graphql: Optional[Dict[str, Any]] = None
    """Postman stores the type of data associated with this request in this field."""
    mode: Optional[Mode] = None
    raw: Optional[str] = None
    urlencoded: Optional[List[URLEncodedParameter]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Body':
        assert isinstance(obj, dict)
        disabled = from_union([from_bool, from_none], obj.get("disabled"))
        file = from_union([File.from_dict, from_none], obj.get("file"))
        formdata = from_union([lambda x: from_list(FormParameter.from_dict, x), from_none], obj.get("formdata"))
        graphql = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("graphql"))
        mode = from_union([Mode, from_none], obj.get("mode"))
        raw = from_union([from_str, from_none], obj.get("raw"))
        urlencoded = from_union([lambda x: from_list(URLEncodedParameter.from_dict, x), from_none],
                                obj.get("urlencoded"))
        return Body(disabled, file, formdata, graphql, mode, raw, urlencoded)

    def to_dict(self) -> dict:
        result: dict = {}
        result["disabled"] = from_union([from_bool, from_none], self.disabled)
        result["file"] = from_union([lambda x: to_class(File, x), from_none], self.file)
        result["formdata"] = from_union([lambda x: from_list(lambda x: to_class(FormParameter, x), x), from_none],
                                        self.formdata)
        result["graphql"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.graphql)
        result["mode"] = from_union([lambda x: to_enum(Mode, x), from_none], self.mode)
        result["raw"] = from_union([from_str, from_none], self.raw)
        result["urlencoded"] = from_union(
            [lambda x: from_list(lambda x: to_class(URLEncodedParameter, x), x), from_none], self.urlencoded)
        return {k:result[k] for k in result if k in self.get_changed_keys()}


@dataclass
class CERT(DataClassMixin):
    """An object containing path to file certificate, on the file system"""
    """The path to file containing key for certificate, on the file system"""
    src: Any

    @staticmethod
    def from_dict(obj: Any) -> 'CERT':
        assert isinstance(obj, dict)
        src = obj.get("lib")
        return CERT(src)

    def to_dict(self) -> dict:
        result: dict = {}
        result["lib"] = self.src
        return {k:result[k] for k in result if k in self.get_changed_keys()}


@dataclass
class Key(DataClassMixin):
    """An object containing path to file containing private key, on the file system"""
    """The path to file containing key for certificate, on the file system"""
    src: Any

    @staticmethod
    def from_dict(obj: Any) -> 'Key':
        assert isinstance(obj, dict)
        src = obj.get("lib")
        return Key(src)

    def to_dict(self) -> dict:
        result: dict = {}
        result["lib"] = self.src
        return {k:result[k] for k in result if k in self.get_changed_keys()}


@dataclass
class Certificate(DataClassMixin):
    """A representation of an ssl certificate"""
    """An object containing path to file certificate, on the file system"""
    cert: Optional[CERT] = None
    """An object containing path to file containing private key, on the file system"""
    key: Optional[Key] = None
    """A list of Url match pattern strings, to identify Urls this certificate can be used for."""
    matches: Optional[List[Any]] = None
    """A name for the certificate for user reference"""
    name: Optional[str] = None
    """The passphrase for the certificate"""
    passphrase: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Certificate':
        assert isinstance(obj, dict)
        cert = from_union([CERT.from_dict, from_none], obj.get("cert"))
        key = from_union([Key.from_dict, from_none], obj.get("key"))
        matches = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("matches"))
        name = from_union([from_str, from_none], obj.get("name"))
        passphrase = from_union([from_str, from_none], obj.get("passphrase"))
        return Certificate(cert, key, matches, name, passphrase)

    def to_dict(self) -> dict:
        result: dict = {}
        result["cert"] = from_union([lambda x: to_class(CERT, x), from_none], self.cert)
        result["key"] = from_union([lambda x: to_class(Key, x), from_none], self.key)
        result["matches"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.matches)
        result["name"] = from_union([from_str, from_none], self.name)
        result["passphrase"] = from_union([from_str, from_none], self.passphrase)
        return {k:result[k] for k in result if k in self.get_changed_keys()}


@dataclass
class Header(DataClassMixin):
    """A representation for a list of headers

    Represents a single HTTP Header
    """
    description: Union[Description, None, str]
    """This holds the LHS of the HTTP Header, e.g ``Content-Type`` or ``X-Custom-Header``"""
    key: str
    """The value (or the RHS) of the Header is stored in this field."""
    value: str
    """If set to true, the current header will not be sent with requests."""
    disabled: Optional[bool] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Header':
        assert isinstance(obj, dict)
        description = from_union([Description.from_dict, from_none, from_str], obj.get("description"))
        key = from_str(obj.get("key"))
        value = from_str(obj.get("value"))
        disabled = from_union([from_bool, from_none], obj.get("disabled"))
        return Header(description, key, value, disabled)

    def to_dict(self) -> dict:
        result: dict = {}
        result["description"] = from_union([lambda x: to_class(Description, x), from_none, from_str], self.description)
        result["key"] = from_str(self.key)
        result["value"] = from_str(self.value)
        result["disabled"] = from_union([from_bool, from_none], self.disabled)
        return {k:result[k] for k in result if k in self.get_changed_keys()}


@dataclass
class ProxyConfig(DataClassMixin):
    """Using the Proxy, you can configure your custom proxy into the postman for particular url
    match
    """
    """When set to true, ignores this proxy configuration entity"""
    disabled: Optional[bool] = None
    """The proxy server host"""
    host: Optional[str] = None
    """The Url match for which the proxy config is defined"""
    match: Optional[str] = None
    """The proxy server port"""
    port: Optional[int] = None
    """The tunneling details for the proxy config"""
    tunnel: Optional[bool] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ProxyConfig':
        assert isinstance(obj, dict)
        disabled = from_union([from_bool, from_none], obj.get("disabled"))
        host = from_union([from_str, from_none], obj.get("host"))
        match = from_union([from_str, from_none], obj.get("match"))
        port = from_union([from_int, from_none], obj.get("port"))
        tunnel = from_union([from_bool, from_none], obj.get("tunnel"))
        return ProxyConfig(disabled, host, match, port, tunnel)

    def to_dict(self) -> dict:
        result: dict = {}
        result["disabled"] = from_union([from_bool, from_none], self.disabled)
        result["host"] = from_union([from_str, from_none], self.host)
        result["match"] = from_union([from_str, from_none], self.match)
        result["port"] = from_union([from_int, from_none], self.port)
        result["tunnel"] = from_union([from_bool, from_none], self.tunnel)
        return {k:result[k] for k in result if k in self.get_changed_keys()}


@dataclass
class Cookie(DataClassMixin):
    """A Cookie, that follows the [Google Chrome
    format](https://developer.chrome.com/extensions/cookies)
    """
    """The domain for which this cookie is valid."""
    domain: str
    """When the cookie expires."""
    expires: Union[float, None, str]
    """The path associated with the Cookie."""
    path: str
    """Custom attributes for a cookie go here, such as the [Priority
    Field](https://code.google.com/p/chromium/issues/detail?id=232693)
    """
    extensions: Optional[List[Any]] = None
    """True if the cookie is a host-only cookie. (i.e. a request's URL domain must exactly match
    the domain of the cookie).
    """
    host_only: Optional[bool] = None
    """Indicates if this cookie is HTTP Only. (if True, the cookie is inaccessible to
    client-side scripts)
    """
    http_only: Optional[bool] = None
    max_age: Optional[str] = None
    """This is the name of the Cookie."""
    name: Optional[str] = None
    """Indicates if the 'secure' flag is set on the Cookie, meaning that it is transmitted over
    secure connections only. (typically HTTPS)
    """
    secure: Optional[bool] = None
    """True if the cookie is a session cookie."""
    session: Optional[bool] = None
    """The value of the Cookie."""
    value: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Cookie':
        assert isinstance(obj, dict)
        domain = from_str(obj.get("domain"))
        expires = from_union([from_float, from_str, from_none], obj.get("expires"))
        path = from_str(obj.get("path"))
        extensions = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("extensions"))
        host_only = from_union([from_bool, from_none], obj.get("hostOnly"))
        http_only = from_union([from_bool, from_none], obj.get("httpOnly"))
        max_age = from_union([from_str, from_none], obj.get("maxAge"))
        name = from_union([from_str, from_none], obj.get("name"))
        secure = from_union([from_bool, from_none], obj.get("secure"))
        session = from_union([from_bool, from_none], obj.get("session"))
        value = from_union([from_str, from_none], obj.get("value"))
        return Cookie(domain, expires, path, extensions, host_only, http_only, max_age, name, secure, session, value)

    def to_dict(self) -> dict:
        result: dict = {}
        result["domain"] = from_str(self.domain)
        result["expires"] = from_union([to_float, from_str, from_none], self.expires)
        result["path"] = from_str(self.path)
        result["extensions"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.extensions)
        result["hostOnly"] = from_union([from_bool, from_none], self.host_only)
        result["httpOnly"] = from_union([from_bool, from_none], self.http_only)
        result["maxAge"] = from_union([from_str, from_none], self.max_age)
        result["name"] = from_union([from_str, from_none], self.name)
        result["secure"] = from_union([from_bool, from_none], self.secure)
        result["session"] = from_union([from_bool, from_none], self.session)
        result["value"] = from_union([from_str, from_none], self.value)
        return {k:result[k] for k in result if k in self.get_changed_keys()}
