# Stremio Manager

A self-hosted system to manage Stremio streaming for friends and family.

## Overview

This project provides a simple web interface to automate Stremio account setup. It uses a shared Torbox debrid subscription and links individual Trakt accounts for watch history tracking.

## Project Structure

- `backend/`: The FastAPI application that handles all the logic.
- `frontend/`: The Vue.js user-facing web portal.
- `docker-compose.yml`: Orchestrates the services for development and production.

## Getting Started

1.  Clone this repository.
2.  Create a `.env` file in the `backend` directory from the `.env.example`.
3.  Fill in your Torbox and Trakt API credentials in the `.env` file.
4.  Run `docker-compose up --build`.

The backend API will be available at `http://localhost:8000`.
The frontend will be available at `http://localhost:8080` (once configured).
