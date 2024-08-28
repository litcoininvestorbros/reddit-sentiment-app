"""
"""
import dotenv


def load_env_variables() -> dict:
    """Load and return environment variables
     as a dictionary.
    """
    env = dotenv.dotenv_values('.env')
    return env