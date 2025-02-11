# Task Manager

## Description
Task Manager is a web-based application that allows users to create, track, and manage tasks efficiently. It provides a collaborative space where team members can assist each other in project development. The project is designed to be flexible and can easily be integrated into larger systems.

## Live Demo 🌍
You can try the Task Manager online here:  
🔗 **[Visit Task Manager](https://your-deployed-site.com/)**  

### **Test User Credentials**
To explore the platform without signing up, use the following test account:
- **Login:** `user`
- **Password:** `user12345`

## Visuals
### Database Structure
The database schema can be found in `database_schema.svg`.

## Installation
### Requirements
- Python 3.8+
- Django
- PostgreSQL (or SQLite for local development)
- pip

### Steps
1. Clone the repository:
   ```bash
   git https://github.com/kkkkkkkkatya/task-manager.git
   cd task-manager
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   Fill in the `.env` file with necessary configurations.

5. Run database migrations:
   ```bash
   python manage.py migrate
   ```
6. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Usage
- Visit `http://127.0.0.1:8000/` in your browser.
- Register or log in to create and manage tasks.
- Assign tasks to team members and track their progress.

## Support
For support, open an issue on [GitHub Issues](https://github.com/your-username/task-manager/issues) or contact the maintainers.

## Roadmap
- Implement notifications for task updates
- Add integrations with third-party tools (e.g., Slack, Trello)
- Improve task filtering and reporting features

## Contributing
Contributions are welcome! Follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them.
4. Push the changes to your fork and create a pull request.

## Authors and Acknowledgment
Developed by Kateryna

## Project Status
Active - ongoing development and improvements.
 