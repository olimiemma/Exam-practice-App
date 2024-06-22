import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [examType, setExamType] = useState('');
  const [question, setQuestion] = useState(null);
  const [userAnswer, setUserAnswer] = useState([]);
  const [feedback, setFeedback] = useState(null);

  const fetchQuestion = async () => {
    try {
      const response = await axios.get(`/question/${examType}`);
      setQuestion(response.data);
      setUserAnswer([]);
      setFeedback(null);
    } catch (error) {
      console.error('Error fetching question:', error);
    }
  };

  const handleAnswerSubmit = async () => {
    try {
      const response = await axios.post('/check-answer', {
        question_id: question._id,
        user_answer: userAnswer
      });
      setFeedback(response.data);
    } catch (error) {
      console.error('Error submitting answer:', error);
    }
  };

  const handleOptionSelect = (index) => {
    const newAnswer = userAnswer.includes(index)
      ? userAnswer.filter(i => i !== index)
      : [...userAnswer, index];
    setUserAnswer(newAnswer);
  };

  return (
    <div className="App">
      <h1>Exam Practice</h1>
      <select value={examType} onChange={(e) => setExamType(e.target.value)}>
        <option value="">Select Exam Type</option>
        <option value="IELTS">IELTS</option>
        <option value="AWS">AWS Certification</option>
        <option value="CFA">CFA</option>
        <option value="CPA">CPA</option>
      </select>
      <button onClick={fetchQuestion}>Get Question</button>

      {question && (
        <div>
          <h2>{question.question_text}</h2>
          {question.options.map((option, index) => (
            <div key={index}>
              <input
                type="checkbox"
                checked={userAnswer.includes(index)}
                onChange={() => handleOptionSelect(index)}
              />
              {option}
            </div>
          ))}
          <button onClick={handleAnswerSubmit}>Submit Answer</button>
        </div>
      )}

      {feedback && (
        <div>
          <h3>{feedback.is_correct ? 'Correct!' : 'Incorrect'}</h3>
          <p>{feedback.is_correct ? 'Well done!' : `The correct answer was: ${feedback.correct_answer.join(', ')}`}</p>
        </div>
      )}
    </div>
  );
}

export default App;