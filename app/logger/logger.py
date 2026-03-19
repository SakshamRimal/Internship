# import logging
# import sys
#
# import logging
# import sys
#
#
# def get_logger(name):
#     logger = logging.getLogger(name)
#
#     # Only add handlers if they don't exist to avoid duplicate logs
#     if not logger.handlers:
#         logger.setLevel(logging.DEBUG)
#
#         # Define the format: Timestamp | Level | Module | Message
#         formatter = logging.Formatter(
#             '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
#         )
#
#         # Console Handler (Outputs to your terminal)
#         stdout_handler = logging.StreamHandler(sys.stdout)
#         stdout_handler.setFormatter(formatter)
#         logger.addHandler(stdout_handler)
#
#         # Optional: File Handler (Saves logs to a file)
#         # file_handler = logging.FileHandler('app.log')
#         # file_handler.setFormatter(formatter)
#         # logger.addHandler(file_handler)
#
#     return logger
#
#
