urls = [
    ('/auth/send_phone_verify_code',
     'handlers.auth.send_phone_verify_code.Handle'),
    ('/auth/check_phone_verify_code',
     'handlers.auth.check_phone_verify_code.Handle'),
    ('/auth/phone_connect', 'handlers.auth.phone_connect.Handle'),
    ('/auth/wechat_connect', 'handlers.auth.wechat_connect.Handle'),
    ('/auth/bind_phone', 'handlers.auth.bind_phone.Handle'),
    ('/auth/get_session_key', 'handlers.auth.get_session_key.Handle'),
    ('/meditation/get_meditation_info',
     'handlers.meditation.get_meditation_info.Handle'),
    ('/user/get_user_info', 'handlers.user.get_user_info.Handle'),
    ('/user/modify_user_info', 'handlers.user.modify_user_info.Handle'),
]
