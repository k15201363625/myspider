'''
class UserInfo(object):
    id = ""
    username = ""
    screenName = ""
    createdAt = ""
    updatedAt = ""
    isVerified = False
    verifyMessage = ""
    briefIntro = ""
    profileImageUrl = ""
    statsCount = {}
        # "topicSubscribed"
        # "topicCreated"
        # "followedCount"
        # "followingCount"
        # "highlightedPersonalUpdates"
        # "liked"

    bio = ""
    gender = ""
    city = ""
    country = ""
    province = ""

if __name__ == '__main__':
    userinfo = UserInfo()
    print(dir(userinfo))
'''

userinfo = {
    "id":"",
    "username":"",
    "screenName":"",
    "createdAt":"",
    "updatedAt":"",
    "isVerified":False,
    "verifyMessage":"",
    "briefIntro":"",
    "profileImageUrl":"",
    "statsCount":{},
        # "topicSubscribed"
        # "topicCreated"
        # "followedCount"
        # "followingCount"
        # "highlightedPersonalUpdates"
        # "liked"

    "bio":"",
    "gender":"",
    "city":"",
    "country":"",
    "province":"",
}
if __name__ == '__main__':
    print(userinfo.keys())