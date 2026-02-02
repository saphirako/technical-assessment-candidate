# Technical Assessment: Product Replacement Search

## Overview

This is a fullstack technical assessment where you will build a backend API and a frontend application for finding replacement products. The system should query an external API that we will provide, process and resolve conflicts in the data, and provide a search interface for finding suitable replacement products.

We expect you to use AI tools, but be prepared to discuss how you used them and explain any code you accepted from AI. Even better if you can walk us through your development process. You are welcome to make as much progress as you'd like, but please aim to spend less than 3 hours on this assessment - we will discuss your progress and work on follow-up questions during the interview. Our objective is to get a sense of what it would be like to work with you.

### What We're Looking For

- Clean, well-structured, readable code
- Sensible design choices

## Data Description

### Synthetic Product Generator

A simple server has been set up that returns synthetic products for each request. Code to retrieve products as a generator is provided in `backend/starter.py`.

### Product Details

Every product will have the following fields:

- `source` (one of `Source A`, `Source B`, `Source C`, `Source D`, `Source E`)
- `mpn` (ten digit alphanumeric string)
- `classification` (can be `null`)
- `lifecycle status` (one of `Active`, `End of Life`, `Obsolete`)
- `RoHS compliance` (`True` or `False`)
- `min/max operating range` (`int between -40 and +85` (Celsius))

Additionally, each product will have up to twenty attributes that need to match 1:1, such as:

- For LEDs: `color`, `brightness`, `size`
- For Resistors: `resistance`, `material`, `surface mount`

To simplify this, additional attributes will be of the form `{attributeX: number between 0 and 4 inclusive}` ex. `{attribute8: 0, attribute15: 4}`

### Attribute Conditions

- Some products may have fewer than three attributes or contain garbage values.
- Conflicting information for `mpn`s from different sources may be present.

## Objective

### Parametric Search

A customer provides the operating range for their environment, minimum compliance, and an obsolete part. The task is to find `mpn`s that:

1. Have compliance greater than or equal to the minimum.
2. Have an operating range that contains the required band.
3. Have a life cycle status that is not obsolete.

### Ranking Products

Products should be ranked to help users find the best replacement. You'll need to decide how to prioritize and order results.

## Design Challenges

### Database Strategy

- Decide whether to use a SQL (e.g., `sqlite3`) or NoSQL (e.g., `mongo`) architecture. Skeleton code for both options is provided in `backend/starter.py`.

### Handling `null`/`garbage` Values

- Decide a strategy to use. E.g. dropping these values or assuming they match the target value

### Handling Conflicting Information

- Decide a strategy to use, e.g.:
  - Always taking the most recent opinion.
  - Storing all values.
  - Using a hybrid approach

### Frontend User Interface

- Design a clear and intuitive search interface for collecting search parameters (MPN, operating range, compliance requirements, etc.)
- Consider how to display product attributes, compliance status, and operating ranges effectively

## Setup Instructions

**Development Environment**: You are welcome to proceed with using the development environment that is most efficient for you.

### Option 1: Using DevContainer

**Prerequisites**: Docker Desktop (or Docker Engine) must be installed and running on your machine.

A complete devcontainer setup is provided in `.devcontainer/` that includes:

- Python 3.11+ with Poetry pre-installed
- Node.js 20+ with yarn/npm pre-installed
- SQLite3 support (no setup needed - works out of the box)
- PostgreSQL service running in a container (port 5432) - available at `postgres:5432` from within container
- MongoDB service running in a container (port 27017) - available at `mongodb:27017` from within container
- VS Code extensions for Python and TypeScript/React development
- All dependencies automatically installed on container creation

**To use the devcontainer:**

1. Open the repository in an editor that supports the Dev Containers extension (such as VS Code, Cursor, GitHub Codespaces)
2. When prompted, click "Reopen in Container" (or use Command Palette: "Dev Containers: Reopen in Container")
3. Wait for the container to build and dependencies to install
4. Database services:
   - **SQLite**: Ready to use immediately (no setup needed)
   - **PostgreSQL**: Available at `postgres:5432` (or `localhost:5432` from your host machine)
   - **MongoDB**: Available at `mongodb:27017` (or `localhost:27017` from your host machine)
5. Follow the setup steps below, but skip the Prerequisites section

### Option 2: Local Development

