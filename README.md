# Aexam

Aexam is a web-based application designed to help users practice for various exams and certifications. It provides a customizable experience where users can select specific exam types and difficulty levels to generate relevant practice questions.

## Features

- User authentication system
- Selection of various exam types (IELTS, AWS Certification, CFA, CPA, etc.)
- Difficulty levels for each exam type (Easy, Medium, Hard)
- Dynamic question generation using OpenAI's GPT model
- Progress tracking for users
- Responsive web design for desktop and mobile use

## Tech Stack

- Frontend: React.js
- Backend: Flask (Python)
- Database: MongoDB
- API Integration: OpenAI GPT for question generation

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Node.js (v14 or later)
- Python (v3.7 or later)
- MongoDB
- OpenAI API key

## Installation

### Backend Setup

1. Clone the repository:
   ```
   git clone https://github.com/olimiemma/aexam.git
   cd aexam/backend
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```
   export FLASK_APP=app.py
   export FLASK_ENV=development
   export MONGO_URI=mongodb://localhost:27017/aexam_db
   export JWT_SECRET_KEY=your_secret_key_here
   export OPENAI_API_KEY=your_openai_api_key_here
   ```

5. Run the Flask application:
   ```
   flask run
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd ../frontend
   ```

2. Install the required npm packages:
   ```
   npm install
   ```

3. Start the React development server:
   ```
   npm start
   ```

## Usage

1. Open your web browser and go to `http://localhost:3000`
2. Register for a new account or log in if you already have one
3. Select an exam type and difficulty level
4. Click "Get Question" to receive a practice question
5. Answer the question and submit to receive feedback
6. Track your progress over time

## Contributing

We welcome contributions to Aexam! Please follow these steps to contribute:

1. Fork the repository
2. Create a new branch: `git checkout -b feature-branch-name`
3. Make your changes and commit them: `git commit -m 'Add some feature'`
4. Push to the original branch: `git push origin feature-branch-name`
5. Create the pull request

Alternatively, see the GitHub documentation on [creating a pull request](https://help.github.com/articles/creating-a-pull-request/).

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Contact

If you want to contact me, you can reach me at `https://www.linkedin.com/in/olimiemma/`.

## Acknowledgements

- OpenAI for providing the GPT model API
- All contributors who have helped to build and improve Aexam
