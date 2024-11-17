# utilities/env_switcher.py
import os
import shutil
import logging

logger = logging.getLogger(__name__)

class EnvironmentSwitcher:
    """Utility class to manage environment switching"""
    
    ENV_FILES = {
        'dev': '.env.dev',
        'qa': '.env',
        'prod': '.env.prod'
    }
    
    @classmethod
    def switch_env(cls, env):
        """
        Switch to the specified environment by copying the appropriate .env file
        
        Args:
            env (str): Environment to switch to ('dev', 'qa', or 'prod')
            
        Returns:
            bool: True if switch was successful, False otherwise
        """
        env = env.lower()
        if env not in cls.ENV_FILES:
            logger.error(f"Invalid environment: {env}")
            return False
            
        try:
            # Get the path to the environment file
            env_file = cls.ENV_FILES[env]
            
            # Copy the environment file to .env
            shutil.copy2(env_file, '.env')
            
            logger.info(f"Successfully switched to {env.upper()} environment")
            return True
            
        except Exception as e:
            logger.error(f"Failed to switch environment: {str(e)}")
            return False

# Command line interface for switching environments
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python env_switcher.py [dev|qa|prod]")
        sys.exit(1)
        
    env = sys.argv[1].lower()
    if EnvironmentSwitcher.switch_env(env):
        print(f"Successfully switched to {env.upper()} environment")
    else:
        print(f"Failed to switch to {env.upper()} environment")
        sys.exit(1)