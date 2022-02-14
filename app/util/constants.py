from config import settings


class BColors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

    def print_colors(this):
        print(
            f"""
        {this.HEADER}HEADER = '\033[95m'{this.ENDC}
        {this.OKBLUE}OKBLUE = '\033[94m'{this.ENDC}
        {this.OKCYAN}OKCYAN = '\033[96m'{this.ENDC}
        {this.OKGREEN}OKGREEN = '\033[92m'{this.ENDC}
        {this.WARNING}WARNING = '\033[93m'{this.ENDC}
        {this.FAIL}FAIL = '\033[91m'{this.ENDC}
        {this.ENDC}ENDC = '\033[0m'{this.ENDC}
        {this.BOLD}BOLD = '\033[1m'{this.ENDC}
        {this.UNDERLINE}UNDERLINE = '\033[4m'{this.ENDC}
        """
        )


SECRET_KEY = settings.fastapi_secret_key
ALGORITHM = settings.fastapi_access_token_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.fastapi_access_token_ttl
