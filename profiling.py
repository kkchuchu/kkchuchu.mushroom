import datetime


def log(message):
    print message

def in_out_log(log_method, message_format, message_parameters):

    def log_in_out_decorator(func):

        def wrapper(*args, **kwargs):
            target_name = func.func_name
            parameters = {
                keyword: kwargs[variable]
                for keyword, variable in message_parameters.items()
                if variable in kwargs
            }
            custom_message = message_format.format(**parameters)
            
            enter_time = datetime.datetime.now()
            enter_message = "Enter:[{target_name}][{enter_time}]".format(
                target_name=target_name, 
                enter_time=str(enter_time),
            )
            log_method(enter_message  + custom_message)
            result = func(*args, **kwargs)
            exit_time = datetime.datetime.now()
            exit_message = "Exit:[{target_name}][{exit_time}]".format(
                target_name=target_name,
                exit_time = str(exit_time),
            )
            log_method(exit_message + custom_message)
            return result

        return wrapper

    return log_in_out_decorator


@in_out_log(log, "Concatrate to a list with args b:{result}", {'result':'b'}) 
def target_function(*args, **kwargs):
    result = list(args) + [number for key, number in kwargs.items()]
    return result

print "Before start decorator function"
print target_function(4, 5, 6, a=1, b=2, c=3)
