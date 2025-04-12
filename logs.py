import logging

# Set up logging configuration
def setup_logger():
    logger = logging.getLogger('LeechBotLogger')
    logger.setLevel(logging.DEBUG)

    # Create file handler to store logs in a file
    file_handler = logging.FileHandler('leechbot_logs.log')
    file_handler.setLevel(logging.DEBUG)

    # Create console handler to also display logs on the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create a formatter and add it to both handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Create logger instance
logger = setup_logger()

# Example log messages
def log_example():
    logger.debug('This is a debug message')
    logger.info('This is an info message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')
    logger.critical('This is a critical message')

# Call the example function to test the logging
if __name__ == "__main__":
    log_example()
