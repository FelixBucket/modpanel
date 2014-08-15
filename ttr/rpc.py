from django.conf import settings
import pyjsonrpc

class RPC():

	def __init__(self, url=settings.RPC_ENDPOINT, username=settings.RPC_USERNAME, password=settings.RPC_PASSWORD):
		self.client = pyjsonrpc.HttpClient(url=url, username=username, password=password)


### SHARD MANAGEMENT ###
"""
@method: listShards: Returns an array of shards
@params: There are no parameters for this RPC call.

Example Response:
[
	{
		u'avg-frame-rate': 19.9051,
		u'districtId': 402000001,
		u'lastSeen': 1408140368,
		u'heap': {
			u'objects': 1126956,
			u'garbage': 319000
		},
		u'districtName': u'Autocorrect Acres',
		u'invasion': None,
		u'channel': 402000000,
		u'population': 0
	}
]
"""

"""
@method: closeDistrict: Closes a district
@params: districtId

Example Response: None
"""

### UBERDOG MANAGEMENT ###
"""
@method: setEnableLogins: Enable/disable all logins
@params: enable

Example Response: None
"""

### GENERAL INFORMATION ###
"""
@method: getGSIDByAccount: Gets the GSID for a given webserver account ID, or null if invalid.
@params: accountId

Example Response: None
"""

"""
@method: getAccountByGSID: Gets the account ID associated to a particular GSID, or null if invalid.
@params: gsId

Example Response: None
"""

"""
@method: getAccountByAvatarID: Gets the account ID associated to a particular avatar (account), or null if invalid.
@params: avId

Example Response: None
"""

"""
@method: : getAvatarsForGSID: Gets the set of avatars (Toons) that exist on a given gsId, or null if invalid.
@params: gsId

Example Response: None
"""

### NAME REVIEW ###
"""
@method: listPendingNames: Returns up to 50 pending names, sorted by time spent in the queue.
It is recommended that the name moderation app call this periodically
to update its database, in order to ensure that no names got lost.

@params: count (default is 50)

Example Response: None
"""

"""
@method: approveName: Approves the name of the specified avatar.
For security, the name must be submitted again.
On success, returns null.
On failure, comes back with a JSON error. The failure codes are:
-100: avId invalid
-101: avId not in the "pending name approval" state
-102: name does not match

@params: avId, name

Example Response: None
"""

"""
@method: rejectName: Rejects the name of the specified avatar.
If the avatar already has a valid name, this will reset them back to their default 'Color Species' name (i.e. this call will have the same effect as the ~badName magic word).
On success, returns null.
On failure, comes back with a JSON error:
-100: avId invalid

@params: avId

Example Response: None
"""

"""
@method: openName: Allows name changes by "opening up" the name of a specified avatar.
This causes the "Name your Toon!" button to appear on the PAT screen, allowing users to submit a different name.
On success, returns null.
On failure, comes back with a JSON error:
-100: avId invalid

@params: avId

Example Response: None
"""

"""
@method: changeName: Changes the name of a Toon.
This will also clear any name-approval status.
On success, returns null.
On failure, comes back with a JSON error:
-100: avId invalid

@params: avId, name

Example Response: None
"""

### ADMIN MESSAGES AND KICKS ###
"""
@method: kickChannel: Kicks any users whose CAs are subscribed to a particular channel.
This always returns null.

@params: channel, code, reason

Example Response: None
"""

"""
@method: kickGSID: Kicks a particular user, by GSID.
This always returns null.

@params: gsId, code, reason

Example Response: None
"""

"""
@method: kickAvatar: Kicks a particular user, by avId.
This always returns null.

@params: avId, code, reason

Example Response: None
"""

"""
@method: kickShard: Kicks all clients in a particular shard.
This always returns null.

@params: shardId, code, reason

Example Response: None
"""

"""
@method: kickAll: Kicks all clients.
This always returns null.

@params: code, reason

Example Response: None
"""

"""
@method: messageChannel: Messages any users whose CAs are subscribed to a particular channel.
'code' is the system-message code for localization.
'params' is an array of parameters used by that system message.

To send a raw message as-is, use code 0 and put the message as the only
item in the params array: (..., 0, ["Hello!"])

This always returns null.

@params: channel, code, params

Example Response: None
"""

"""
@method: messageGSID: Messages a particular user, by GSID.
'code' is the system-message code for localization.
'params' is an array of parameters used by that system message.

To send a raw message as-is, use code 0 and put the message as the only
item in the params array: (..., 0, ["Hello!"])

This always returns null.

@params: gsId, code, params

Example Response: None
"""

"""
@method: messageAvatar: Messages a particular user, by avId.
'code' is the system-message code for localization.
'params' is an array of parameters used by that system message.

To send a raw message as-is, use code 0 and put the message as the only
item in the params array: (..., 0, ["Hello!"])

This always returns null.

@params: avId, code, params

Example Response: None
"""

"""
@method: messageShard: Messages all clients in a particular shard.
'code' is the system-message code for localization.
'params' is an array of parameters used by that system message.

To send a raw message as-is, use code 0 and put the message as the only
item in the params array: (..., 0, ["Hello!"])

This always returns null.

@params: shardId, code, params

Example Response: None
"""

"""
@method: messageAll: Messages all clients.
'code' is the system-message code for localization.
'params' is an array of parameters used by that system message.

To send a raw message as-is, use code 0 and put the message as the only
item in the params array: (..., 0, ["Hello!"])

This always returns null.

@params: code, params

Example Response: None
"""
