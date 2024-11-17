# Web Automation Testing Framework (WAT)

## Overview
This is a test automation framework built using Python, Selenium WebDriver, and Behave for automated testing of web applications. The framework follows the Page Object Model design pattern and uses BDD (Behavior Driven Development) approach.


## Project Structure
```
WAT/
├── features/                     # BDD test features and step definitions
│   ├── steps/                   # Step definition files
│   │   ├── __init__.py         # Makes steps directory a Python package
│   │   └── homepage_steps.py    # Step definitions for homepage tests
│   ├── environment.py           # Behave hooks for test setup/teardown
│   └── homepage_navigation.feature  # Feature file for homepage tests
│
├── pages/                       # Page Object Model implementations
│   ├── __init__.py             # Makes pages directory a Python package
│   ├── base_page.py            # Base class with common methods and wait strategies
│   └── home_page.py            # Homepage specific page object
│
├── utilities/                   # Framework utilities and configurations
│   ├── __init__.py             # Makes utilities directory a Python package
│   ├── driver_factory.py       # WebDriver management with version compatibility
│   ├── config.py               # Test configuration and environment settings
│   └── env_switcher.py         # Utility to switch between environments
│
├── screenshots/                 # Directory for failure screenshots
├── .env                        # Default/QA environment settings
├── .env.dev                    # Development environment settings
├── .env.prod                   # Production environment settings
├── README.md                   # Project documentation
└── requirements.txt            # Project dependencies
```

## Features
- Environment-specific configuration (dev, qa, prod)
- Page Object Model implementation
- Explicit wait strategies for reliable element interaction
- Screenshot capture on test failures
- Detailed logging
- Multiple browser support
- Headless mode support
- Version-compatible WebDriver management

## Setup and Installation

### Prerequisites
- Python 3.x
- Chrome browser
- Git

### Installation Steps
1. Clone the repository:
```bash
git clone [repository-url]
cd WAT
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # For Unix/MacOS
venv\Scripts\activate     # For Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create environment configuration files:

**.env (QA Environment - Default)**
```ini
TEST_ENV=qa
BROWSER=chrome
HEADLESS=False
DEFAULT_TIMEOUT=10
EXPLICIT_TIMEOUT=20
```

Similar files needed for .env.dev and .env.prod with appropriate settings.

## Running Tests

### Basic Test Execution
```bash
behave
```

### Run with Detailed Logging
```bash
behave -v --logging-level=INFO
```

### Run Specific Feature
```bash
behave features/homepage_navigation.feature
```

## Environment Management

### Switching Environments
The framework supports three environments:
- Development (dev)
- Quality Assurance (qa)
- Production (prod)

To switch environments, either:
1. Copy the appropriate .env.* file to .env
2. Use the env_switcher.py utility:
```bash
python utilities/env_switcher.py [dev|qa|prod]
```

## Framework Components

### Page Objects
- **BasePage**: Provides common functionality and wait strategies
- **HomePage**: Implements homepage-specific elements and verifications

### Configuration
- Environment-specific settings
- Browser configurations
- Timeout settings
- URL management

### Utilities
- **DriverFactory**: Manages WebDriver creation with version compatibility
- **Config**: Handles environment configuration
- **EnvSwitcher**: Manages environment switching

## Logging and Debugging
- Detailed logging with different log levels
- Screenshot capture on test failures
- Environment-specific logging
- Step-by-step execution logging

## Current Test Coverage
1. Homepage Navigation
   - Browser launch verification
   - URL navigation
   - Homepage element verification

## Best Practices Implemented
- Explicit wait strategies
- Page Object Model
- Configuration management
- Error handling and logging
- Screenshot capture for failures
- Environment-specific testing
- Clean code structure
- Proper documentation

## Contributing
1. Create a feature branch
2. Implement changes with appropriate tests
3. Update documentation
4. Submit pull request

## Future Enhancements
- [ ] Add more feature tests
- [ ] Implement detailed reporting
- [ ] Add parallel test execution
- [ ] Integrate with CI/CD
- [ ] Add API testing capabilities
- [ ] Implement cross-browser testing
- [ ] Add data-driven testing capabilities

## Troubleshooting
- Check environment configuration in .env file
- Verify Chrome browser and ChromeDriver versions
- Review logs in terminal output
- Check screenshots directory for failure captures
- Verify Python and dependency versions

## Contact
[Moise Dore]
[MoiseDore@gmail.com]
[LinkedIn](https://www.linkedin.com/in/moise-dore-1b5a6a