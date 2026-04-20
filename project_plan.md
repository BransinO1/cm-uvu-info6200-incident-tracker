# Project Plan: Incident Log Tracker

## Author
Corbin Meacham
UVU Spring 2026
INFO 6200

## Section 1: Project Overview

The Incident Log Tracker is a data management application designed to improve organizational visibility, accountability, and consistency in incident handling. This system enables employees, team leads, and managers to record, track, and manage incidents that occur within their operations. Users can document incidents with key details, monitor status throughout the resolution process, and follow up on corrective actions from initial reporting through closure.

## Section 2: Core Features

- Create a new incident record with a description and date  
- View a list of all reported incidents and their current status  
- Update an incident’s status as it progresses toward resolution  
- Edit or close an incident once it has been resolved  

## Section 3: Data Model

**Incident Record Structure:**

- `incident_id` (integer) – A unique identifier for the incident  
- `title` (string) – A brief summary of the incident  
- `description` (string) – Detailed information about the incident  
- `incident_date` (string) – The date the incident occurred  
- `status` (string) – Current state of the incident (open, in progress, resolved)  
- `reported_by` (string) – Name of the reporting user  
- `created_at` (string) – Timestamp of when the incident report was created

## Chunk 1: Command-Line Interface (CLI) Prototype

In this development chunk, I worked on implementing a functional command-line interface (CLI) prototype of the Incident Log Tracker. The prototype allows users to add new incidents, view a list of all recorded incidents, and update the status of existing incidents. All incident data is stored in-memory using a single global data structure for the duration of the program’s execution. This first chunk establishes the core functionality of the application and demonstrates how incidents move through their lifecycle, in a simple interactive environment.

## Chunk 2: Refactoring for Structured Data

During this second development phase, the application’s internal data representation was updated to align with the formal data model defined in the project plan. Each incident is now stored as a single dictionary whose keys match the specified fields, with the addition of `reported_by` and `created_at`. These records are maintained in a master list that represents the active dataset during program execution.

The listing functionality was updated to iterate through the structured records and display them in a clear, human-readable format. Although the internal architecture changed, the user experience of the CLI remained the same, and users can still add, view, and update incidents as before.

Data integrity was further improved by adding date input validation to ensure it follows the required `YYYY-MM-DD` format. This refactor better positions the application for future enhancements such as file-based or database persistence.

## Chunk 3: Achieving Data Persistence

In this phase, the Incident Log Tracker was enhanced to prevent data loss between program runs by introducing file-based persistence using JSON. On startup, the application now checks for the presence of a data file (data.json) and automatically loads existing incidents if it is found; otherwise, it safely initializes an empty collection. This ensures the program can run without errors regardless of whether prior data exists.

The system was further updated so that any modification, such as adding a new incident or changing a status, immediately writes the full dataset back to file in a structured, human-readable format. While these changes significantly improved reliability, the command-line experience for users remains simple and familiar. Incidents now survive through application restarts, bringing the project closer to real-world operational expectations.

## Chunk 4: "Hello, Web!" with Flask

In this phase, the project began transitioning from a command-line interface to a web-based application by implementing a minimal Flask server. A new Python script (web_app.py) was created to start up a Flask application, define a root route (/), and return a simple HTML page when accessed through a browser. The development server is configured to run locally, allowing the application to function as a temporary website.

While the app.py incident tracker functionality remains in the CLI for now, this milestone builds out the foundation for future integration of web-based routes, forms, and dynamic content. This was the first step toward converting the Incident Log Tracker into a fully web-accessible application.

## Chunk 5: From CLI Input to Web Form

In this development phase, the application was transitioned from a simple command-line input to a web-based form using Flask. A new route (/add) was created to render a basic HTML form that collects all required incident data fields. When the form is submitted, the application processes the POST request, structures the submitted data into a dictionary that matches it to the existing JSON, and immediately saves it to the JSON data file that we created in a previous step.

After successfully storing the incident, the application redirects the user back to the add form. This milestone connects the persistent data layer to a functional web interface, moving this project much closer toward being a functional browser-based Incident Log Tracker.

## Chunk 6: Rendering Dynamic Data with Jinja2

This week, the application was enhanced to dynamically display all stored incidents on a webpage. A new route was added to the Flask application that loads all incident records from the JSON data file and passes them to a Jinja2 template for rendering on the webpage. The template uses a Jinja for-loop to iterate through the incident collection and generate HTML for each record, allowing the page to automatically display any number of incidents without creating multiple static pages. This update connects the stored data to the user interface and is a great example of how a single template can dynamically render database content in a web application.

## Chunk 7: Database Integration with SQLAlchemy

In this development chunk, the application was upgraded from an in-memory data structure (JSON) to a persistent SQLite database using SQLAlchemy as the Object-Relational Mapping (ORM) tool. This change transitions the application to a more realistic, real-world data management system. The Incident model was defined to represent the structure of each record, and database operations such as creating, retrieving, and updating incidents were implemented through ORM-based queries. This enhancement lays the foundation for future expansion, such as more advanced querying, filtering, and integration with a user interface. Overall, this chunk represents a transition from a simple prototype to a more robust and production-oriented architecture.

## Chunk 8: Full CRUD Functionality

In this phase, the Incident Log Tracker was updated with full CRUD (Create, Read, Update, Delete) functionality using the SQLAlchemy database. After this week's updates, users can now add new incidents, view all records, update statuses, and remove incidents entirely through the web interface. All operations interact seamlessly with the persistant SQLite database, ensuring data integrity and consistency. This milestone establishes the application as a fully functional, production-ready system while maintaining the simplicity and usability established in earlier phases.

## Chunk 9: User Authentication & Data Ownership

In this development phase, the Incident Log Tracker was upgraded with full user authentication and session management. A new User model was added with securely hashed passwords, and each incident is now linked to its creator through a foreign key. Users can register, log in, and log out, and all incident routes are protected so only authenticated users can access them. The system enforces data ownership, ensuring users can view, edit, and delete only their own incidents, which greatly enhances security, usability, and readiness for a multi-user environment.

## Chunk 10: RESTful API Integration

In this phase, the Incident Log Tracker was equipped with a RESTful API to make application data accessible to external systems. New protected endpoints were introduced under /api/v1/ to allow authenticated users to retrieve all of their incidents or a specific incident in JSON format. The API enforces authentication, ownership validation, and proper HTTP status codes. This change improves the system’s flexibility making it ready for integration with other applications or services.

## Chunk 11: Production Hardening & Deployment Readiness

In this chunk, the Incident Log Tracker was updated for production by implementing industry-standard configuration and deployment practices. All sensitive configuration data, including the secret key and database URI, was moved to environment variables and documented through a .env.example file. This leads to improved security and flexibility across environments. The project was also updated with a clean requirements.txt, an improved .gitignore, and support for running on a WSGI server (waitress). These updates confirm that the application is properly packaged and ready for real-world deployment.