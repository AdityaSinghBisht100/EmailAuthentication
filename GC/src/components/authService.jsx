// Signup API Call
export const signupUser = async (email, password, confirmPassword) => {
    try {
      const response = await fetch('http://localhost:8000/users/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email,
          password,
          confirm_password: confirmPassword
        })
      });
  
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Signup failed');
      }
  
      return await response.json();
    } catch (error) {
      console.error('Signup error:', error);
      throw error;
    }
  };
  
  
  export const loginUser = async (email, password) => {
    try {
      const response = await fetch('http://localhost:8000/users/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password })
      });
  
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Login failed');
      }
  
      return await response.json();
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  };
  
 
  export const verifyEmail = async (email, token) => {
    try {
      const response = await fetch('http://localhost:8000/users/verify', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, token })
      });
  
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Verification failed');
      }
  
      return await response.json();
    } catch (error) {
      console.error('Verification error:', error);
      throw error;
    }
  };