### Prerequisites

- Python 3.11+ with Poetry
- Node.js 20+ and yarn/npm (Node 24 recommended)
- MongoDB (optional, if using MongoDB instead of SQLite)
- Access to the external API server (URL and API key will be provided)

## Components

### External API (provided)

The external API server runs separately and is not included in this repository. You will be provided with:

- Server URL
- API key for authentication

### Backend

1. **Install dependencies:**

   ```bash
   poetry install
   ```

   This will create a `.venv` virtual environment in the project root.

2. **Configure secrets:**

   ```bash
   cp backend/secrets.json.example backend/secrets.json
   # Edit backend/secrets.json with your API key and server URL
   ```

3. **Choose your database:**

   Choose one of: **SQLite** (simplest, no setup), **PostgreSQL**, or **MongoDB**. All work in both devcontainer and local environments.

   - **SQLite**: No connection string needed. Use `sqlite3.connect("products.db")` directly in your code.
   - **PostgreSQL**: 
     - Devcontainer: `postgresql://postgres:password@postgres:5432/products` (use `postgres` hostname)
     - Local: Install PostgreSQL, then use `postgresql://postgres:password@localhost:5432/products`
   - **MongoDB**:
     - Devcontainer: `mongodb://mongodb:27017/` (use `mongodb` hostname)
     - Local: Install MongoDB, then use `mongodb://localhost:27017/`
   
   Optionally add connection strings to `secrets.json`.

4. **Run the backend server:**
   ```bash
   poetry run python backend/app.py
   ```
   The server will start on `http://localhost:8000`

### Frontend

1. **Install dependencies:**

   ```bash
   yarn install
   # or
   npm install
   ```

   This will install Node.js dependencies at the project root.

2. **Configure environment (optional):**

   - The frontend is pre-configured to connect to `http://localhost:8000` via `.env.local`
   - If your backend runs on a different URL or port, edit `.env.local` at the root and update `VITE_API_BASE_URL`

3. **Run the development server:**
   ```bash
   yarn dev
   # or
   npm run dev
   ```
   The frontend will start on `http://localhost:5173`

## Your Tasks

### Backend


1. **Create a data population script/pipeline**:

   - Query the external API using helpers from `starter.py` (`product_generator()`, `reset_generator()`)
   - Populate your chosen database (SQLite, PostgreSQL, or MongoDB) with products from the external API
   - Resolve conflicts (handle nulls, conflicting sources from different data sources)
   - Build a canonical product collection
   - This script runs separately to populate your datastore before starting the API server
   - The external API provides "untrustworthy" data - products may have:
     - Conflicting information for the same MPN from different sources
     - Null/garbage values
     - Incorrect data from certain sources
   - You need to decide on a strategy to handle these issues and build a reliable canonical product database
   - You can run the script using the command:
     ```bash
     poetry run python backend/populate_db.py # or whatever you name your script
     ```
   - The backend API (`app.py`) should then read from this populated datastore

2. **Set up Flask API server** - Template provided in `backend/app.py`:

   - Initialize your database connection (SQLite, PostgreSQL, or MongoDB)
   - Connect to your populated datastore
   - The API should read from your populated datastore, not query the external API directly

3. **Design and implement API endpoint(s)** for finding replacement products:
   - Design your own request/response format based on the requirements
   - The endpoint should:
     - Read from your populated datastore (not the external API)
     - Accept search parameters (MPN, operating range, compliance requirements, etc.)
     - Return ranked replacement products with relevant metadata
   - Consider what information the frontend needs to display results effectively
   - The exact request/response format is up to you - design it with the user in mind

### Frontend

The frontend boilerplate is provided, but you need to implement:

1. **Search interface** - Build a form/component to collect search parameters (MPN, operating range, compliance requirements, etc.)
2. **API integration** - Implement API calls in `frontend/app/services/api/api.ts` to match your backend API design
   - Define TypeScript types in `frontend/app/services/api/types.ts`
   - The boilerplate provides RTK Query setup - you need to implement the actual endpoints
3. **Results display** - Design how to present the ranked replacement products

The frontend includes basic routing, MUI theme/components, RTK Query, and a simple Home page. Feel free to modify any files as needed - the boilerplate is just a starting point.

## Good Luck!

We look forward to seeing your approach to these challenges.
