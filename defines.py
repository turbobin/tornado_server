from tornado.options import define

# Defines an option in the global namespace.
define(name="port", type=int)
define(name="env", default="base", type=str)
define(name="appname", default="waterworld", type=str)
