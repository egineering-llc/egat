class TestResult():
    class_ = None
    func = None
    environment = None
    configuration = None
    thread = None
    status = None
    selenium_webdriver = None
    exception = None
    traceback = None

    def __init__(self, class_instance, func, thread=None, status=None, 
                 exception=None, traceback=None):
        self.class_ = class_instance.__class__
        self.func = func
        self.environment = getattr(class_instance, 'environment', {})
        self.configuration = getattr(class_instance, 'configuration', {})
        self.selenium_webdriver = getattr(class_instance, 'browser', {})
        self.thread = thread
        self.status = status
        self.exception = exception
        self.traceback = traceback

    def full_class_name(self):
        """Takes a class instance and a function from that class and returns the fully 
        qualified class name as a string."""
        return "%s.%s" % (self.func.__module__, self.class_.__name__)

    def environment_string(self):
        """Returns a string representing this TestResult's environment."""
        return ", ".join(map(str, self.environment.values()))
