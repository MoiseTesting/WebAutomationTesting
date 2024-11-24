# Web Automation Testing Framework

## Overview
A test automation framework built using Python, Selenium WebDriver, and Behave for automated testing of web applications. The framework follows the Page Object Model design pattern and uses BDD (Behavior Driven Development) approach.

## Project Structure
```
WAT/
├── features/                     # BDD test features and step definitions
│   ├── steps/                   # Step definition files
│   │   ├── __init__.py         # Makes steps directory a Python package
│   │   ├── sample_login_steps.py    # Step definitions for login tests
│   │   ├── homepage_steps.py        # Step definitions for homepage navigation
│   │   ├── formspage_steps.py       # Step definitions for Forms page tests
│   ├── environment.py           # Behave hooks for test setup/teardown
│   ├── sample_login.feature     # Feature file for login tests
│   └── forms_page.feature       # Feature file for Forms page functionality
│
├── pages/                       # Page Object Model implementations
│   ├── __init__.py             # Makes pages directory a Python package
│   ├── base_page.py            # Base class with common methods
│   ├── sample_page.py          # Login page-specific object
│   └── forms_page.py           # Forms page-specific object
│
├── utilities/                   # Framework utilities and configurations
│   ├── __init__.py             # Makes utilities directory a Python package
│   ├── driver_factory.py       # WebDriver management
│   ├── config.py               # Test configuration and environment settings
│   └── env_switcher.py         # Utility to switch between environments
│
├── screenshots/                 # Directory for screenshots (success and failures)
├── downloads/                   # Directory for downloaded files during tests
├── CV_ZIP/                      # Directory containing test files (CV, ZIP)
│   ├── index.html
│   └── github-pages.zip
├── .env                        # Environment configuration
├── .env.dev                    # Development environment settings
├── .env.prod                   # Production environment settings
└── requirements.txt            # Project dependencies
```

## Features
- Environment-specific configuration (dev, qa, prod)
- Page Object Model implementation
- Explicit wait strategies
- Screenshot capture on test failures & debugging
- Multiple browser support
- Headless mode support
- GitHub Actions integration for CI/CD
- File upload and download handling
- Dynamic file paths for portability in CI/CD (e.g., GitHub Actions)

## Setup and Installation

### Prerequisites
- Python 3.x
- Chrome browser
- Git

### Installation Steps
1. Clone the repository:
```bash
git clone https://github.com/MoiseTesting/WebAutomationTesting.git
cd WebAutomationTesting
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

### Running Tests
Run all tests:
```bash
behave
```

Run specific feature:
```bash
behave features/sample_login.feature

```

Run with specific tags:
```bash
behave --tags=@login
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
## Test Scenarios
Currently implemented test scenarios include:
1. Login Page Navigation
2. Successful Login
3. Invalid Login Attempt
4. Registering a new account
5. filling out registartion form and Pizza form

 Forms Page Tests
6. Successfully navigate to the Forms page.
7. Fill out the basic form controls and submit.
8. Verify the "Download File" functionality.
9. Fill out the "Non-English Labels and Locators" section.

### Utilities
- **DriverFactory**: Manages WebDriver creation with version compatibility
- **Config**: Handles environment configuration
- **EnvSwitcher**: Manages environment switching

## Logging and Debugging
- Detailed logging with different log levels
- Screenshot capture on test failures
- Environment-specific logging
- Step-by-step execution logging

## Environment Configuration
The framework supports three environments:
- Development (dev)
- Quality Assurance (qa)
- Production (prod)

Environment variables are managed through .env files:
```ini
TEST_ENV=qa
BROWSER=chrome
HEADLESS=False
DEFAULT_TIMEOUT=10
EXPLICIT_TIMEOUT=20
```
## Best Practices Implemented
- Explicit wait strategies
- Page Object Model
- Configuration management
- Error handling and logging
- Screenshot capture for failures
- Environment-specific testing
- Clean code structure
- Proper documentation

## CI/CD Integration
This project uses GitHub Actions for continuous integration. The workflow:
- Runs on push to main branch
- Executes tests in headless mode
- Captures and stores test artifacts
- Provides test execution reports

##Logging and Debugging
- Detailed logging with different log levels.
- Screenshot capture for debugging and test failures.
- Step-by-step execution logs for all scenarios.

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Future Enhancements
- [ ] Add more feature tests
- [ ] Implement detailed reporting
- [ ] Add parallel test execution
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
[LinkedIn](https://www.linkedin.com/in/moise-dore-1b5a6a)
