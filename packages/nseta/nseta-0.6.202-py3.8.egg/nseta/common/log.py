import logging
import os
# import sys
import warnings
# import pandas as pd

from functools import wraps
from inspect import getcallargs, getfullargspec
from collections import OrderedDict, Iterable
from itertools import *

__all__ = ['setup_custom_logger', 'default_logger', 'log_to', 'tracelog', 'suppress_stdout_stderr']
__trace__ = False
def setup_custom_logger(name, levelname=logging.DEBUG, trace=False, log_file_path='logs.log'):
	trace_formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(module)s - %(funcName)s - %(lineno)d\n%(message)s\n')
	console_info_formatter = logging.Formatter(fmt='%(levelname)s - %(filename)s(%(funcName)s - %(lineno)d)\n%(message)s\n')
	__trace__ = trace

	logger = logging.getLogger(name)
	logger.setLevel(levelname)

	consolehandler = logging.StreamHandler()
	consolehandler.setFormatter(console_info_formatter if levelname == logging.INFO else trace_formatter)
	consolehandler.setLevel(levelname)
	logger.addHandler(consolehandler)

	if levelname == logging.DEBUG:
		filehandler = logging.FileHandler(log_file_path)
		filehandler.setFormatter(trace_formatter)
		filehandler.setLevel(levelname)
		logger.addHandler(filehandler)
		logger.debug('Logging started')

	if trace:
		tracelogger = logging.getLogger('nseta_file_logger')
		tracelogger.setLevel(levelname)
		tracelogger.addHandler(consolehandler)
		tracelogger.addHandler(filehandler)
		logger.debug('Tracing started')
	# Turn off pystan warnings
	warnings.simplefilter("ignore", DeprecationWarning)
	warnings.simplefilter("ignore", FutureWarning)
	
	return logger

def default_logger():
	return logging.getLogger('nseta')

def file_logger():
	return logging.getLogger('nseta_file_logger')

def trace_log(line):
	if __trace__:
		default_logger().info(line)
	else:
		file_logger().info(line)

def flatten(l):
	"""Flatten a list (or other iterable) recursively"""
	for el in l:
		if isinstance(el, Iterable) and not isinstance(el, str):
			for sub in flatten(el):
				yield sub
		else:
			yield el

def getargnames(func):
	"""Return an iterator over all arg names, including nested arg names and varargs.
	Goes in the order of the functions argspec, with varargs and
	keyword args last if present."""
	(args, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, annotations) = getfullargspec(func)
	return chain(flatten(args), filter(None, [varargs, varkw]))

def getcallargs_ordered(func, *args, **kwargs):
	"""Return an OrderedDict of all arguments to a function.
	Items are ordered by the function's argspec."""
	argdict = getcallargs(func, *args, **kwargs)
	return OrderedDict((name, argdict[name]) for name in getargnames(func))

def describe_call(func, *args, **kwargs):
	yield "Calling %s with args:" % func.__name__
	for argname, argvalue in getcallargs_ordered(func, *args, **kwargs).items():
		yield "\t%s = %s" % (argname, repr(argvalue))

def log_to(logger_func):
	"""A decorator to log every call to function (function name and arg values).
	logger_func should be a function that accepts a string and logs it
	somewhere. The default is logging.debug.
	If logger_func is None, then the resulting decorator does nothing.
	This is much more efficient than providing a no-op logger
	function: @log_to(lambda x: None).
	"""
	if logger_func is not None:
		def decorator(func):
			@wraps(func)
			def wrapper(*args, **kwargs):
				description = ""
				for line in describe_call(func, *args, **kwargs):
					description = description + "\n" + line
				logger_func(description)
				return func(*args, **kwargs)
			return wrapper
	else:
		decorator = lambda x: x
	return decorator

tracelog = log_to(trace_log)

class suppress_stdout_stderr(object):
	'''
	A context manager for doing a "deep suppression" of stdout and stderr in
	Python, i.e. will suppress all print, even if the print originates in a
	compiled C/Fortran sub-function.
	   This will not suppress raised exceptions, since exceptions are printed
	to stderr just before a script exits, and after the context manager has
	exited (at least, I think that is why it lets exceptions through).

	'''
	def __init__(self):
		# Open a pair of null files
		self.null_fds = [os.open(os.devnull, os.O_RDWR) for x in range(2)]
		# Save the actual stdout (1) and stderr (2) file descriptors.
		self.save_fds = [os.dup(1), os.dup(2)]

	def __enter__(self):
		# Assign the null pointers to stdout and stderr.
		os.dup2(self.null_fds[0], 1)
		os.dup2(self.null_fds[1], 2)

	def __exit__(self, *_):
		# Re-assign the real stdout/stderr back to (1) and (2)
		os.dup2(self.save_fds[0], 1)
		os.dup2(self.save_fds[1], 2)
		# Close the null files
		for fd in self.null_fds + self.save_fds:
			os.close(fd)
