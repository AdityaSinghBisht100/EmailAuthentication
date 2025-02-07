import React, { useState } from 'react';
import { signupUser, loginUser } from '../components/authService';

const AuthPage = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      if (isLogin) {
        await loginUser(email, password);
      } else {
        if (password !== confirmPassword) {
          setError('Passwords do not match');
          return;
        }
        const response = await signupUser(email, password, confirmPassword);
        setMessage('Verification email sent. Please check your inbox.');
        await signupUser(email, password, confirmPassword);
      }
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="relative min-h-screen flex overflow-hidden bg-gray-100">
      {/* Curved Background Divide */}
      <div className="absolute top-0 left-0 w-full h-full z-0">
        <svg width="100%" height="100%" viewBox="0 0 1440 900" preserveAspectRatio="none">
          <path 
            d="M0 0 L1440 0 L1440 900 L0 900 Q600 600, 1440 600" 
            fill="#7E57C2" 
            className="opacity-90"
          />
        </svg>
      </div>

      {/* Left Side (Purple) */}
      <div className="w-1/2 z-10 flex items-center justify-center p-12 text-white">
        <div className="max-w-md space-y-6">
          <h1 className="text-5xl font-bold mb-6 text-black ">Secure Digital Identity</h1>
          <p className="text-xl mb-6 leading-relaxed text-black">
            Protect your digital footprint with our cutting-edge authentication platform. 
            Experience seamless, secure access across all your digital interactions.
          </p>
          
          <div className="space-y-4">
            <div className="flex items-center space-x-4">
              <div className="bg-white/20 rounded-full p-3">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </div>
              
            </div>
          </div>
        </div>
      </div>

      {/* Right Side (White) */}
      <div className="w-1/2 z-20 flex items-center justify-center">
        <div className="bg-white rounded-xl shadow-2xl p-10 w-96">
          <h2 className="text-3xl font-bold mb-6 text-center text-gray-800">
            {isLogin ? 'Welcome Back' : 'Create Account'}
          </h2>
          
          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4">
              {error}
            </div>
          )}
          
          <form onSubmit={handleSubmit} className="space-y-4">
            <input
              type="email"
              placeholder="Email Address"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
              required
            />
            
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
              required
            />
            
            {!isLogin && (
              <input
                type="password"
                placeholder="Confirm Password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                required
              />
            )}
            
            <button 
              type="submit" 
              className="w-full bg-purple-600 text-white py-2 rounded-md hover:bg-purple-700 transition duration-300"
            >
              {isLogin ? 'Login' : 'Sign Up'}
            </button>
          </form>
          
          <div className="text-center mt-4">
            <button 
              onClick={() => setIsLogin(!isLogin)}
              className="text-purple-600 hover:underline"
            >
              {isLogin 
                ? 'Need an account? Sign Up' 
                : 'Already have an account? Login'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AuthPage;