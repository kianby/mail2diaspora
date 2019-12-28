# [DEPRECATED]

## Mail to Diaspora

Small piece of code providing a way to post text and image to Diaspora via
emails. It is part of my ecosystem built around RabbitMQ. It depends on
[SRMail](https://github.com/kianby/srmail) to send and receive e-mails. Other
dependencies are listed in **requirements.txt**. Mail2Diaspora is written in
Python 3.

*config.json* is a configuration example.


**Diaspy connection patch for Framasphere:**

    class Connection():
        """Object representing connection with the pod.
        """
        _token_regex = re.compile(r'name="csrf-token"\s+content="(.*?)"')
        _userinfo_regex = re.compile(r'window.current_user_attributes = ({.*})')
        # this is for older version of D*
        _token_regex_2 = re.compile(r'content="(.*?)"\s+name="csrf-token')
        _userinfo_regex_2 = re.compile(r'gon.user=({.*});gon.appConfig')
        _verify_SSL = True
