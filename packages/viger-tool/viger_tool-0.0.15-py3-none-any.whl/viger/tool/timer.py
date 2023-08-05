#!/usr/bin/env python

# Timer
class Timer():
    """
    计算函数, 段落的执行时间
    ex:
        def example():
            Timer.start()
            time.sleep(1)
            Timer.end()

        @Timer.calc
        def example():
            time.sleep(1)
    """

    logger = ''
    start_time = 0
    end_time = 0

    def __init__(self):
        pass

    @classmethod
    def start(cls):
        cls.start_time = time.time()
        msg = 'Caculate time start'
        if cls.logger:
            extra = {
                'pathname': sys._getframe(1).f_code.co_filename,
                'lineno': sys._getframe(1).f_lineno,
            }
            cls.logger.info(msg, extra=extra)
        else:
            print(msg)

    @classmethod
    def end(cls):
        cls.end_time = time.time()
        msg = 'Caculate time end, Time: %0.2f sec'%(cls.end_time - cls.start_time)
        if cls.logger:
            extra = {
                'pathname': sys._getframe(1).f_code.co_filename,
                'lineno': sys._getframe(1).f_lineno,
            }
            cls.logger.info(msg, extra=extra)
        else:
            print(msg)

    @classmethod
    def calc(cls, func):
        def wrap(*args, **kwargs):
            start_time = time.time()
            rsp = func(*args, **kwargs)
            end_time = time.time()
            msg = 'Time: %0.2f sec'%(end_time - start_time)
            if cls.logger:
                cls.logger.info(msg)
            else:
                print(msg)
            return rsp
        return wrap

