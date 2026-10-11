# Discord Fact Bot
### Intelligent Information Retrieval and Voice Synthesis System

## 1. Project Overview

The **Discord Fact Bot** is a Python-based automation solution designed to provide interactive access to informational content through Discord. The system integrates external web services, command-based interactions, and text-to-speech technology to deliver a more dynamic user experience.

The application enables users to retrieve information across different knowledge domains, including science, history, astronomy, and general knowledge, while offering configurable voice synthesis based on the voices available on the host system.

## 2. Business Objectives

The project aims to demonstrate the practical application of automation and external service integration through a modular and extensible software solution.

Its primary objectives are:

- Automate user interactions within Discord servers.
- Retrieve informational content from external APIs.
- Organize information retrieval by subject.
- Integrate text-to-speech capabilities.
- Implement error handling for external service requests.
- Establish a foundation for future improvements and additional features.

## 3. Core Features

### 3.1. Automated Welcome System

The `!start` command generates a personalized welcome message for the user interacting with the bot.

### 3.2. Subject-Based Information Retrieval

The `!fact` command retrieves article summaries from the Portuguese Wikipedia API.

Supported categories include:

- **Science:** scientific concepts and discoveries.
- **History:** historical events and subjects.
- **Astronomy:** celestial objects and astronomical concepts.
- **General Knowledge:** broad informational searches.

The system retrieves relevant articles, extracts introductory content, and provides a reference link for further reading.

### 3.3. Configurable Voice Synthesis

The application integrates the `pyttsx3` library to convert retrieved text into speech.

Available commands allow users to request a masculine or feminine voice, provided a compatible voice is installed and identifiable on the host system.

### 3.4. Voice Inventory

The `!vozes` command displays the voices available through the local speech synthesis engine, supporting voice selection and troubleshooting.

### 3.5. Error Handling

The application includes basic error handling for HTTP requests, unavailable services, invalid responses, and unsupported command parameters.

## 4. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application development |
| discord.py | Discord bot integration |
| Requests | HTTP communication with external services |
| pyttsx3 | Local text-to-speech synthesis |
| Wikipedia API | Retrieval of informational content |
| asyncio | Asynchronous task coordination |

## 5. Installation Requirements

The project requires Python, an internet connection, a Discord application configured as a bot, and a compatible local speech synthesis environment.

Install the required dependencies:

```bash
pip install discord.py requests pyttsx3
```

## 6. Configuration

### Discord Application

1. Create an application through the [Discord Developer Portal](https://discord.com/developers/applications).
2. Configure the bot and enable the **Message Content Intent**.
3. Invite the bot to the intended server with the necessary permissions.
4. Store the authentication token securely.

### Authentication

The current implementation imports the token from a local `token.py` file.

For improved security, credentials should be stored outside the source code and excluded from version control.

Add the following entries to `.gitignore`:

```text
token.py
.env
__pycache__/
```

Never publish bot tokens or other authentication credentials in a public repository.

## 7. Command Reference

| Command | Description |
|---|---|
| `!start` | Displays a personalized welcome message |
| `!fact` | Retrieves general informational content |
| `!fact ciencia` | Searches for science-related content |
| `!fact historia` | Searches for history-related content |
| `!fact astronomia` | Searches for astronomy-related content |
| `!voz masculina` | Attempts to select a masculine voice |
| `!voz feminina` | Attempts to select a feminine voice |
| `!vozes` | Lists locally available speech voices |

## 8. System Architecture

The application follows a modular structure consisting of command processing, external data retrieval, response formatting, and speech synthesis.

The general workflow is:

1.
