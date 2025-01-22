"""
Centralized error handling system for LogoCraft.
Provides standardized error handling and logging functionality.
"""
from typing import Type, Callable
import logging
from functools import wraps

class ImageProcessingError(Exception):
    """Base exception for image processing related errors"""
    pass

class ConfigurationError(Exception):
    """Exception for configuration related errors"""
    pass

class ValidationError(Exception):
    """Exception for data validation errors"""
    pass

def handle_errors(logger: logging.Logger = None, error_type: Type[Exception] = ImageProcessingError) -> Callable:
    """
    Decorator for standardized error handling and logging.
    
    Args:
        logger: Logger instance to use. If None, creates a new logger.
        error_type: Type of exception to raise. Defaults to ImageProcessingError.
    
    Returns:
        Callable: Decorated function with error handling.
    """
    if logger is None:
        logger = logging.getLogger(__name__)
        
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_msg = f"Error in {func.__name__}: {str(e)}"
                logger.error(error_msg, exc_info=True)
                raise error_type(error_msg) from e
        return wrapper
    return decorator

def log_operation(logger: logging.Logger = None) -> Callable:
    """
    Decorator for logging function entry and exit.
    
    Args:
        logger: Logger instance to use. If None, creates a new logger.
    
    Returns:
        Callable: Decorated function with operation logging.
    """
    if logger is None:
        logger = logging.getLogger(__name__)
        
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.debug(f"Entering {func.__name__}")
            try:
                result = func(*args, **kwargs)
                logger.debug(f"Exiting {func.__name__}")
                return result
            except Exception as e:
                logger.error(f"Error in {func.__name__}: {str(e)}")
                raise
        return wrapper
    return decorator